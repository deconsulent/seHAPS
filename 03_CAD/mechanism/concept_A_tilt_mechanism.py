"""
Concept A — Servo+Pushrod parametric bench rig (DAY 6-7)
Run: FreeCAD GUI Python console exec(open(r".../concept_A_tilt_mechanism.py").read())
     or: freecadcmd.exe concept_A_tilt_mechanism.py
Dims from Vyan GUI-verified: barrel Ø32 inner/Ø55 outer, rod 161→95-110 shortened, hingeback 55 clamp
Exports STLs to ../exports/
"""
import os, sys
try:
    import FreeCAD, Part
    HAS_FC = True
except:
    HAS_FC = False

# params (mm) — edit here
P = dict(
    barrel_outer_d=32.0,  # inner pivot housing actually Ø32; outer printed ~52 — we make 32 ID housing + 52 OD
    barrel_outer_od=52.0,
    barrel_len=55.0,
    shaft_d=10.0,
    bearing_od=24.0,  # 6802
    bearing_w=5.0,
    boom_d=16.0,
    clamp_w=55.0,
    clamp_len=63.0,
    pushrod_len=105.0,  # 95-110
    servo_horn_r=17.5,
    hinge_horn_r=32.0,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(OUT, exist_ok=True)

if not HAS_FC:
    print("FreeCAD not found — writing params only to", OUT)
    open(os.path.join(OUT, "params.txt"), "w").write(str(P))
    sys.exit(0)

doc = FreeCAD.newDocument("ConceptA")
# --- boom clamp (split block 63x55 with Ø16 bore + M3 holes) ---
clamp = Part.makeBox(P["clamp_len"], P["clamp_w"], 30)
# bore along X
cyl = Part.makeCylinder(P["boom_d"]/2, P["clamp_len"], FreeCAD.Vector(0, P["clamp_w"]/2, 15), FreeCAD.Vector(1,0,0))
clamp = clamp.cut(cyl)
# bearing seat in clamp side: Ø24×5 pocket (for 6802 outer)
seat = Part.makeCylinder(P["bearing_od"]/2, P["bearing_w"], FreeCAD.Vector(P["clamp_len"]/2 - P["bearing_w"]/2, P["clamp_w"]/2, 30-P["bearing_w"]), FreeCAD.Vector(1,0,0))
# approximate by Z pocket (simplified — real axis along boom, keep visual)
# hinge barrel (cylinder Ø52×55 with Ø32 bore and Ø10 shaft bore)
barrel = Part.makeCylinder(P["barrel_outer_od"]/2, P["barrel_len"], FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1))
bore = Part.makeCylinder(P["barrel_outer_d"]/2, P["barrel_len"]+2, FreeCAD.Vector(0,0,-1), FreeCAD.Vector(0,0,1))
barrel = barrel.cut(bore)
shaft_bore = Part.makeCylinder(P["shaft_d"]/2, P["barrel_len"]+2, FreeCAD.Vector(0,0,-1), FreeCAD.Vector(0,0,1))
barrel = barrel.cut(shaft_bore)

# servo mount block 45×40×28 with DS3218 pocket 40.5×20×28
servo_mount = Part.makeBox(45, 40, 28)
pocket = Part.makeBox(40.5, 20, 28)
pocket.translate(FreeCAD.Vector(2.25, 10, 0))
servo_mount = servo_mount.cut(pocket)

# bearing test coupon 20×20×10 with Ø24 and Ø10
coupon = Part.makeBox(20, 20, 10)
c1 = Part.makeCylinder(P["bearing_od"]/2, 6, FreeCAD.Vector(10,10,4), FreeCAD.Vector(0,0,1))
c2 = Part.makeCylinder(P["shaft_d"]/2, 11, FreeCAD.Vector(10,10,-1), FreeCAD.Vector(0,0,1))
coupon = coupon.cut(c1).cut(c2)

for name, shape in [("boom_clamp", clamp), ("hinge_barrel", barrel), ("servo_mount", servo_mount), ("bearing_pocket_test", coupon)]:
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    # export STL
    path = os.path.join(OUT, f"{name}.stl")
    shape.exportStl(path)
    print(f"Exported {path}")

doc.recompute()
# optional GUI fit
try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
except:
    pass
print(f"Done — STLs in {OUT}. Params: pushrod {P['pushrod_len']} mm, shaft Ø{P['shaft_d']}, clamp for Ø{P['boom_d']} boom.")
print("Next: slice bearing_pocket_test.stl first (T00), then others per print_list.md")
