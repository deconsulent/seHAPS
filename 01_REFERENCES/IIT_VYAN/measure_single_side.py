# Optional tight framing — shows only ONE mirrored side so mechanism fills the frame (much larger in image).
# Paste: exec(open(r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\measure_single_side.py").read())
import os, time, FreeCAD, FreeCADGui
doc = FreeCAD.ActiveDocument
out_dir = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\screenshots"
os.makedirs(out_dir, exist_ok=True)
# hide all Part::Feature
for o in doc.Objects:
    if o.TypeId == "Part::Feature":
        try: o.ViewObject.Visibility = False
        except: pass
# show only one side (without 001 suffix) + base parts
keep = ["hingeback","servohinge","hinge1","hinge2","rod","rodhinge","tiltservo","Servo, Metal Gear, MG90S"]
for o in doc.Objects:
    if o.TypeId == "Part::Feature" and o.Label in keep:
        o.ViewObject.Visibility = True
        o.Visibility = True
for o in doc.Objects:
    if o.TypeId == "App::Part":
        try: o.Visibility = True
        except: pass
FreeCADGui.updateGui()
view = FreeCADGui.ActiveDocument.activeView()
for name, cmd in [("tilt_iso_single.png","viewIsometric"),("tilt_side_single.png","viewFront"),("tilt_top_single.png","viewTop")]:
    getattr(view, cmd)(); FreeCADGui.SendMsgToActiveView("ViewFit"); FreeCADGui.updateGui(); time.sleep(0.6)
    p=os.path.join(out_dir,name); view.saveImage(p,1920,1080,"White")
    print(f"Saved {name} ({os.path.getsize(p)} bytes)")
view.viewIsometric(); FreeCADGui.SendMsgToActiveView("ViewFit")
print("Single-side screenshots done — check screenshots folder (expect 60-300KB, 5-15% non-white vs 0.05% before).")
