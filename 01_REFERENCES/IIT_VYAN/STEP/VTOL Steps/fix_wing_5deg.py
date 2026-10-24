"""Fix V1_2_FIXED_5DEG: correct spars, revert small aileron hinges, tilt full aileron assemblies, re-export STEP.
"""
import os, math
SRC = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\V1_2_FIXED.FCStd"
NEW = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\V1_2_FIXED_5DEG.FCStd"
OUT_STEP_FULL = os.path.join(os.path.dirname(NEW), "V1_2_FIXED_5DEG_FULL.STEP")
LOG = os.path.join(os.path.dirname(NEW), "wing_5deg_fix.log")
DIH = 5.0

def log(m):
    print(m, flush=True)
    try:
        open(LOG, "a", encoding="utf-8").write(m + "\n")
    except Exception:
        pass
try: os.remove(LOG)
except OSError: pass

import FreeCAD as App
import Part

# get original hinge placements to revert
for n in list(App.listDocuments().keys()):
    try: App.closeDocument(n)
    except Exception: pass
sdoc = App.openDocument(SRC)
orig_plm = {}
for name in ("Part__Feature244", "Part__Feature257"):
    for o in sdoc.Objects:
        if o.Name == name:
            orig_plm[name] = App.Placement(o.Placement)
            log(f"orig {name} label={o.Label} plm={o.Placement}")
            break
# full aileron assembly bboxes original
for pname, plabel in (("aileron", "aileron011"), ("aileronright", "aileronright011")):
    for o in sdoc.Objects:
        if o.Name == pname and o.TypeId == "App::Part":
            try:
                bb = o.Shape.BoundBox
                log(f"orig ASSEMBLY {plabel}/{pname} bbox X[{bb.XMin:.0f},{bb.XMax:.0f}] Y[{bb.YMin:.0f},{bb.YMax:.0f}] Z[{bb.ZMin:.0f},{bb.ZMax:.0f}] plm={o.Placement}")
            except Exception as e:
                log(f"orig {pname} bbox fail {e}")
            break
App.closeDocument(sdoc.Name)

for n in list(App.listDocuments().keys()):
    try: App.closeDocument(n)
    except Exception: pass
doc = App.openDocument(NEW)
log(f"opened {doc.Name} objs={len(doc.Objects)}")

# --- remove bad spars ---
wing_part = None
for o in doc.Objects:
    if o.Name == "Wing_5deg":
        wing_part = o
        break
if wing_part is None:
    log("FATAL no Wing_5deg"); raise SystemExit(1)

bad = [o for o in doc.Objects if o.Name.startswith("spar_5deg_")]
log(f"removing {len(bad)} bad spars")
for o in bad:
    try:
        # remove from Wing_5deg group first
        grp = list(wing_part.Group)
        if o in grp:
            grp.remove(o)
            wing_part.Group = grp
        doc.removeObject(o.Name)
    except Exception as e:
        log(f"  rm {o.Name} fail {e}")
doc.recompute()

# wing params from placed wing
wobj = doc.getObject("wing_5deg")
wbb = wobj.Shape.BoundBox
log(f"wing bbox X[{wbb.XMin:.1f},{wbb.XMax:.1f}] Y[{wbb.YMin:.1f},{wbb.YMax:.1f}] Z[{wbb.ZMin:.1f},{wbb.ZMax:.1f}]")
CHORD = wbb.XLength
LE_X = wbb.XMax
YC = 79.54  # original centre (keep)
ZC = 0.0
SPAN = 2472.97
HALF = SPAN/2.0
LEN = HALF / math.cos(math.radians(DIH))
log(f"CHORD={CHORD:.2f} LE={LE_X:.2f} HALF={HALF:.1f} spar_len={LEN:.1f}")

# --- correct spars: base origin, dir +-Z, rotate, translate ---
spars = []
for frac, dia in ((0.25, 12.0), (0.60, 10.0)):
    xc = LE_X - frac*CHORD
    for side, ang in ((1, -DIH), (-1, DIH)):
        direction = App.Vector(0, 0, 1 if side > 0 else -1)
        cyl = Part.makeCylinder(dia/2.0, LEN, App.Vector(0, 0, 0), direction)
        cyl = cyl.rotated(App.Vector(0, 0, 0), App.Vector(1, 0, 0), ang)
        cyl.translate(App.Vector(xc, YC, ZC))
        spars.append((f"spar_5deg_{frac}_{ '+' if side>0 else '-' }", cyl))
        bb = cyl.BoundBox
        log(f"  new spar f={frac} side={side:+d} Z[{bb.ZMin:.0f},{bb.ZMax:.0f}] Y[{bb.YMin:.0f},{bb.YMax:.0f}]")
for name, sh in spars:
    # sanitize name (FreeCAD no + - . )
    sname = name.replace(".", "p").replace("+", "pos").replace("-", "neg")
    so = doc.addObject("Part::Feature", sname)
    so.Label = name
    so.Shape = sh
    wing_part.addObject(so)
