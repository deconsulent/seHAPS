"""
Run in FreeCAD GUI console to render both airframe variants to PNG.
Usage: FreeCAD.exe (GUI) -> Python console:
    exec(open(r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\airframe\ss_airframe.py").read())
"""
import os
import FreeCAD as App
import FreeCADGui as Gui

BASE = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\airframe"
OUT = os.path.join(BASE, "render")
os.makedirs(OUT, exist_ok=True)

def set_materials():
    try:
        from PySide2 import QtGui  # or PySide
        g = QtGui.QColor(190, 210, 235)   # light blue body
        m = QtGui.QColor(60, 80, 110)     # dark blue
        mats = {}
        for o in App.ActiveDocument.Objects:
            if o.Name.startswith(("wing", "pod", "boom", "vtail", "pylon")):
                mats[o.Name] = {"DiffuseColor": g}
            else:
                mats[o.Name] = {"DiffuseColor": m}
        Gui.ActiveDocument.activeObject().ViewObject  # ensure
        for name, c in mats.items():
            vo = Gui.ActiveDocument.getObject(name)
            if vo:
                vo.DiffuseColor = [(c["DiffuseColor"].redF(), c["DiffuseColor"].greenF(),
                                    c["DiffuseColor"].blueF(), 1.0)] * 200
    except Exception as e:
        print("mat skip:", e)

def snap(name, iso=True):
    view = Gui.ActiveDocument.ActiveView
    view.viewIsometric()
    view.setCameraOrientation(Gui.ActiveDocument.ActiveView.getCameraOrientation())
    try:
        from pivy import coin
        cam = view.getCameraNode()
        cam.orientation.setValue(0.648, -0.474, 0.596, 2.13)
    except Exception:
        pass
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    view.saveImage(os.path.join(OUT, name), 2000, 1200, "White")
    print("saved", os.path.join(OUT, name))

# close open docs, load both variants
for d in [d for d in App.listDocuments() if d != "Unnamed"]:
    try:
        App.closeDocument(d)
    except Exception:
        pass
for variant, fname in [("fixed", 1), ("tilt", 2)]:
    path = os.path.join(BASE, "STEP", f"airframe_{variant}.fcstd")
    App.openDocument(path)
    set_materials()
    Gui.SendMsgToActiveView("ViewFit")
    App.GuiUp = True
    snap(f"airframe_{'f' if fname == 1 else 't'}.png")
    try:
        App.closeDocument(f"airframe_{variant}")
    except Exception:
        pass
print("DONE")