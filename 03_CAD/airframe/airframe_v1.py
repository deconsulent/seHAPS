"""
Baltic Tilt-Rotor V1 -- Full airframe parametric model (DAY 8)
Variants: 1 = FIXED (default, front lift + tail pusher), 2 = TILT (Concept A fronts)
Dims: span 1400, length 900, chord 180, boom 600 O16, V-tail, MH32-ish wing 3deg dihedral
Exports: STEP per variant + STLs to 03_CAD/airframe/exports and STEP
Run: freecadcmd.exe airframe_v1.py
"""
import os, sys
try:
    import FreeCAD as App
    import Part
    try:
        import Import
        HAS_IMPORT = True
    except Exception:
        HAS_IMPORT = False
    DOC = App.newDocument("V1_Airframe")
except Exception as e:
    print("FreeCAD import failed:", e); sys.exit(1)

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "airframe", "exports"))
STEP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "airframe", "STEP"))
# optional override: V1_STEP_DIR -> put the STEP/FCSD into another folder (e.g. Vyan reference)
V1_STEP_DIR = os.environ.get("V1_STEP_DIR")
if V1_STEP_DIR:
    STEP = os.path.normpath(V1_STEP_DIR)
os.makedirs(OUT, exist_ok=True); os.makedirs(STEP, exist_ok=True)

# infer variant from an arg EXCEPT the script path
VARIANT = 1
for a in sys.argv[1:]:
    if a in ("1", "2"):
        VARIANT = int(a)
if "--variant=" in "".join(sys.argv):
    VARIANT = int("".join(sys.argv).split("--variant=")[1][0])

# ---------- params mm ----------
SPAN, CHORD, THK = 1400.0, 180.0, 16.0          # wing span, chord, thickness
DIH = 3.0                                        # dihedral deg
POD_L, POD_H = 340.0, 120.0                      # pod length/height
BOOM_L, BOOM_D = 600.0, 16.0                     # boom
TAIL_PITCH = 55.0                                # v-tail fin length
TAIL_OPEN = 45.0                                 # v-tail dihedral from horiz
TIER = 140.0                                     # vertical offset (landing clearance)
STEP_VET = 1e-3
STEP_DEV = 0.4                                   # linear deflection for STEP

LIFT_MOTOR = 28.0                                # O28 bell (A2212)
PUSHER_D = 28.0
PROP_LIFT = 254.0                                # 10x6 O254
PROP_PUSH = 250.0

def add(name, shape, export=True):
    obj = DOC.addObject("Part::Feature", name)
    obj.Shape = shape
    if export:
        p = os.path.join(OUT, name + ".stl")
        shape.exportStl(p)
    return obj

# ---------- airfoil MH32 approx (rounded, mirrored) ----------
from math import sin, cos, pi, radians
pts = []
for i in range(24):
    t = i / 23.0
    x = t * CHORD
    cam = 0.059 * CHORD * (4 * t * (1 - t))
    th = 0.086 * CHORD * 4 * (t * (1 - t)) ** 0.5
    pts.append((x, cam + th / 2 - CHORD * 0.02))
for i in range(23, -1, -1):
    t = i / 23.0
    x = t * CHORD
    cam = 0.059 * CHORD * (4 * t * (1 - t))
    th = 0.086 * CHORD * 4 * (t * (1 - t)) ** 0.5
    pts.append((x, cam - th / 2 - CHORD * 0.02))
wire = Part.makePolygon([App.Vector(p[0], 0, p[1]) for p in pts] + [App.Vector(pts[0][0], 0, pts[0][1])])
AF = Part.Face(wire)

def wing_half(sign, fused=True):
    z0 = sign * (SPAN / 2) * sin(radians(DIH))          # dihedral rise
    vz = z0 / (SPAN / 2) * 0.0
    # sweep base: flat chord span along X, thickness in Z, dihedral by rotating around X
    solid = AF.extrude(App.Vector(0, SPAN / 2, 0))
    # apply dihedral: rotate tip section -- approximate with simple shear (linear rise)
    # simpler: place wing halves tilted via rotation of wire local coords is complex;
    # emulate 3deg by rotating the whole half around leading-edge axis at root
    rot = Part.Rotation(App.Vector(1, 0, 0), -sign * DIH)
    m = App.Matrix()
    rot.multiply(m)
    solid = solid.transformGeometry(m)
    # reposition so root stays at center
    box = solid.BoundBox
    up = -min(0, box.ZMin)
    solid.translate(App.Vector(0, 0, 0))
    return solid

# build wing: center box + two dihedral halves extruded +/-Y, rotated about X at root
def make_half(sign):
    half = AF.extrude(App.Vector(0, sign * SPAN / 2, 0))
    return half.rotated(App.Vector(0, 0, 0), App.Vector(1, 0, 0), float(sign * DIH))
w_center = AF.extrude(App.Vector(0, 24, 0))               # center section
wing = w_center.fuse(make_half(1)).fuse(make_half(-1))
# halves already span y -700..700; center chord on X so pod sits at mid-chord
wing.Placement = App.Placement(App.Vector(-CHORD / 2, -0*1400.0, TIER), App.Rotation())
wing = wing.removeSplitter()
add("wing", wing)

# ---------- pod ----------
pod = Part.makeBox(POD_L, 62, POD_H, App.Vector(-POD_L / 2, -31, 40))
pod = pod.fuse(Part.makeBox(30, 36, 30, App.Vector(-15, -18, 0)))       # nose block
# mount plate for front motors (fixed) or tilt (alt)
mount = Part.makeBox(24, 36, 8, App.Vector(-12, -18, POD_H - 8))
pod = pod.fuse(mount)
# camera pod
pod = pod.fuse(Part.makeSphere(26, App.Vector(-POD_L / 2 + 60, 0, 48)))
pod = pod.common(pod)  # no-op keep
pod.Placement = App.Placement(App.Vector(0, 0, TIER), App.Rotation())
add("pod", pod)

