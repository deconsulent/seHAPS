"""
Render airframe (fixed + tilt) to PNG offscreen.
Usage: freecadcmd.exe render_airframe.py
Needs Qt offscreen platform. Falls back to GUI instructions if unavailable.
"""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import FreeCAD as App
import FreeCADGui as Gui

# Qt application must exist before any view ops
try:
    from PySide2 import QtWidgets
except Exception:
    from PySide import QtWidgets as _q
    QtWidgets = __import__("PySide", fromlist=["QtWidgets"]).QtWidgets
_inst = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

BASE = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\airframe"
OUTDIR = os.path.join(BASE, "render")
os.makedirs(OUTDIR, exist_ok=True)

def render(variant):
    if App.ActiveDocument:
        App.closeDocument(App.ActiveDocument.Name)
    step = os.path.join(BASE, "STEP", f"airframe_{'fixed' if variant == 1 else 'tilt'}.step")
    App.openDocument(step)
    view = Gui.ActiveDocument.ActiveView
    try:
        cam = view.getCameraNode()
        cam.orientation.setValue(0.57735, -0.57735, 0.57735, 2.0944)
        out = os.path.join(OUTDIR, f"airframe_{'f' if variant == 1 else 't'}.png")
        view.saveImage(out, 1600, 1000, "White")
        print("saved", out)
    except Exception as e:
        print("render failed:", e)

try:
    for v in (1, 2):
        render(v)
    print("DONE")
except Exception as e:
    print("OFFSCREEN render unavailable:", type(e).__name__, e)