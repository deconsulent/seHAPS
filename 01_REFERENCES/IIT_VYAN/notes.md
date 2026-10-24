# IIT Vyan Tilt-Rotor CAD — Study Notes (DAY 3)
**Source:** `01_REFERENCES/IIT_VYAN/source/` cloned from https://github.com/GeneralVader/Tilt_Rotor_VTOL_UAV  
**STEP extracted to:** `01_REFERENCES/IIT_VYAN/STEP/VTOL Steps/` from `VTOL Steps.7z` (19 MB → 102 MB)  
**Date:** 2026-09-13 / updated 2026-09-14 with FreeCAD 1.1 headless measurement (`D:\Installation\FreeCAD 1.1\bin\freecadcmd.exe`)

## 1. Architecture (from README)
- 4x ducted 10x5 props on twin booms below high wing; **front 2 tilt**, rear 2 fixed (shut off in cruise to save power)
- Inverted V-tail (~20% less wetted area claim), high-wing monoplane, Wortmann FX 73-CL2-152 airfoil, ribs/spars balsa+birch+carbon + solar film
- Fuselage: stringer/frame balsa+birch + skin, Al landing gear, camera+gimbal underneath
- Battery + Pixhawk at CG = intersection of diagonals of square formed by 4 props
- Servo push-pull rod + rotor hinge mechanism (one rod + hinge per side)

## 2. Files found
- `tiltmech/`: `hinge1.SLDPRT`, `hinge2.SLDPRT`, `hingeback.SLDPRT`, `rod.SLDPRT`, `rodhinge.SLDPRT`, `servohinge.SLDPRT`, `tiltservo.SLDPRT`, `Servo, Metal Gear, MG90S.SLDPRT`, `tiltassemb.SLDASM`
  → MG90S metal-gear servo is the documented actuator. Good starting hypothesis for V1 servo class (verify torque after loads measured).
- `prop/`: `duct.SLDPRT`, `16x5.4.SLDPRT` (note: README says 10x5 ducted — 16x5.4 file may be prototype variant, do NOT trust blindly), `bldc motor.SLDPRT`
- `wing/`, `fuselage/`, `prototypes/`, `vtol.SLDASM` (9.7 MB), `vtoldrawing.PDF` (empty title-block template, no usable dims), `vtoldrawing.SLDDRW`
- STEP (AP214, SolidWorks 2018, SwSTEP 2.0): `vtol.STEP` 64.3 MB, `wing.STEP` 18.3 MB, `tail.STEP` 12.2 MB, `fuselage.STEP` 7.1 MB — valid ISO-10303-21, units meters (spot coords ~0.005–0.9 m)

## 3. Tilt mechanism — FreeCAD measurement (vtol.STEP, 432 objects / 270 Part::Feature)
Tool: `freecadcmd.exe` + `Import.insert()`. Units in STEP import read as **mm** (fuselage subset bbox 803.7 x 322.1 x 202.1 mm — plausible; full-assembly bbox 2079.9 x 804.7 x 2748.9 mm is NOT aircraft size — subassemblies import at scattered/exploded positions, e.g. ribs at y~560, motors at x~-810).

Front-tilt cluster found (mirrored pair, z ≈ +380 vs −430):
- `hingeback` x2: 55.00 x 63.10 x 55.00 mm, vol 17,648 mm³; cyl radii r = 1.0 / 16.0 / 25.0 / 26.1 / 27.5 mm
- `servohinge` x2: 40.00 x 97.85 x 55.00 mm, vol 28,305 mm³; r = 2.5 / 25.5 / 27.5 mm
- `hinge1` x2: 55.00 x 52.00 x 52.00 mm, vol 3,507 mm³; r = 3.5 / 25.25 / 26.0 mm
- `hinge2` + `hinge002`: 64.31 x 74.03 x 55.00 / 67.11 x 72.85 x 55.00 mm, vol ~15,292 mm³; r = 1.0 / 2.5 / 5.0 / 16.0 / 27.5 mm
- `rod` push-plate: 161.17 x 82.88 x 5.10 mm, vol 5,623 mm³; holes r = 2.5 / 5.0 mm (mirror `rod001`: 143.58 x 111.60 x 5.10)
- `rodhinge`: 32.11 x 23.14 x 10.00 mm, vol 2,111 mm³; r = 1.1 / 2.5 / 4.91 / 8.55 mm
- `tiltservo` bracket x2: ~32.4 x 13.0 x 31.9 mm, vol ~7,501 mm³
- `Servo, Metal Gear, MG90S` x4: ~16.6 x 6.2 x 19.2 mm CAD envelope (UNDERSIZED vs real MG90S 23.1 x 12.2 x 29.0 mm — CAD is schematic, use datasheet for V1)
- `duct` x4: Ø ~257–291 mm x 34.4 mm height (front pair rectangular-pattern ducts 273/291 mm; rear 257/230 mm variants) — consistent with 10-inch class ducted props
- Wing rods (`1st–4th rod new 1`): Ø 6–18 mm, lengths 1,294–2,468 mm (spans in exploded placement, not bay lengths)

