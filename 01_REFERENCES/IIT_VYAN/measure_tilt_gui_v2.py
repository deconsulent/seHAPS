# v2 fix — previous screenshots were blank white because parent App::Part was hidden.
# Paste: exec(open(r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\measure_tilt_gui_v2.py").read())
import os, time, FreeCAD, FreeCADGui
doc = FreeCAD.ActiveDocument
out_dir = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\screenshots"
os.makedirs(out_dir, exist_ok=True)

wanted_kw = ["hingeback","servohinge","hinge1","hinge2","rodhinge","tiltservo","mg90s","servo, metal"]
# only hide/show Part::Feature — keep App::Part containers visible
for o in doc.Objects:
    if o.TypeId == "Part::Feature":
        try: o.Visibility = False
        except: pass

shown = []
for o in doc.Objects:
    if o.TypeId != "Part::Feature": continue
    lab = o.Label.lower()
    is_wanted = any(k in lab for k in wanted_kw) or lab in ["rod","rod001"]
    if is_wanted:
        try:
            o.ViewObject.Visibility = True  # ViewObject is key
            o.Visibility = True
            shown.append(o.Label)
        except Exception as e: print(e)

# ensure parent Parts are visible
for o in doc.Objects:
    if o.TypeId == "App::Part":
        try: o.Visibility = True
        except: pass

FreeCADGui.updateGui()
print(f"Visible tilt features ({len(shown)}): {shown}")

def is_cyl(f):
    try: return "Cylinder" in f.Surface.TypeId
    except: return False

print("\n=== BORE DIAMETERS (mm) ===")
for o in doc.Objects:
    if o.TypeId != "Part::Feature": continue
    if not getattr(o.ViewObject, "Visibility", False): continue
    sh = o.Shape
    diams = sorted(set(round(f.Surface.Radius*2,3) for f in sh.Faces if is_cyl(f)))
    bb = sh.BoundBox
    print(f"{o.Label:30s} bbox {bb.XLength:.1f}x{bb.YLength:.1f}x{bb.ZLength:.1f}  diams {diams}  vol {sh.Volume:.0f}")

# screenshots with small delay so view renders
view = FreeCADGui.ActiveDocument.activeView()
for name, cmd in [("tilt_iso.png","viewIsometric"),("tilt_side.png","viewFront"),("tilt_top.png","viewTop")]:
    getattr(view, cmd)()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.updateGui()
    time.sleep(0.6)
    path = os.path.join(out_dir, name)
    view.saveImage(path, 1920, 1080, "White")
    sz = os.path.getsize(path)
    print(f"Saved {name} ({sz} bytes)")

view.viewIsometric(); FreeCADGui.SendMsgToActiveView("ViewFit")
print(f"\nDone — check {out_dir}. If still blank/9265 bytes, paste the Report-view lines here.")
