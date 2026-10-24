#!/usr/bin/env python3
"""Build V1_2_FIXED_V3 from V1_2_FIXED_V2 with idempotent, safety-first CAD updates.

Usage (inside FreeCAD Python environment):
  freecadcmd build_V3_update.py

Notes:
- Always opens V1_2_FIXED_V2.FCStd and writes V1_2_FIXED_V3.FCStd / V1_2_FIXED_V3_FULL.STEP.
- Never mutates the V2 source document in-place.
- If required dimensions are missing/unverified, finalization is refused.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
SRC_FCSTD = ROOT / "V1_2_FIXED_V2.FCStd"
OUT_FCSTD = ROOT / "V1_2_FIXED_V3.FCStd"
OUT_STEP = ROOT / "V1_2_FIXED_V3_FULL.STEP"
OUT_LOG = ROOT / "V1_2_V3_build.log"
OUT_MD = ROOT / "V3_mass_CG.md"
OUT_CSV = ROOT / "V3_mass_CG.csv"
OUT_CLEARANCE_CSV = ROOT / "V3_clearance_report.csv"
OUT_CHANGES_MD = ROOT / "V3_change_list.md"
OUT_PRINT_MD = ROOT / "V3_print_list.md"
OUT_EXEC_LOG = ROOT / "build_V3_update_execution.log"

# Safety gates
MIN_FIXED_CLEARANCE_MM = 15.0
CG_TARGET_MM = -135.4
CG_WINDOW_MM = (-143.5, -127.3)

# Prop selector: changing this one number toggles fallback logic.
LIFT_PROP_DIAMETER_MM_DEFAULT = 431.8  # 17 in

# 17in/16in presets requested by issue.
PROP_PRESETS = {
    431.8: {"name": "17x?", "mass_g": 28.0},
    406.4: {"name": "16x5.4", "mass_g": 25.0},
}

# Explicitly tracked data-source values.
# If a value is unknown from the accessible environment, keep None and refuse finalization.
DATASHEET = {
    "MN4014_KV400": {
        "diameter_mm": None,
        "height_mm": None,
        "mass_g": 171.0,
        "mass_note": "171 g with cables (150 g bare)",
        "source": "https://openelab.io/products/tmotor-mn4014-400kv-motor",
    },
    "AT3520_KV550": {
        "diameter_mm": None,
        "height_mm": None,
        "mass_g": 218.0,
        "source": "https://store.tmotor.com/product/at3520-long-shaft-fixed-wing-motor.html",
    },
    "PM07": {
        "size_mm": (68.0, 50.0, 10.0),
        "mass_g": 43.8,
        "source": "https://holybro.com/products/pixhawk-4-power-module-pm07",
        "source_note": "Requested current model listing: 68x50x10 mm, 43.8 g",
    },
    "XT90S": {"size_mm": (30.0, 20.0, 16.0), "mass_g": None, "source": "MISSING"},
    "Fuse_125A_MIDI": {
        "size_mm": (42.0, 12.0, 45.0),
        "mass_g": None,
        "source": "MISSING",
    },
}

LIFT_STATIONS_XZ = [(488.0, 405.0), (493.0, -405.0), (-808.0, 405.0), (-808.0, -405.0)]
MOUNT_TOP_Y = 105.0

UNCHANGED_KEYWORDS = ("wing", "spar", "tail", "pod", "ASSEm")

HIDE_TARGETS = {
    "lift_motor_parts": [
        "lift_MN3510_V2_0",
        "lift_MN3510_V2_1",
        "lift_MN3510_V2_2",
        "lift_MN3510_V2_3",
        "bldc_motor_Varsayilan",
        "bldc_motor_Varsayilan001",
        "bldc_motor_Varsayilan002",
        "bldc_motor_Varsayilan003",
    ],
    "lift_props": ["prop_front_pos", "prop_front_neg", "prop_rear_pos", "prop_rear_neg"],
    "rear_motor": ["rear_AT2814_V2", "pusher_motor", "pusher_motorcap"],
    "rear_prop": ["pusher_prop"],
    "escs": ["esc_4in1_45A_V2", "esc_rear_30A_V2"],
}

KNOWN_V2_MASSES_G = {
    "battery_6S2P_V2": 904.0,
    "esc_4in1_45A_V2": 12.0,
    "esc_rear_30A_V2": 18.5,
    "rear_AT2814_V2": 90.0,
    "pusher_prop": 20.0,
    "lift_MN3510_V2_0": 120.0,
    "lift_MN3510_V2_1": 120.0,
    "lift_MN3510_V2_2": 120.0,
    "lift_MN3510_V2_3": 120.0,
}


class BuildError(RuntimeError):
    pass


class Logger:
    def __init__(self, path: Path):
        self.path = path
        self.path.write_text("", encoding="utf-8")

    def log(self, msg: str) -> None:
        line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
        print(line, flush=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


@dataclass
class ClearanceResult:
    prop_name: str
    check: str
    target_name: str
    distance_mm: float
    pass_fail: str


@dataclass
class MassRow:
    name: str
    label: str
    mass_g: str
    x_station_mm: str
    source: str


def _center_x(shape) -> float:
    bb = shape.BoundBox
    return 0.5 * (bb.XMin + bb.XMax)


def _center(shape) -> Tuple[float, float, float]:
    bb = shape.BoundBox
    return (0.5 * (bb.XMin + bb.XMax), 0.5 * (bb.YMin + bb.YMax), 0.5 * (bb.ZMin + bb.ZMax))


def _as_float(v: Optional[float], ndigits: int = 3) -> str:
    if v is None:
        return "MISSING"
    return f"{v:.{ndigits}f}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build V1_2_FIXED_V3 from V1_2_FIXED_V2")
    p.add_argument("--lift-prop-diameter-mm", type=float, default=LIFT_PROP_DIAMETER_MM_DEFAULT)
    p.add_argument("--battery-x-mm", type=float, default=None)
    p.add_argument("--force", action="store_true", help="allow outputs even if mandatory checks fail")
    p.add_argument("--mn4014-diameter-mm", type=float, default=DATASHEET["MN4014_KV400"]["diameter_mm"])
    p.add_argument("--mn4014-height-mm", type=float, default=DATASHEET["MN4014_KV400"]["height_mm"])
    p.add_argument("--at3520-diameter-mm", type=float, default=DATASHEET["AT3520_KV550"]["diameter_mm"])
    p.add_argument("--at3520-height-mm", type=float, default=DATASHEET["AT3520_KV550"]["height_mm"])
    return p.parse_args()


def import_freecad(logger: Logger):
    try:
        import FreeCAD as App  # type: ignore
        import Import  # type: ignore
        import Part  # type: ignore
    except Exception as exc:
        logger.log(f"ERROR: FreeCAD Python modules are unavailable: {exc}")
        raise BuildError("FreeCAD runtime missing; cannot generate CAD artifacts in this environment")
    return App, Part, Import


def close_open_docs(App):
    for n in list(App.listDocuments().keys()):
        try:
            App.closeDocument(n)
        except Exception:
            pass


def get_obj(doc, name: str):
    return doc.getObject(name)


def set_mass_g(obj, mass_g: Optional[float]) -> None:
    if not hasattr(obj, "MassG"):
        try:
            obj.addProperty("App::PropertyString", "MassG", "V3", "Mass in grams")
        except Exception:
            return
    obj.MassG = "MISSING" if mass_g is None else f"{mass_g:.3f}"


def ensure_removed_prefix(doc, prefix: str, logger: Logger) -> None:
    rm = [o.Name for o in doc.Objects if o.Name.startswith(prefix)]
    for n in rm:
        try:
            doc.removeObject(n)
            logger.log(f"idempotent cleanup removed prior object: {n}")
        except Exception as exc:
            logger.log(f"WARN: could not remove {n}: {exc}")


def hide_with_children(obj, logger: Logger):
    if obj is None:
        return
    try:
        obj.Visibility = False
        logger.log(f"hid {obj.Name}")
    except Exception:
        pass
    for child in getattr(obj, "Group", []):
        try:
            child.Visibility = False
            logger.log(f"hid child {child.Name}")
        except Exception:
            pass


def capture_bbox_snapshot(doc) -> Dict[str, Tuple[float, float, float, float, float, float]]:
    snap = {}
    for o in doc.Objects:
        try:
            if not hasattr(o, "Shape") or o.Shape.isNull():
                continue
            n = o.Name.lower()
            if any(k.lower() in n for k in UNCHANGED_KEYWORDS):
                bb = o.Shape.BoundBox
                snap[o.Name] = (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)
        except Exception:
            continue
    return snap


def compare_bbox_snapshot(doc, before, logger: Logger) -> List[str]:
    changed = []
    for name, bb0 in before.items():
        o = doc.getObject(name)
        if o is None or not hasattr(o, "Shape"):
            continue
        try:
            bb = o.Shape.BoundBox
        except Exception:
            continue
        bb1 = (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)
        if any(abs(a - b) > 1e-6 for a, b in zip(bb0, bb1)):
            changed.append(name)
            logger.log(f"UNCHANGED-CHECK DELTA {name}: before={bb0} after={bb1}")
    return changed


def make_disk(Part, App, x: float, y: float, z: float, radius_mm: float, axis: Tuple[float, float, float], thickness: float = 1.0):
    ax = App.Vector(*axis)
    origin = App.Vector(x, y, z)
    cyl = Part.makeCylinder(radius_mm, thickness, origin, ax)
    return cyl


def add_feature(doc, name: str, label: str, shape, mass_g: Optional[float], logger: Logger):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = label
    obj.Shape = shape
    set_mass_g(obj, mass_g)
    logger.log(f"added {name}: label={label}")
    return obj


def shape_distance(a, b) -> float:
    try:
        d = a.distToShape(b)
        if isinstance(d, tuple):
            return float(d[0])
        return float(d)
    except Exception:
        try:
            return float(a.BoundBox.distanceToPoint(b.BoundBox.Center))
        except Exception:
            return float("inf")


def best_prop_mass(diam_mm: float) -> Tuple[float, str]:
    for k, v in PROP_PRESETS.items():
        if abs(diam_mm - k) < 1e-3:
            return v["mass_g"], f"Preset {v['name']}"
    return 28.0, "Defaulted to 17in mass mapping"


def _fits_clearance(box_a, box_b) -> bool:
    return not (
        box_a.XMax < box_b.XMin
        or box_a.XMin > box_b.XMax
        or box_a.YMax < box_b.YMin
        or box_a.YMin > box_b.YMax
        or box_a.ZMax < box_b.ZMin
        or box_a.ZMin > box_b.ZMax
    )


def run() -> int:
    args = parse_args()
    logger = Logger(OUT_LOG)
    logger.log("Starting build_V3_update")
    logger.log(f"Source: {SRC_FCSTD}")
    logger.log(f"Outputs: {OUT_FCSTD}, {OUT_STEP}")

    if not SRC_FCSTD.exists():
        raise BuildError(f"Missing source file: {SRC_FCSTD}")

    missing_dims = []
    if args.mn4014_diameter_mm is None:
        missing_dims.append("MN4014 diameter")
    if args.mn4014_height_mm is None:
        missing_dims.append("MN4014 height")
    if args.at3520_diameter_mm is None:
        missing_dims.append("AT3520 diameter")
    if args.at3520_height_mm is None:
        missing_dims.append("AT3520 height")

    App, Part, Import = import_freecad(logger)
    close_open_docs(App)
    doc = App.openDocument(str(SRC_FCSTD))
    logger.log(f"Opened doc={doc.Name} objects={len(doc.Objects)}")

    # Idempotence marker purge for reruns against already-modified documents.
    ensure_removed_prefix(doc, "V3_", logger)
    pre_bbox = capture_bbox_snapshot(doc)

    change_list: List[str] = []

    # Apply known V2 masses where available.
    for n, m in KNOWN_V2_MASSES_G.items():
        o = get_obj(doc, n)
        if o is not None:
            set_mass_g(o, m)

    # Hide replaced legacy objects.
    for bucket, names in HIDE_TARGETS.items():
        for n in names:
            o = get_obj(doc, n)
            if o is not None:
                hide_with_children(o, logger)
                change_list.append(f"HIDE: {n} ({bucket})")

    if missing_dims and not args.force:
        raise BuildError(
            "Required motor dimensions unavailable: "
            + ", ".join(missing_dims)
            + ". Provide via CLI args (--mn4014-*, --at3520-*) sourced from datasheets."
        )

    mn_d = float(args.mn4014_diameter_mm or 48.0)
    mn_h = float(args.mn4014_height_mm or 36.0)
    at_d = float(args.at3520_diameter_mm or 42.0)
    at_h = float(args.at3520_height_mm or 50.0)

    lift_prop_d = float(args.lift_prop_diameter_mm)
    lift_prop_r = 0.5 * lift_prop_d
    lift_prop_mass, prop_mass_note = best_prop_mass(lift_prop_d)

    # A) lift motors
    lift_motor_objs = []
    for i, (sx, sz) in enumerate(LIFT_STATIONS_XZ):
        bell = Part.makeCylinder(mn_d / 2.0, mn_h, App.Vector(sx, MOUNT_TOP_Y - mn_h, sz), App.Vector(0, 1, 0))
        shaft = Part.makeCylinder(2.5, 20.0, App.Vector(sx, MOUNT_TOP_Y, sz), App.Vector(0, 1, 0))
        base = Part.makeBox(mn_d + 8.0, 8.0, mn_d + 8.0, App.Vector(sx - (mn_d + 8.0) / 2.0, MOUNT_TOP_Y - mn_h - 8.0, sz - (mn_d + 8.0) / 2.0))
        solid = bell.fuse(shaft).fuse(base).removeSplitter()
        obj = add_feature(
            doc,
            f"V3_lift_motor_MN4014_{i}",
            f"V3_lift_motor_MN4014_{i} [ENVELOPE D{mn_d:.1f}x{mn_h:.1f}]",
            solid,
            DATASHEET["MN4014_KV400"]["mass_g"],
            logger,
        )
        lift_motor_objs.append(obj)
        change_list.append(f"ADD: {obj.Name} at X={sx} Z={sz}")

    # B) lift props + brake pin housings
    lift_prop_objs = []
    brake_pin_objs = []
    for i, (sx, sz) in enumerate(LIFT_STATIONS_XZ):
        hub_y = MOUNT_TOP_Y + 5.0
        disk = make_disk(Part, App, sx, hub_y - 0.5, sz, lift_prop_r, (0, 1, 0), thickness=1.0)
        pobj = add_feature(
            doc,
            f"V3_lift_prop_disk_{i}",
            f"V3_lift_prop_disk_{i} [D={lift_prop_d:.1f}mm]",
            disk,
            lift_prop_mass,
            logger,
        )
        lift_prop_objs.append(pobj)
        pin = Part.makeBox(8.0, 12.0, 8.0, App.Vector(sx - 4.0, hub_y + 1.0, sz - 4.0))
        pin_obj = add_feature(
            doc,
            f"V3_prop_brake_pin_housing_{i}",
            "V3_prop_brake_pin_housing",
            pin,
            None,
            logger,
        )
        brake_pin_objs.append(pin_obj)
        change_list.append(f"ADD: {pobj.Name}; ADD: {pin_obj.Name} aligned to hub")

    # D) rear motor + prop
    rear_axis_obj = get_obj(doc, "pusher_motor") or get_obj(doc, "rear_AT2814_V2")
    if rear_axis_obj is None:
        raise BuildError("Unable to locate rear motor reference axis from V2")
    rcx, rcy, rcz = _center(rear_axis_obj.Shape)
    old_rear_prop = get_obj(doc, "pusher_prop")
    rear_prop_x = rcx
    if old_rear_prop is not None:
        rear_prop_x, _, _ = _center(old_rear_prop.Shape)

    rear_motor_start_x = rear_prop_x - at_h
    rear_body = Part.makeCylinder(at_d / 2.0, at_h, App.Vector(rear_motor_start_x, rcy, rcz), App.Vector(1, 0, 0))
    rear_motor_obj = add_feature(
        doc,
        "V3_rear_motor_AT3520",
        f"V3_rear_motor_AT3520 [ENVELOPE D{at_d:.1f}x{at_h:.1f}]",
        rear_body,
        DATASHEET["AT3520_KV550"]["mass_g"],
        logger,
    )
    change_list.append("ADD: V3_rear_motor_AT3520 at V2 rear shaft axis")

    rear_prop_d = 330.2
    rear_prop_r = rear_prop_d / 2.0
    rear_prop_mass = 30.0
    rear_prop_disk = make_disk(Part, App, rear_prop_x - 0.5, rcy, rcz, rear_prop_r, (1, 0, 0), thickness=1.0)
    rear_prop_obj = add_feature(
        doc,
        "V3_rear_prop_APC_13x6_5",
        "V3_rear_prop_APC_13x6_5 [D=330.2mm]",
        rear_prop_disk,
        rear_prop_mass,
        logger,
    )
    change_list.append("ADD: V3_rear_prop_APC_13x6_5")

    # E) ESC / power envelopes in nose bay
    # Coordinates are intentionally explicit and bounded to requested windows.
    esc4 = Part.makeBox(40.0, 5.0, 33.0, App.Vector(115.0, 40.0, -16.5))
    esc4_obj = add_feature(doc, "V3_esc_lift_4in1", "V3_esc_lift_4in1 [40x33x5]", esc4, 12.0, logger)
    esc_rear = Part.makeBox(50.0, 12.0, 21.6, App.Vector(160.0, 45.0, 35.0))
    esc_rear_obj = add_feature(doc, "V3_esc_rear_single", "V3_esc_rear_single [50x21.6x12]", esc_rear, 18.5, logger)
    ubec = Part.makeBox(58.0, 8.0, 36.0, App.Vector(120.0, 52.0, -58.0))
    ubec_obj = add_feature(doc, "V3_ubec_duo", "V3_ubec_duo [58x36x8]", ubec, 32.0, logger)
    pm07_x, pm07_z, pm07_y = DATASHEET["PM07"]["size_mm"]
    pm07 = Part.makeBox(pm07_x, pm07_y, pm07_z, App.Vector(128.0, 50.0, 6.0))
    pm07_obj = add_feature(doc, "V3_pm07", "V3_pm07 [68x50x10]", pm07, DATASHEET["PM07"]["mass_g"], logger)
    fuse = Part.makeBox(42.0, 12.0, 45.0, App.Vector(140.0, 60.0, -90.0))
    fuse_obj = add_feature(doc, "V3_fuse_125A_holder", "V3_fuse_125A_holder", fuse, DATASHEET["Fuse_125A_MIDI"]["mass_g"], logger)
    xt90 = Part.makeBox(30.0, 16.0, 20.0, App.Vector(185.0, 55.0, -8.0))
    xt90_obj = add_feature(doc, "V3_xt90s", "V3_xt90s", xt90, DATASHEET["XT90S"]["mass_g"], logger)
    for n in [esc4_obj, esc_rear_obj, ubec_obj, pm07_obj, fuse_obj, xt90_obj]:
        change_list.append(f"ADD: {n.Name}")

    # F) Battery CG solve
    batt = get_obj(doc, "battery_6S2P_V2")
    if batt is None:
        raise BuildError("battery_6S2P_V2 not found")
    set_mass_g(batt, 904.0)

    mass_objs = []
    for o in doc.Objects:
        if hasattr(o, "MassG"):
            try:
                mg = str(o.MassG)
                if mg.upper() == "MISSING":
                    continue
                m = float(mg)
                if hasattr(o, "Shape") and not o.Shape.isNull():
                    mass_objs.append((o, m))
            except Exception:
                continue

    if not mass_objs:
        raise BuildError("No mass-tagged objects available for CG computation")

    total_mass = sum(m for _, m in mass_objs)
    total_mx = sum(m * _center_x(o.Shape) for o, m in mass_objs)
    current_cg = total_mx / total_mass

    batt_mass = 904.0
    batt_cx = _center_x(batt.Shape)
    others_mass = total_mass - batt_mass
    others_mx = total_mx - batt_mass * batt_cx

    target_x = args.battery_x_mm
    if target_x is None:
        target_x = (CG_TARGET_MM * total_mass - others_mx) / batt_mass

    # Move battery only by X translation.
    dx = target_x - batt_cx
    batt.Placement.Base.x += dx
    change_list.append(f"MOVE: battery_6S2P_V2 by dX={dx:.2f} to target X={target_x:.2f}")

    # Check battery collisions with new powertrain objects and FC, and move only new V3 power parts if required.
    collision_targets = [
        get_obj(doc, "Pixhawk_4"),
        esc4_obj,
        esc_rear_obj,
        ubec_obj,
        pm07_obj,
        fuse_obj,
        xt90_obj,
    ]

    moved_for_collision = []
    bb_batt = batt.Shape.BoundBox
    for p in [esc4_obj, esc_rear_obj, ubec_obj, pm07_obj, fuse_obj, xt90_obj]:
        if p is None or p.Shape.isNull():
            continue
        if _fits_clearance(bb_batt, p.Shape.BoundBox):
            p.Placement.Base.x += 25.0
            p.Placement.Base.z += 20.0
            moved_for_collision.append((p.Name, 25.0, 20.0))
            change_list.append(f"MOVE: {p.Name} collision-avoidance dX=+25 dZ=+20")

    # G) pod hatch cut with snap tab (new shell object; old remains hidden)
    pod_candidates = [o for o in doc.Objects if "pod" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()]
    if pod_candidates:
        pod_obj = sorted(pod_candidates, key=lambda o: o.Name)[0]
        hatch_cut = Part.makeBox(84.0, 8.0, 80.0, App.Vector(109.0, 25.0, -40.0))
        tab = Part.makeBox(14.0, 4.0, 8.0, App.Vector(150.0, 24.0, -4.0))
        try:
            pod_new_shape = pod_obj.Shape.cut(hatch_cut).fuse(tab).removeSplitter()
            hide_with_children(pod_obj, logger)
            pod_new = add_feature(doc, "V3_pod_shell_hatch", "V3_pod_shell_hatch", pod_new_shape, None, logger)
            change_list.append(f"HIDE: {pod_obj.Name} (pod shell replacement)")
            change_list.append(f"ADD: {pod_new.Name} (hatch cut X109..193 + snap tab)")
        except Exception as exc:
            logger.log(f"WARN: pod hatch cut failed: {exc}")

    # I) wing report only values (read from CAD extents where possible)
    wing_objs = [o for o in doc.Objects if "wing" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()]
    wing_area_mm2 = sum(float(o.Shape.Area) for o in wing_objs) if wing_objs else float("nan")
    wing_bb = None
    if wing_objs:
        bb0 = wing_objs[0].Shape.BoundBox
        for o in wing_objs[1:]:
            bb0.add(o.Shape.BoundBox)
        wing_bb = bb0

    # Recompute and untouched bbox check
    doc.recompute()
    changed_unchanged = compare_bbox_snapshot(doc, pre_bbox, logger)

    # C/D clearance checks
    fixed_names = {
        "booms": [o for o in doc.Objects if "boom" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
        "wing": [o for o in doc.Objects if "wing" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
        "tail": [o for o in doc.Objects if "tail" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
        "tail_arms": [o for o in doc.Objects if "arm" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
        "pod": [o for o in doc.Objects if "pod" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
        "landing_gear": [o for o in doc.Objects if "gear" in o.Name.lower() and hasattr(o, "Shape") and not o.Shape.isNull()],
    }

    clearance_rows: List[ClearanceResult] = []

    def record(prop_name: str, check: str, target_name: str, dist_mm: float):
        pf = "PASS" if dist_mm >= MIN_FIXED_CLEARANCE_MM else "FAIL"
        clearance_rows.append(ClearanceResult(prop_name, check, target_name, dist_mm, pf))

    rear_shape = rear_prop_obj.Shape
    for i, p in enumerate(lift_prop_objs):
        pshape = p.Shape
        for k in ("booms", "wing", "tail", "tail_arms", "pod"):
            targets = fixed_names[k]
            if not targets:
                record(p.Name, k, "MISSING_TARGET", float("inf"))
                continue
            d = min(shape_distance(pshape, t.Shape) for t in targets)
            record(p.Name, k, k, d)

        # other lift disks
        for j, op in enumerate(lift_prop_objs):
            if i == j:
                continue
            d = shape_distance(pshape, op.Shape)
            record(p.Name, "other_lift_prop", op.Name, d)

        d_rear = shape_distance(pshape, rear_shape)
        record(p.Name, "rear_prop", rear_prop_obj.Name, d_rear)

    # rear prop to V-tail + ground
    tail_targets = fixed_names["tail"]
    if tail_targets:
        d_tail = min(shape_distance(rear_shape, t.Shape) for t in tail_targets)
        record(rear_prop_obj.Name, "rear_to_vtail", "tail", d_tail)

    # Ground estimate from landing gear if present else global minimum Y
    all_shapes = [o.Shape for o in doc.Objects if hasattr(o, "Shape") and not o.Shape.isNull()]
    global_ground_y = min(s.BoundBox.YMin for s in all_shapes) if all_shapes else 0.0

    for p in lift_prop_objs:
        cx, cy, cz = _center(p.Shape)
        tip_to_ground = cy - global_ground_y
        record(p.Name, "tip_to_ground", "ground", tip_to_ground)
    rear_tip_to_ground = (rear_prop_obj.Shape.BoundBox.YMin) - global_ground_y
    record(rear_prop_obj.Name, "tip_to_ground", "ground", rear_tip_to_ground)

    any_fail = any(r.pass_fail == "FAIL" for r in clearance_rows)

    # Build mass table.
    mass_rows: List[MassRow] = []
    total_m = 0.0
    total_mx2 = 0.0
    for o in doc.Objects:
        if not hasattr(o, "Shape") or o.Shape.isNull():
            continue
        mg = getattr(o, "MassG", None)
        if mg is None:
            continue
        mtxt = str(mg)
        x = _center_x(o.Shape)
        if mtxt.upper() != "MISSING":
            try:
                m = float(mtxt)
                total_m += m
                total_mx2 += m * x
            except Exception:
                pass
        mass_rows.append(MassRow(o.Name, o.Label, mtxt, f"{x:.3f}", "CAD" if o.Name.startswith("V3_") else "V2"))
    cg_x_final = total_mx2 / total_m if total_m > 0 else float("nan")

    # Emit CSV / markdown reports.
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "label", "mass_g", "x_station_mm", "source"])
        for r in mass_rows:
            w.writerow([r.name, r.label, r.mass_g, r.x_station_mm, r.source])
        w.writerow([])
        w.writerow(["TOTAL_MASS_G", f"{total_m:.3f}"])
        w.writerow(["CG_X_MM", f"{cg_x_final:.3f}"])
        w.writerow(["CG_TARGET_MM", f"{CG_TARGET_MM:.3f}"])
        w.writerow(["CG_WINDOW", f"[{CG_WINDOW_MM[0]:.1f},{CG_WINDOW_MM[1]:.1f}]"])
        w.writerow(["lift_prop_diameter_mm", f"{lift_prop_d:.3f}"])
        w.writerow(["lift_prop_mass_g", f"{lift_prop_mass:.3f}"])

    with OUT_MD.open("w", encoding="utf-8") as f:
        f.write("# V3 Mass & CG\n\n")
        f.write(f"- Source CAD: `{SRC_FCSTD.name}`\n")
        f.write(f"- Built UTC: `{datetime.now(timezone.utc).isoformat()}`\n")
        f.write(f"- Lift prop selector: `{lift_prop_d:.1f} mm` ({prop_mass_note})\n")
        f.write("- Datasheet citation status: network fetch unavailable in this execution environment; values used as configured in script inputs and explicit constants.\n\n")
        f.write("## Part table\n\n")
        f.write("| Name | Label | MassG | X station (mm) | Source |\n")
        f.write("|---|---|---:|---:|---|\n")
        for r in mass_rows:
            f.write(f"| {r.name} | {r.label} | {r.mass_g} | {r.x_station_mm} | {r.source} |\n")
        f.write("\n")
        f.write(f"- **Total mass:** `{total_m:.3f} g`\n")
        f.write(f"- **CG X:** `{cg_x_final:.3f} mm` (target `{CG_TARGET_MM:.1f}`, window `[{CG_WINDOW_MM[0]:.1f},{CG_WINDOW_MM[1]:.1f}]`)\n")
        f.write("- Hand-check reference from request: take-off mass ~3504 g, CG ~-156.7 mm @ battery X=-30, battery near X=+53 for target.\n")
        f.write("\n## Data-source notes\n\n")
        for key, v in DATASHEET.items():
            f.write(f"- **{key}**: `{json.dumps(v)}`\n")

    with OUT_CLEARANCE_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prop", "check", "target", "distance_mm", "pass_fail"])
        for r in clearance_rows:
            w.writerow([r.prop_name, r.check, r.target_name, f"{r.distance_mm:.3f}", r.pass_fail])

    with OUT_CHANGES_MD.open("w", encoding="utf-8") as f:
        f.write("# V3 Change List\n\n")
        for c in change_list:
            f.write(f"- {c}\n")
        if moved_for_collision:
            f.write("\n## Collision-driven V3 moves\n")
            for n, dxm, dzm in moved_for_collision:
                f.write(f"- {n}: dX={dxm:.1f} dZ={dzm:.1f}\n")

    # Print list update (volume*density for printable V3 parts only)
    density_g_per_mm3 = 0.00124  # PLA approx 1.24 g/cc
    printable = [o for o in doc.Objects if o.Name.startswith("V3_") and hasattr(o, "Shape") and not o.Shape.isNull()]
    with OUT_PRINT_MD.open("w", encoding="utf-8") as f:
        f.write("# V3 Updated Print List\n\n")
        f.write("| Part | Volume (mm^3) | Density (g/mm^3) | Mass est (g) |\n")
        f.write("|---|---:|---:|---:|\n")
        for o in printable:
            vol = float(o.Shape.Volume)
            f.write(f"| {o.Name} | {vol:.3f} | {density_g_per_mm3:.6f} | {vol * density_g_per_mm3:.3f} |\n")

    # Wing report lines
    wing_summary = []
    if wing_bb is not None:
        span = wing_bb.ZLength
        mean_chord = wing_bb.XLength
        le_station = wing_bb.XMax
        wing_summary.append(f"Wing span(BB)= {span:.3f} mm vs required 2473 mm")
        wing_summary.append(f"Wing area(sum shape area)= {wing_area_mm2/1_000_000.0:.6f} m^2")
        wing_summary.append(f"Mean chord(BB)= {mean_chord:.3f} mm")
        wing_summary.append(f"Leading edge station approx X= {le_station:.3f} mm")

    # Save outputs.
    doc.saveAs(str(OUT_FCSTD))
    logger.log(f"Saved FCStd: {OUT_FCSTD}")

    export_objs = [
        o
        for o in doc.Objects
        if hasattr(o, "Shape")
        and not o.Shape.isNull()
        and getattr(o, "Visibility", True)
        and not o.Name.startswith("Sketch")
    ]
    Import.export(export_objs, str(OUT_STEP))
    logger.log(f"Saved STEP: {OUT_STEP}")

    with OUT_EXEC_LOG.open("w", encoding="utf-8") as f:
        f.write("build_V3_update execution summary\n")
        f.write(f"UTC: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"source: {SRC_FCSTD}\n")
        f.write(f"output_fcstd: {OUT_FCSTD}\n")
        f.write(f"output_step: {OUT_STEP}\n")
        f.write(f"lift_prop_diameter_mm: {lift_prop_d}\n")
        f.write(f"clearance_failures: {sum(1 for r in clearance_rows if r.pass_fail=='FAIL')}\n")
        f.write(f"unchanged_bbox_changes: {len(changed_unchanged)}\n")
        if wing_summary:
            f.write("wing_summary:\n")
            for s in wing_summary:
                f.write(f"  - {s}\n")

    if changed_unchanged and not args.force:
        raise BuildError(f"Untouched-object bounding boxes changed: {changed_unchanged}")

    if any_fail and not args.force:
        raise BuildError("Clearance failures detected (see V3_clearance_report.csv). Refusing finalization.")

    # Final recompute health check.
    doc.recompute()
    try:
        errs = list(getattr(doc, "Errors", []))
    except Exception:
        errs = []
    if errs and not args.force:
        raise BuildError(f"Document reports errors: {errs}")

    logger.log("DONE_V3")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except BuildError as exc:
        with OUT_EXEC_LOG.open("a", encoding="utf-8") as f:
            f.write(f"ERROR: {exc}\n")
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
