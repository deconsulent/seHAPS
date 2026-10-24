"""Replace main wing (ASSEm) in V1_2_FIXED with 5-deg dihedral wing.
Run: freecadcmd.exe replace_wing_5deg.py
Input : .../VTOL Steps/V1_2_FIXED.FCStd
Output: .../VTOL Steps/V1_2_FIXED_5DEG.FCStd + STEP + STL + log
Wing axes in V1_2: X=chord/fore-aft(+X fwd), Y=vertical, Z=span.
Old wing ASSEm bbox: X[-370,-46] chord 323.7, Y[22,137], Z[-1236,1236] span 2473.
New wing: same chord/span, MH32-ish airfoil, 5 deg dihedral, root at old centre.
"""
import os, sys, math, traceback

SRC = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\V1_2_FIXED.FCStd"
OUTDIR = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps"
OUT_FCSTD = os.path.join(OUTDIR, "V1_2_FIXED_5DEG.FCStd")
OUT_STEP_FULL = os.path.join(OUTDIR, "V1_2_FIXED_5DEG.STEP")
OUT_STEP_WING = os.path.join(OUTDIR, "wing_5deg_only.STEP")
OUT_STL_WING = os.path.join(OUTDIR, "wing_5deg_only.stl")
LOG = os.path.join(OUTDIR, "wing_5deg_replace.log")

DIH = 5.0  # deg, per request