## 4. Mechanism record table — GUI-verified 2026-09-14 (`measure_tilt_gui.py` + `measure_tilt_gui_v2.py`, FreeCAD 1.1.3)
Confirmed in GUI Report view (both runs identical):
| Parameter | Value | Source | Confidence |
|---|---:|---|---|
| Pivot diameter | **Inner pivot Ø 32.0 mm (r 16.0 hingeback/hinge2) confirmed both headless + GUI**; barrel outer Ø 50.0 / 52.19 / 55.0 mm (hingeback), hinge1 Ø 50.5 / 52.0 mm, hinge2 Ø 55.0 mm — rotating bore is 32 mm, housing ~51–55 mm | vtol.STEP GUI+headless | **High** |
| Bearing type | **Plain bore** — no bearing ring part in tree; all bores plain cylindrical faces (r 2.0/2.5/5.0 fastener holes). V1 must insert real 6805/6905-class bearing + T00 test | CAD | **High** |
| Tilt range | Still numerically TBD — linkage is servo → `rod` plate (161.2×82.8×5.1 holes Ø5/10) → `rodhinge` (31.7×22.7×10 Ø5.0/9.8/17.1) interlink; README front-only vertical tilt, rear fixed. GUI visually confirms but needs horn-radius calc for angle | CAD/docs + GUI visual | Medium |
| Servo type | MG90S metal gear ×4 (labels MG90S + MG90S001-003) but CAD envelope undersized 16.6×6.1×19.1 mm vs real MG90S 22.8×12.2×28.5 mm — trust datasheet ~2.2 kg·cm @6 V, 13 g; bench-test T01-B | CAD label + datasheet | **High (mismatch confirmed)** |
| Pushrod geometry | **GUI bbox:** `rod` 161.2×82.8×5.1 vol 5623, `rod001` 143.5×111.6×5.1, `rodhinge` 31.7×22.7×10 vol 2111 (Ø2.2/5.0/9.8/17.1), `servohinge` 40.0×97.8×55.0 vol 28305, `tiltservo` 32.4×12.6×31.8 vol 7501 | vtol.STEP GUI | **High** |
| Structural attachment | `hingeback` 54.9×63.1×55.0 vol 17648 = boom clamp block; twin-boom spar interface Ø consistent with ducts Ø 257–291 mm (10-inch class) | CAD | High |

## 5. FreeCAD procedure — GUI-verified 2026-09-14
1. FreeCAD 1.1.3 at `D:\Installation\FreeCAD 1.1\bin\` — 432 objects / 270 Part::Feature
2. Headless: `freecadcmd.exe` + `measure_tilt_headless.py` → bbox/cyl survey (matches GUI)
3. GUI: `measure_tilt_gui.py` → isolate 18 tilt features → Report-view bore dump (above) + screenshots `tilt_iso/side/top.png` (first run blank 9265 B due to App::Part hidden bug)
4. GUI v2: `measure_tilt_gui_v2.py` (fix ViewObject.Visibility) → 18 features → `tilt_iso.png` 13751 B (0.19% non-white), `tilt_side.png` 11218 B (0.15%), `tilt_top.png` 9886 B (0.055%) at 1920×1080 — geometry present but small because both mirrored clusters (≈1200 mm apart) fit in one view. For presentation, re-run with single side only (hide `*001` mirrors) to enlarge.
5. Scripts kept in `IIT_VYAN/` + `C:\Users\shiva\AppData\Local\Temp\opencode\`
6. Note: `TwinTiltParametric/Init.py` `__file__` error on freecadcmd init — harmless.

## 6. Classification
**Vyan = primary mechanical/CAD reference.** Only reference with real STEP + tilt-assembly parts. Architecture differs from V1 (Vyan = 4-rotor hybrid with rear shutoff; V1 = twin-motor tilt-rotor), so extract **mechanism principle (servo + pushrod + hinge)**, not full airframe.

## 7. Cautions
- No mass, power, or test data in repo — purely CAD/design-event (IIT TechFest AL-VTOLA). Do NOT use for thrust/power budgets.
- Prop size conflict (10x5 vs 16x5.4 file) → resolve by measurement, not README.
- Drawing PDF has no dimensions — ignore for engineering.
- Balsa/birch/solar-film construction ≠ our carbon + print strategy — adapt joints, keep hinge kinematics.
