# Concept A Bench Prototype — DAY 6–7 Scaffold
**Selected:** Servo+Pushrod (DAY 5, score 4.05)  
**Pivot:** Ø32 barrel → Ø10 steel shaft in 2×6802 15×24×5 (Vyan plain bore upgraded)  
**Pushrod:** 95–110 mm CF Ø6 + M3 ball-links (Vyan 161 mm shortened)  
**Servo:** ≥20 kg·cm (DS3218MG / HV7232MG), not MG90S

This folder will hold the printable CAD for the T01 bench rig (no aircraft).
Run `concept_A_tilt_mechanism.py` in FreeCAD to regenerate.

## Files
- `concept_A_tilt_mechanism.py` — parametric FreeCAD generator (run via `freecadcmd` or GUI Python console)
- `concept_A.scad` — same geometry in OpenSCAD for quick STL export / vase-mode tweaks (OpenGeoDrone workflow)
- `BOM.md` — what to buy vs print
- `print_list.md` — STLs + slicer settings

## Quick generate
GUI: FreeCAD → View → Panels → Python console → `exec(open(r".../concept_A_tilt_mechanism.py").read())` → File → Export → STL  
Headless: `freecadcmd.exe concept_A_tilt_mechanism.py` → exports to `exports/`
