import FreeCAD as App
import FreeCADGui as Gui
import os, sys, traceback

FCSTD = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\V1_FIXED.FCStd"
OUTDIR = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\STEP\VTOL Steps\render"
LOG = os.path.join(OUTDIR, "render.log")
os.makedirs(OUTDIR, exist_ok=True)

def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(m + "\n")
    print(m, flush=True)

try:
    os.remove(LOG)
except OSError:
    pass

W, H = 1500, 1100

try:
    for name in list(App.listDocuments().keys()):
        App.closeDocument(name)
    App.openDocument(FCSTD)
    doc = list(App.listDocuments().values())[0]
    log("opened " + doc.Name + " objects=" + str(len(doc.Objects)))

    hidden = 0
    for o in doc.Objects:
        if o.TypeId in ("App::Origin", "App::Plane", "App::Line") or \
           o.isDerivedFrom("App::GeoFeatureGroup"):
            try:
                o.ViewObject.Visibility = False
                hidden += 1
            except Exception:
                pass
    log("hidden datums: " + str(hidden))

    gui_doc = Gui.getDocument(doc.Name)
    view = gui_doc.ActiveView

    # orthographic camera for clean engineering views
    try:
        view.setCameraType("Orthographic")
        log("camera type: " + str(view.getCameraType()))
    except Exception:
        log("setCameraType err: " + traceback.format_exc().splitlines()[-1])

    BATCH = [
        ("iso",   "viewIsometric"),
        ("iso2",  "viewAxonometric"),
        ("top",   "viewTop"),
        ("bottom","viewBottom"),
        ("front", "viewFront"),
        ("rear",  "viewRear"),
        ("left",  "viewLeft"),
        ("right", "viewRight"),
    ]

    for name, meth in BATCH:
        try:
            getattr(view, meth)()
            view.fitAll()
            Gui.updateGui()
            path = os.path.join(OUTDIR, "v1_" + name + ".png")
            view.saveImage(path, W, H, "White")
            log("saved " + os.path.basename(path) + " bytes=" + str(os.path.getsize(path)))
        except Exception:
            log(meth + " FAILED: " + traceback.format_exc().splitlines()[-1])

    # 4 diagonal angles via setViewDirection (camera looks along -dir)
    for i, (dx, dy, dz) in enumerate([
        (1.0, 0.5, 1.0), (-1.0, 0.5, 1.0), (1.0, -0.5, -1.0), (-1.0, -0.5, -1.0)]):
        try:
            view.setCameraType("Orthographic")
            view.setViewDirection(App.Vector(float(dx), float(dy), float(dz)))
            view.fitAll()
            Gui.updateGui()
            path = os.path.join(OUTDIR, "v1_diag%d.png" % (i + 1))
            view.saveImage(path, W, H, "White")
            log("saved " + os.path.basename(path) + " bytes=" + str(os.path.getsize(path)))
        except Exception:
            log("diag%d FAILED: %s" % (i + 1, traceback.format_exc().splitlines()[-1]))
except Exception:
    log("FATAL: " + traceback.format_exc())
try:
    Gui.closeDocument(doc.Name)
except Exception:
    pass
try:
    Gui.exitApplication()
except Exception:
    pass
sys.stdout.flush()
os._exit(0)