"""Build V1_2_FIXED_V2: apply final-config deltas to stock flat-wing V1_2_FIXED.
Deltas: 6S2P pack envelope, 4x MN3510 envelopes, AT2814 envelope, 4-in-1 + rear ESC,
hide stock equivalents, mass-weighted CG vs 25-30% chord, save + STEP + report.
Envelope dims are stated assumptions (replace with vendor STEP after purchase).
Axes: X=fore-aft(+fwd), Y=vertical, Z=span.
"""
import os, math
SRC = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\V1_2_FIXED.FCStd"
OUTDIR = os.path.dirname(SRC)
OUT_FCSTD = os.path.join(OUTDIR, "V1_2_FIXED_V2.FCStd")
OUT_STEP = os.path.join(OUTDIR, "V1_2_FIXED_V2_FULL.STEP")
LOG = os.path.join(OUTDIR, "V1_2_V2_build.log")
try: os.remove(LOG)
except OSError: pass

def log(m):
    print(m, flush=True)
    open(LOG, "a", encoding="utf-8").write(m + "\n")

import FreeCAD as App
import Part

for n in list(App.listDocuments().keys()):
    try: App.closeDocument(n)
    except Exception: pass
doc = App.openDocument(SRC)
log(f"opened {doc.Name} objs={len(doc.Objects)}")

def hide(o):
    try: o.Visibility = False
    except Exception: pass

# ---------- 1. Battery: stock 85x45x70 -> 6S2P 132x48x80 envelope ----------
batt = doc.getObject("Part__Feature208")
log(f"stock battery bbox X[{batt.Shape.BoundBox.XMin:.0f},{batt.Shape.BoundBox.XMax:.0f}] Y[{batt.Shape.BoundBox.YMin:.0f},{batt.Shape.BoundBox.YMax:.0f}] Z[{batt.Shape.BoundBox.ZMin:.0f},{batt.Shape.BoundBox.ZMax:.0f}]")
hide(batt)
# 6S2P 21700: 6(X)x2(Z) standing, 21 dia + gaps, H 70 + BMS 10
BATT_L, BATT_W, BATT_H = 132.0, 48.0, 80.0
batt_cx, batt_cy, batt_cz = -197.5, -33.5, 0.0  # same tray station as stock
pack = Part.makeBox(BATT_L, BATT_H, BATT_W,
    App.Vector(batt_cx - BATT_L/2, batt_cy - BATT_H/2, batt_cz - BATT_W/2))
# BMS hump on top
bms = Part.makeBox(60, 12, 30, App.Vector(batt_cx - 30, batt_cy + BATT_H/2, -15))
pack = pack.fuse(bms).removeSplitter()
bo = doc.addObject("Part::Feature", "battery_6S2P_V2")
bo.Label = "battery_6S2P_V2 [ENVELOPE 132x48x80]"
bo.Shape = pack
log(f"new 6S2P pack X[{pack.BoundBox.XMin:.0f},{pack.BoundBox.XMax:.0f}] Y[{pack.BoundBox.YMin:.0f},{pack.BoundBox.YMax:.0f}] Z[{pack.BoundBox.ZMin:.0f},{pack.BoundBox.ZMax:.0f}] vol={pack.Volume:.0f}")

# ---------- 2. Lift motors: hide stock clusters, add MN3510 envelopes ----------
# prop shaft stations (from measured prop placements, axis = Y vertical)
STATIONS = [(488, 405), (493, -405), (-808, 405), (-808, -405)]  # (X, Z)
MN_D, MN_H, MN_SH = 44.0, 36.0, 20.0  # bell dia/h + shaft (ASSUMED envelope)
MOUNT_TOP_Y = 105.0
for pname in ("bldc_motor_Varsayilan", "bldc_motor_Varsayilan001",
              "bldc_motor_Varsayilan002", "bldc_motor_Varsayilan003"):
    for o in doc.Objects:
        if o.Name == pname and o.TypeId == "App::Part":
            try: o.Visibility = False
            except Exception: pass
            for m in getattr(o, "Group", []):
                hide(m)
            log(f"hid cluster {pname} ({len(getattr(o,'Group',[]))} parts)")
            break
mot_part = doc.addObject("App::Part", "LiftMotors_MN3510_V2")
mot_part.Label = "LiftMotors_MN3510_V2"
for i, (sx, sz) in enumerate(STATIONS):
    bell = Part.makeCylinder(MN_D/2, MN_H, App.Vector(sx, MOUNT_TOP_Y - MN_H, sz), App.Vector(0, 1, 0))
    shaft = Part.makeCylinder(5.0/2, MN_SH, App.Vector(sx, MOUNT_TOP_Y, sz), App.Vector(0, 1, 0))
    xring = Part.makeBox(MN_D + 6, 8, MN_D + 6, App.Vector(sx - (MN_D+6)/2, MOUNT_TOP_Y - MN_H - 8, sz - (MN_D+6)/2))
    solid = bell.fuse(shaft).fuse(xring).removeSplitter()
    mo = doc.addObject("Part::Feature", f"lift_MN3510_V2_{i}")
    mo.Label = f"lift_MN3510_V2_{i} [ENVELOPE D44]"
    mo.Shape = solid
    mot_part.addObject(mo)
log(f"added 4x MN3510 envelopes at {STATIONS}")