def log(m):
    print(m, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(m + "\n")
    except Exception:
        pass

try:
    os.remove(LOG)
except OSError:
    pass

import FreeCAD as App
import Part

for n in list(App.listDocuments().keys()):
    try:
        App.closeDocument(n)
    except Exception:
        pass

doc = App.openDocument(SRC)
log(f"opened {doc.Name} label={doc.Label} objects={len(doc.Objects)}")

# --- locate wing assembly ---
assm = None
for o in doc.Objects:
    if o.Name == "ASSEm" or o.Label == "ASSEm":
        assm = o
        break
if assm is None:
    log("FATAL: ASSEm not found")
    sys.exit(1)
log(f"ASSEm type={assm.TypeId} placement={assm.Placement}")

# old wing bbox via Shape (compound of placed children)
try:
    obb = assm.Shape.BoundBox
    log(f"old wing bbox X[{obb.XMin:.1f},{obb.XMax:.1f}] dx={obb.XLength:.1f} "
        f"Y[{obb.YMin:.1f},{obb.YMax:.1f}] dy={obb.YLength:.1f} "
        f"Z[{obb.ZMin:.1f},{obb.ZMax:.1f}] dz={obb.ZLength:.1f} vol={assm.Shape.Volume:.0f}")
    CHORD = obb.XLength
    SPAN = obb.ZLength
    XC_MIN, XC_MAX = obb.XMin, obb.XMax
    YC = (obb.YMin + obb.YMax) / 2.0
    ZC = (obb.ZMin + obb.ZMax) / 2.0
except Exception as e:
    log(f"bbox via Shape failed ({e}), using measured defaults")
    CHORD, SPAN = 323.7, 2473.0
    XC_MIN, XC_MAX = -370.0, -46.0
    YC, ZC = 79.5, 0.0

LE_X = XC_MAX  # leading edge forward (+X)
log(f"CHORD={CHORD:.2f} SPAN={SPAN:.2f} LE_X={LE_X:.2f} YC={YC:.2f} ZC={ZC:.2f}")

HALF = SPAN / 2.0
TIP_RISE = HALF * math.sin(math.radians(DIH))
SPAN_PROJ = HALF * math.cos(math.radians(DIH))
log(f"DIH={DIH}deg HALF={HALF:.1f} tip_rise={TIP_RISE:.1f} half_proj={SPAN_PROJ:.1f}")

# --- airfoil (MH32-ish, same formula as airframe_v1.py), chord along -X, thickness along Y ---
pts = []
N = 24
for i in range(N):
    t = i / (N - 1)
    x = -t * CHORD  # LE at 0, TE at -CHORD
    cam = 0.059 * CHORD * (4 * t * (1 - t))
    th = 0.086 * CHORD * 4 * (t * (1 - t)) ** 0.5
    pts.append((x, cam + th / 2 - CHORD * 0.02))
for i in range(N - 1, -1, -1):
    t = i / (N - 1)
    x = -t * CHORD
    cam = 0.059 * CHORD * (4 * t * (1 - t))
    th = 0.086 * CHORD * 4 * (t * (1 - t)) ** 0.5
    pts.append((x, cam - th / 2 - CHORD * 0.02))

wire = Part.makePolygon([App.Vector(p[0], p[1], 0) for p in pts] + [App.Vector(pts[0][0], pts[0][1], 0)])
try:
    face = Part.Face(wire)
except Exception as e:
    log(f"Face failed: {e}")
    raise
log(f"airfoil face valid={face.isValid()} area={face.Area:.0f}")

# extrude along +Z / -Z then rotate about X for dihedral
# right half (+Z)
solid_R = face.extrude(App.Vector(0, 0, HALF))
solid_R = solid_R.rotated(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -DIH)
# left half (-Z)
solid_L = face.extrude(App.Vector(0, 0, -HALF))
solid_L = solid_L.rotated(App.Vector(0, 0, 0), App.Vector(1, 0, 0), DIH)

log(f"half R bbox dx={solid_R.BoundBox.XLength:.1f} dy={solid_R.BoundBox.YLength:.1f} dz={solid_R.BoundBox.ZLength:.1f}")
log(f"half L bbox dx={solid_L.BoundBox.XLength:.1f} dy={solid_L.BoundBox.YLength:.1f} dz={solid_L.BoundBox.ZLength:.1f}")

wing_local = solid_R.fuse(solid_L)
wing_local = wing_local.removeSplitter()
log(f"fused wing local bbox X[{wing_local.BoundBox.XMin:.1f},{wing_local.BoundBox.XMax:.1f}] "
    f"Y[{wing_local.BoundBox.YMin:.1f},{wing_local.BoundBox.YMax:.1f}] "
    f"Z[{wing_local.BoundBox.ZMin:.1f},{wing_local.BoundBox.ZMax:.1f}] vol={wing_local.Volume:.0f}")

# translate to assembly position: LE at LE_X, mid-thickness at YC, span centred at ZC
# airfoil x in [-CHORD,0], so Tx = LE_X ; y mean ~ +? compute face centre
face_cy = face.BoundBox.YMin + face.BoundBox.YLength / 2.0
Tx, Ty, Tz = LE_X, YC - face_cy, ZC
log(f"face centre y={face_cy:.2f} -> translate ({Tx:.2f},{Ty:.2f},{Tz:.2f})")
wing = wing_local.copy()
wing.translate(App.Vector(Tx, Ty, Tz))
log(f"placed wing bbox X[{wing.BoundBox.XMin:.1f},{wing.BoundBox.XMax:.1f}] "
    f"Y[{wing.BoundBox.YMin:.1f},{wing.BoundBox.YMax:.1f}] "
    f"Z[{wing.BoundBox.ZMin:.1f},{wing.BoundBox.ZMax:.1f}] vol={wing.Volume:.0f}")

# --- spars: 2 per half following dihedral, at 25% and 60% chord ---
spar_shapes = []
for frac, dia in ((0.25, 12.0), (0.60, 10.0)):
    xc = LE_X - frac * CHORD
    for side, ang in ((1, -DIH), (-1, DIH)):
        length = HALF / math.cos(math.radians(DIH)) + 20.0  # slight root overlap
        # cylinder along +Z from root, then rotate
        cyl = Part.makeCylinder(dia / 2.0, length, App.Vector(0, 0, 0 if side > 0 else -length), App.Vector(0, 0, 1 if side > 0 else -1))
        # NOTE: for -Z side built downward then rotated; simpler: build +Z then mirror via rotation 180? Use direct:
        if side < 0:
            # rebuild as +Z then rotate 180 about X? easier: create along -Z then rotate +DIH about origin
            pass
        cyl = cyl.rotated(App.Vector(0, 0, 0), App.Vector(1, 0, 0), ang)
        cyl.translate(App.Vector(xc, YC, ZC))
        spar_shapes.append(cyl)
        log(f"spar frac={frac} side={side:+d} dia={dia} len={length:.0f} bbox dy={cyl.BoundBox.YLength:.1f} dz={cyl.BoundBox.ZLength:.1f}")

# --- insert into document ---
wing_part = doc.addObject("App::Part", "Wing_5deg")
wing_part.Label = "Wing_5deg"
log(f"created {wing_part.Name} label={wing_part.Label}")

wobj = doc.addObject("Part::Feature", "wing_5deg")
wobj.Label = "wing_5deg"
wobj.Shape = wing
wing_part.addObject(wobj)
log(f"added wing solid vol={wing.Volume:.0f}")

for i, s in enumerate(spar_shapes):
    so = doc.addObject("Part::Feature", f"spar_5deg_{i}")
    so.Label = f"spar_5deg_{i}"
    so.Shape = s
    wing_part.addObject(so)
log(f"added {len(spar_shapes)} spars")

# --- hide old wing: remove ASSEm from top assembly + hide ---
try:
    vtol = None
    for o in doc.Objects:
        if o.Name == "vtol" or o.Label == "vtol":
            vtol = o
            break
    if vtol is not None:
        grp = list(vtol.Group)
        log(f"vtol members before={len(grp)}")
        if assm in grp:
            grp.remove(assm)
            vtol.Group = grp
            log("removed ASSEm from vtol.Group")
        if wing_part not in grp:
            grp.append(wing_part)
            vtol.Group = grp
            log("added Wing_5deg to vtol.Group")
        log(f"vtol members after={len(vtol.Group)}")
    else:
        log("WARN: vtol container not found")
except Exception as e:
    log(f"vtol regroup failed: {e}\n{traceback.format_exc()}")

# hide old wing objects (container + members) so renders/exports can filter
try:
    assm.Visibility = False
    log("ASSEm.Visibility=False")
except Exception as e:
    log(f"hide ASSEm fail: {e}")
# hide members
try:
    hidden = 0
    # ASSEm direct members
    for m in getattr(assm, "Group", []):
        try:
            # nested App::Part (Ribs, trailing)
            if m.TypeId == "App::Part":
                try:
                    m.Visibility = False
                except Exception:
                    pass
                for mm in getattr(m, "Group", []):
                    try:
                        mm.Visibility = False
                        hidden += 1
                    except Exception:
                        pass
            else:
                m.Visibility = False
                hidden += 1
        except Exception:
            pass
    log(f"hid {hidden} old-wing sub-objects")
except Exception as e:
    log(f"hide members fail: {e}")

# keep ailerons but tilt them with wing (rotate about X through YC,ZC)
for aname in ("aileron", "aileronright"):
    try:
        apart = None
        for o in doc.Objects:
            if o.Name == aname or o.Label == aname:
                apart = o
                break
        if apart is None:
            log(f"{aname}: not found")
            continue
        # determine side by shape bbox Z centre
        try:
            abb = apart.Shape.BoundBox
            zc = (abb.ZMin + abb.ZMax) / 2.0
            side = 1 if zc > 0 else -1
            ang = -DIH if side > 0 else DIH
            # rotate placement about point (LE_X-CHORD/2, YC, 0): trailing-edge line
            base = App.Vector((XC_MIN + XC_MAX) / 2.0, YC, 0.0)
            # Apply: Placement = Rot(base, X, ang) * old Placement
            rot = App.Placement(base, App.Rotation(App.Vector(1, 0, 0), ang))
            # move to origin-centred, rotate, move back: new = T(base)*R*T(-base)*old
            old_plm = apart.Placement
            # construct by transforming shape? Simpler: adjust Placement via multiply
            # FreeCAD: apart.Placement = rot.multiply(old_plm)? Need T(-base) first.
            # Use: new_plm = App.Placement(base, App.Rotation(X,ang)).multiply(App.Placement(-base, App.Rotation())).multiply(old_plm)
            to_org = App.Placement(App.Vector(-base.x, -base.y, -base.z), App.Rotation())
            back = App.Placement(base, App.Rotation(App.Vector(1, 0, 0), ang))
            apart.Placement = back.multiply(to_org.multiply(old_plm))
            log(f"{aname}: side={side:+d} zc={zc:.0f} rotated {ang:+.1f}deg about Y={YC:.1f} -> new placement {apart.Placement}")
        except Exception as e:
            log(f"{aname} rotate fail: {e}\n{traceback.format_exc()}")
    except Exception as e:
        log(f"{aname} outer fail: {e}")

doc.recompute()
log("recomputed")

# --- save new FCStd ---
try:
    doc.saveAs(OUT_FCSTD)
    log(f"saved FCStd -> {OUT_FCSTD} ({os.path.getsize(OUT_FCSTD)} bytes)")
except Exception as e:
    log(f"saveAs failed: {e}\n{traceback.format_exc()}")
    sys.exit(1)

# --- exports ---
# wing-only STEP/STL
try:
    wing.exportStep(OUT_STEP_WING)
    log(f"wing STEP -> {OUT_STEP_WING} ({os.path.getsize(OUT_STEP_WING)} bytes)")
except Exception as e:
    log(f"wing STEP fail: {e}")
try:
    wing.exportStl(OUT_STL_WING)
    log(f"wing STL -> {OUT_STL_WING} ({os.path.getsize(OUT_STL_WING)} bytes)")
except Exception as e:
    log(f"wing STL fail: {e}")

# full assembly STEP (exclude hidden old wing): collect visible Part::Feature shapes except ASSEm subtree
try:
    # build exclusion set: ASSEm + all nested members
    excl = set()
    def collect(o):
        excl.add(o.Name)
        for m in getattr(o, "Group", []):
            collect(m)
    collect(assm)
    log(f"excluded {len(excl)} old-wing objects from full export")
    shapes = []
    for o in doc.Objects:
        if o.Name in excl:
            continue
        # skip containers themselves (App::Part has no own Shape of interest except compound dup) -> use Part::Feature only
        if o.TypeId == "Part::Feature" and hasattr(o, "Shape"):
            try:
                if o.Shape is None or o.Shape.isNull():
                    continue
                # skip infinite datums
                bb = o.Shape.BoundBox
                if bb.XLength > 1e12:
                    continue
                shapes.append(o.Shape)
            except Exception:
                pass
    log(f"exporting {len(shapes)} solids to full STEP...")
    Part.export(shapes, OUT_STEP_FULL)
    log(f"full STEP -> {OUT_STEP_FULL} ({os.path.getsize(OUT_STEP_FULL)} bytes)")
except Exception as e:
    log(f"full STEP fail: {e}\n{traceback.format_exc()}")

# --- verification: measure new wing angle ---
try:
    bb = wing.BoundBox
    # sample tip vs root: tip rise from geometry -> angle = atan((Ymax-Ycentre)/(Zmax-Zcentre))? Use halves separately
    # right half tip: max Z point should be high Y
    # approximate dihedral from bbox: rise = (Ymax - Ymin)/2? For symmetric V, Ymin at root, Ymax at tips.
    # root Y ~ Ty+face range, tip Y = root + TIP_RISE. So measured rise = Ymax - Yroot. Yroot approx YC+face range min? Use (Ymax - YC).
    rise_meas = bb.YMax - YC
    span_meas = bb.ZMax - ZC
    ang_meas = math.degrees(math.atan2(rise_meas, span_meas))
    log(f"VERIFY new wing bbox dy={bb.YLength:.1f} dz={bb.ZLength:.1f} rise~{rise_meas:.1f} halfspan~{span_meas:.1f} angle~{ang_meas:.2f}deg (target {DIH})")
    log(f"VERIFY old span={SPAN:.1f} new projected dz={bb.ZLength:.1f} (expect {SPAN*math.cos(math.radians(DIH)):.1f})")
except Exception as e:
    log(f"verify fail: {e}")

log("DONE")