# ---------- boom ----------
# boom runs AFT along -X from pod x=-170 to x=-770 (600 mm), at wing height
boom_z = TIER + 120
boom = Part.makeCylinder(BOOM_D / 2, BOOM_L, App.Vector(-170, 0, boom_z), App.Vector(-1, 0, 0))
add("boom", boom)

# ---------- V-tail fins (aft on boom, x=-740..-580) ----------
for side in (1, -1):
    # plate vertical (X-Z) 160x55, then rotate about X to open into V (45deg each side)
    fin = Part.makeBox(160, THK, 55, App.Vector(0, -THK / 2, 0))
    fin.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -side * TAIL_OPEN)
    fin.translate(App.Vector(-740, 0, boom_z + 30))
    add(f"vtail_fin_{side}", fin)

# ---------- propulsion (per variant) ----------
def prop_disk(d, x, y, z, axis=(0, 0, 1)):
    return Part.makeCylinder(d / 2, 6, App.Vector(x, y, z), App.Vector(*axis))

if VARIANT == 1:
    # FIXED: two front lift pylons (motors vertical) + rear pusher
    for side in (-1, 1):
        # pylon arm from pod edge (y=36) out to motor (y=170)
        arm = Part.makeBox(14, abs(170 - 36), 22)
        arm.Placement = App.Placement(App.Vector(0, (36 + 170) / 2 * side, TIER + 160), App.Rotation())
        add(f"pylon_fwd_{side}", arm)
        # motor can vertical (fixed up)
        mot = Part.makeCylinder(LIFT_MOTOR / 2, 30, App.Vector(0, side * 170, TIER + 178), App.Vector(0, 0, 1))
        add(f"lift_motor_{side}", mot)
        add(f"lift_prop_{side}", prop_disk(PROP_LIFT, 0, side * 170, TIER + 210))
    # rear pusher (motor + prop) at aft boom end, axis along -X (pusher prop behind)
    pu = boom_z
    add("pusher_motor", Part.makeCylinder(PUSHER_D / 2, 34, App.Vector(-770, 0, pu), App.Vector(-1, 0, 0)))
    add("pusher_prop", prop_disk(PROP_PUSH, -800, 0, pu, axis=(-1, 0, 0)))
else:
    # TILT: Concept A housings + servos, front rotors tilt, no pusher
    for side in (-1, 1):
        # housing sits at pod edge (y=36), shaft tilts outward to motor @170
        # barrel axle along X (fore-aft pivot), motor bell rotates 0-90 in plane
        barrel = Part.makeCylinder(26, 55, App.Vector(-40, side * 103, TIER + 178), App.Vector(1, 0, 0))
        shaft = Part.makeCylinder(5, 70, App.Vector(-40 - 35, side * 103, TIER + 178), App.Vector(1, 0, 0))
        serv = Part.makeBox(40, 20, 28, App.Vector(-62, side * 90, TIER + 195))
        add(f"tilt_housing_{side}", barrel)
        add(f"tilt_servo_{side}", serv)
        add(f"tilt_shaft_{side}", shaft)
        add(f"tilt_motor_{side}", Part.makeCylinder(LIFT_MOTOR / 2, 30, App.Vector(0, side * 170, TIER + 178), App.Vector(0, 0, 1)))
        add(f"tilt_prop_{side}", prop_disk(PROP_LIFT, 0, side * 170, TIER + 210))

# ---------- export ----------
DOC.recompute()
suffix = "_fixed" if VARIANT == 1 else "_tilt"
ass = DOC.findObjects("Part::Feature")
shapes = [o.Shape for o in ass if hasattr(o, "Shape") and o.Shape]
# save project FCStd
fcstd_path = os.path.join(STEP, f"airframe{suffix}.fcstd")
DOC.saveAs(fcstd_path)
print(f"FCStd -> {fcstd_path}")
# STEP export (per-solid list ok)
stp = os.path.join(STEP, f"airframe{suffix}.step")
try:
    Part.export(shapes, stp)
    print(f"STEP -> {stp}")
except Exception as e:
    print("STEP skip:", e)
print(f"Variant {VARIANT}: {len(shapes)} solids, fused OK. STLs -> {OUT}")
# when V1_STEP_DIR set: also write a single fused solid STEP for external viewers
if V1_STEP_DIR:
    fused = shapes[0]
    for s in shapes[1:]:
        fused = fused.fuse(s)
    fused = fused.removeSplitter()
    out1 = os.path.join(STEP, f"V1_FIXED_COMPLETE.STEP")
    try:
        fused.exportStep(out1)
        print(f"FUSED-STEP -> {out1} ({os.path.getsize(out1) if os.path.exists(out1) else 0} bytes)")
    except Exception as e:
        print("fused STEP skip:", e)
    aux = os.path.join(STEP, f"V1_FIXED_COMPLETE.FCStd")
    try:
        doc2 = App.newDocument("V1FixedExport")
        fobj = doc2.addObject("Part::Feature", "complete")
        fobj.Shape = fused
        doc2.recompute()
        doc2.saveAs(aux)
        App.closeDocument("V1FixedExport")
        print(f"FUSED-FCStd -> {aux}")
    except Exception as e:
        print("fused FCStd skip:", e)