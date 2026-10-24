# Requirements (CONCEPTUAL ONLY — do NOT freeze, Guide Sec 22)
- Wingspan ~1400 mm / Length ~900 mm / Chord ~180 mm / MH32-type concept / 3° dihedral
- Twin-motor tilt 0–90° / A2212-class concept / 10x6 folding prop concept
- 600 mm tail boom / inverted V-tail / central pod / camera-gimbal provision
- 3D-printable non-primary + carbon primary structure
- Revise after: ref study → mass/thrust/propulsion/mechanism/structural validation.

# Decisions
- Architecture stays twin-motor tilt-rotor (no switch to fixed-wing VTOL for CAD convenience).
- REI = control/systems ref only. Vyan = mechanism/CAD ref. Underactuated = test/failure ref. OpenGeoDrone = parametric-manufacturing ref.
- First physical milestone: validated tilt mechanism (T01). First flight milestone: controlled hover (T07/T08). No transition before Gates 1–8 pass.
- 2026-09-14 DAY 5: Selected Concept A Servo+Pushrod for V1 (score 4.05 vs B 3.95 vs C 2.45; `03_CAD/mechanism/DAY5_concepts.md`). Pivot Ø32 inner / 50-55 barrel, plain→bearing upgrade, CF pushrod 95-110 mm, servo ≥20 kg·cm (not MG90S). B kept as V2 fallback.
