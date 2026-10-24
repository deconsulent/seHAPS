# OpenGeoDrone — Manufacturing Reference Note
**Source:** `01_REFERENCES/OTHER/OpenGeoDrone/` (depth-1 clone from https://github.com/enacuavlab/OpenGeoDrone)  
**Date:** 2026-09-13

- NOT a tilt-rotor baseline. Quad-hover + pusher-plane hybrid, fully parametric OpenSCAD, vase-mode FDM.
- Default ~1200 mm span, 1.066 kg w/o battery, MH61 airfoil, 4S 4Ah, 25 min plane / 90 s hover.
- Value for V1: parametric workflow (`OpenGeoDrone.scad`, `WingGenerator.scad`, `stl_generator.sh`, `stl_print_part/`, `3mf_print_part/`) — how to keep printable parts editable without fragile AI scripts.
- Classification: **manufacturing/parametric-CAD reference.**
- Action: when V1 printable joints/brackets are designed, mirror this pattern (one param file → regenerated STL/3MF, slicer presets versioned).