log(f"added {len(spars)} corrected spars")
doc.recompute()

# --- revert small hinge features to original placements ---
for fname, plm in orig_plm.items():
    o = doc.getObject(fname)
    if o is not None:
        o.Placement = App.Placement(plm)
        log(f"reverted {fname} to {plm}")
    else:
        log(f"WARN {fname} not found in new doc")

# --- tilt FULL aileron assemblies (App::Part) with wing ---
# Identify by TypeId App::Part and Name aileron / aileronright
for pname in ("aileron", "aileronright"):
    apart = None
    for o in doc.Objects:
        if o.Name == pname and o.TypeId == "App::Part":
            apart = o
            break
    if apart is None:
        log(f"{pname} App::Part not found"); continue
    try:
        bb = apart.Shape.BoundBox
        zc = (bb.ZMin + bb.ZMax)/2.0
        side = 1 if zc > 0 else -1
        ang = -DIH if side > 0 else DIH
        log(f"{pname} pre bbox X[{bb.XMin:.0f},{bb.XMax:.0f}] Y[{bb.YMin:.0f},{bb.YMax:.0f}] Z[{bb.ZMin:.0f},{bb.ZMax:.0f}] zc={zc:.0f} side={side:+d}")
        base = App.Vector((wbb.XMin+wbb.XMax)/2.0, YC, 0.0)
        to_org = App.Placement(App.Vector(-base.x, -base.y, -base.z), App.Rotation())
        back = App.Placement(base, App.Rotation(App.Vector(1, 0, 0), ang))
        apart.Placement = back.multiply(to_org.multiply(apart.Placement))
        bb2 = apart.Shape.BoundBox
        log(f"{pname} post rot {ang:+.1f}deg bbox Y[{bb2.YMin:.0f},{bb2.YMax:.0f}] Z[{bb2.ZMin:.0f},{bb2.ZMax:.0f}] plm={apart.Placement}")
    except Exception as e:
        import traceback
        log(f"{pname} tilt fail {e}\n{traceback.format_exc()}")

doc.recompute()
doc.saveAs(NEW)
log(f"saved {NEW} ({os.path.getsize(NEW)} bytes)")

# --- verify dihedral from single half: use right half tip vs root mid ---
try:
    # root mid Y: sample wing shape at Z~0? Approximate via face centre: YC + cam mean (~12)
    # tip mid Y: YC + cam + TIP_RISE. Use TIP_RISE formula (exact by construction).
    tip_rise = HALF*math.sin(math.radians(DIH))
    ang_exact = DIH
    # measured from halves: take right spar (straight, easy): dy/dz
    sp = doc.getObject("spar_5deg_0p25_pos")
    if sp is None:
        # find first pos spar
        for o in doc.Objects:
            if "spar_5deg" in o.Name and "pos" in o.Name:
                sp = o; break
    bb = sp.Shape.BoundBox
    rise_m = bb.YMax - bb.YMin
    # spar is inclined cylinder: dy = LEN*sin(DIH)+dia, dz = LEN*cos(DIH)
    # subtract dia to get pure rise
    import re
    dia = 12.0
    rise_pure = rise_m - dia
    span_pure = bb.ZMax - bb.ZMin
    ang_m = math.degrees(math.atan2(rise_pure, span_pure))
    log(f"VERIFY spar-based: dy={rise_m:.1f} dz={span_pure:.1f} dia={dia} -> angle={ang_m:.3f}deg (target {DIH})")
    log(f"VERIFY construction: tip_rise={tip_rise:.1f}mm over half-span {HALF:.1f}mm -> {ang_exact}deg exact")
except Exception as e:
    log(f"verify fail {e}")

# --- full STEP export via objects (not shapes) ---
try:
    import Import
    # collect visible feature objects excluding old wing subtree (ASSEm)
    assm = doc.getObject("ASSEm")
    excl = set()
    def collect(o):
        if o is None: return
        excl.add(o.Name)
        for m in getattr(o, "Group", []):
            collect(m)
    if assm: collect(assm)
    log(f"excluding {len(excl)} old-wing objs")
    objs = [o for o in doc.Objects if o.TypeId=="Part::Feature" and o.Name not in excl]
    # filter null/infinite
    good = []
    for o in objs:
        try:
            if o.Shape is None or o.Shape.isNull(): continue
            if o.Shape.BoundBox.XLength > 1e12: continue
            good.append(o)
        except Exception:
            pass
    log(f"exporting {len(good)} Part::Feature objects via Import.export...")
    Import.export(good, OUT_STEP_FULL)
    log(f"full STEP -> {OUT_STEP_FULL} ({os.path.getsize(OUT_STEP_FULL)} bytes)")
except Exception as e:
    import traceback
    log(f"full export fail {e}\n{traceback.format_exc()}")

log("DONE_FIX")