# ---------- 3. Rear motor: hide stock, add AT2814 envelope ----------
rm = doc.getObject("pusher_motor")
log(f"stock rear motor dx={rm.Shape.BoundBox.XLength:.0f} (38) at X[{rm.Shape.BoundBox.XMin:.0f},{rm.Shape.BoundBox.XMax:.0f}]")
hide(rm)
AT_D, AT_L = 36.0, 34.0  # ASSUMED envelope (stator 28 class)
at = Part.makeCylinder(AT_D/2, AT_L, App.Vector(-610, 0, 0), App.Vector(-1, 0, 0))
ro = doc.addObject("Part::Feature", "rear_AT2814_V2")
ro.Label = "rear_AT2814_V2 [ENVELOPE D36]"
ro.Shape = at
log(f"new AT2814 envelope X[{at.BoundBox.XMin:.0f},{at.BoundBox.XMax:.0f}] dia={AT_D}")

# ---------- 4. ESCs: 4-in-1 45x45 + rear 30A near FC ----------
esc4 = Part.makeBox(45, 12, 45, App.Vector(-60, -64, -22.5))      # beside Pixhawk (X[-91,-7])
escr = Part.makeBox(35, 8, 25, App.Vector(-60, -64, 25))
for nm, sh in (("esc_4in1_45A_V2", esc4), ("esc_rear_30A_V2", escr)):
    o = doc.addObject("Part::Feature", nm)
    o.Label = nm
    o.Shape = sh
    log(f"{nm} X[{sh.BoundBox.XMin:.0f},{sh.BoundBox.XMax:.0f}] Y[{sh.BoundBox.YMin:.0f},{sh.BoundBox.YMax:.0f}]")

doc.recompute()

# ---------- 5. CG: mass-weighted, X axis vs 25-30% chord ----------
LE_X, CHORD = -46.36, 323.66
tgt_lo, tgt_hi = LE_X - 0.30*CHORD, LE_X - 0.25*CHORD
log(f"CG target X in [{tgt_lo:.1f},{tgt_hi:.1f}] (25-30% chord from LE {LE_X})")
# (mass g, X center) — centers from measured bboxes
WING_X = (-370.0 + -46.4)/2
POD_X = (-450 + 354)/2
TAIL_X = (-1465 + 458)/2
items = [
    ("wing_group", 400, WING_X), ("pod_group", 300, POD_X), ("tail_mounts_group", 250, -500),
    ("lift_motors_4", 480, (-808-808+488+493)/4), ("rear_motor", 90, -594),
    ("esc_props_wire", 350, POD_X), ("electronics", 84, -49),
    ("battery_6S2P", 928, batt_cx), ("camera", 120, 5), ("servos_pitot", 180, -336),
]
tot = sum(m for _, m, _ in items)
cgx = sum(m*x for _, m, x in items)/tot
log(f"mass rollup total={tot}g (spec 3108g RS50)")
for n, m, x in items:
    log(f"  {n:18s} {m:4.0f}g @ X={x:7.1f}  dx={(x-cgx):+7.1f} from CG")
log(f"CG_X = {cgx:.1f}  (target [{tgt_lo:.1f},{tgt_hi:.1f}])")
if tgt_lo <= cgx <= tgt_hi:
    log("CG IN RANGE")
else:
    # solve battery X for CG = mid target
    mid = (tgt_lo + tgt_hi)/2
    others = [(m, x) for n, m, x in items if n != "battery_6S2P"]
    m_oth = sum(m for m, _ in others); mx_oth = sum(m*x for m, x in others)
    bx = (mid*tot - mx_oth)/928
    log(f"CG OUT OF RANGE by {cgx-mid:+.1f}mm -> move 6S2P pack to X={bx:.0f} (tray shift {bx-batt_cx:+.0f}mm) for CG={mid:.0f}")
    log(f"tray slot needed: pack half-len 66 + shift -> verify pod bay X[-450,354] fits [{bx-66:.0f},{bx+66:.0f}]")

doc.saveAs(OUT_FCSTD)
log(f"saved {OUT_FCSTD} ({os.path.getsize(OUT_FCSTD)} bytes)")

import Import
old = {"ASSEm"}  # keep ASSEm hidden? No — flat wing KEPT in V2. Exclude only replaced clusters' doubles?
# Export: all visible Part::Feature except hidden stock power parts
hidden_names = {"Part__Feature208", "pusher_motor"}
for pname in ("bldc_motor_Varsayilan", "bldc_motor_Varsayilan001", "bldc_motor_Varsayilan002", "bldc_motor_Varsayilan003"):
    for o in doc.Objects:
        if o.Name == pname and o.TypeId == "App::Part":
            for m in getattr(o, "Group", []):
                hidden_names.add(m.Name)
objs = [o for o in doc.Objects if o.TypeId == "Part::Feature" and o.Name not in hidden_names]
good = []
for o in objs:
    try:
        if o.Shape is None or o.Shape.isNull(): continue
        if o.Shape.BoundBox.XLength > 1e12: continue
        if o.Visibility == False and o.Name.startswith("Part__Feature"): continue
        good.append(o)
    except Exception: pass
log(f"exporting {len(good)} objects...")
Import.export(good, OUT_STEP)
log(f"STEP -> {OUT_STEP} ({os.path.getsize(OUT_STEP)} bytes)")
log("DONE_V2")
