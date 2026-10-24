# Run INSIDE FreeCAD GUI: View -> Panels -> Python console -> paste entire file -> Enter
# Requires vtol.STEP already open (doc name doesn't matter). Creates screenshots + prints measurements.
import os, FreeCAD, FreeCADGui
doc = FreeCAD.ActiveDocument
if doc is None:
    raise SystemExit("No document open. Open vtol.STEP first.")

out_dir = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\screenshots"
os.makedirs(out_dir, exist_ok=True)

# 1) Isolate tilt cluster
wanted_keywords = ["hingeback","servohinge","hinge1","hinge2","rodhinge","tiltservo","mg90s","servo, metal"]
# hide all
for o in doc.Objects:
    try: o.Visibility = False
    except: pass
shown = []
for o in doc.Objects:
    lab = o.Label.lower()
    if any(k in lab for k in wanted_keywords) or o.Label.lower() in ["rod","rod001"]:
        try:
            o.Visibility = True
            shown.append(o.Label)
        except: pass
# also force rods visible
for name in ["rod","rod001"]:
    obj = doc.getObject(name)
    if obj:
        try: obj.Visibility = True; shown.append(name)
        except: pass
print(f"Visible tilt objects: {shown}")
FreeCADGui.SendMsgToActiveView("ViewFit")
FreeCADGui.activeDocument().activeView().viewIsometric()

# 2) Auto-measure: find cylindrical faces, report diameters per part
def is_cyl_face(f):
    try:
        s = f.Surface
        return "Cylinder" in s.TypeId or "Cylinder" in str(type(s))
    except: return False

print("\n=== AUTO BORE MEASUREMENTS (mm) ===")
for o in doc.Objects:
    if not getattr(o, "Visibility", False): continue
    if o.TypeId != "Part::Feature": continue
    try:
        sh = o.Shape
        cyls = []
        for f in sh.Faces:
            if is_cyl_face(f):
                try: cyls.append(round(f.Surface.Radius*2, 3))
                except: pass
        cyls = sorted(set(cyls))
        bb = sh.BoundBox
        print(f"{o.Label:30s} bbox {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm  vol {sh.Volume:.0f} mm3  cyl-diameters {cyls}")
    except Exception as e:
        print(f"{o.Label} ERR {e}")

# 3) Screenshots (no manual clicking)
view = FreeCADGui.ActiveDocument.activeView()
# isometric
view.viewIsometric(); FreeCADGui.SendMsgToActiveView("ViewFit")
view.saveImage(os.path.join(out_dir, "tilt_iso.png"), 1920, 1080, "White")
print("Saved tilt_iso.png")
# front (side)
view.viewFront(); FreeCADGui.SendMsgToActiveView("ViewFit")
view.saveImage(os.path.join(out_dir, "tilt_side.png"), 1920, 1080, "White")
print("Saved tilt_side.png")
# top
view.viewTop(); FreeCADGui.SendMsgToActiveView("ViewFit")
view.saveImage(os.path.join(out_dir, "tilt_top.png"), 1920, 1080, "White")
print("Saved tilt_top.png")
# restore isometric
view.viewIsometric(); FreeCADGui.SendMsgToActiveView("ViewFit")
print(f"\nDone. Check {out_dir}")
