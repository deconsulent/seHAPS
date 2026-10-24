# Baltic Tilt-Rotor V1 — Design & Spec Summary
**Rev:** A1-2 · **File:** TR-V1-SPEC-001 · **Date:** 2026-09-16

---

## What we're building
Two variants of one airframe (shared wing, pod, boom, V-tail). Only the propulsion mounts differ - 2 parts change, the rest is common.

**Variant 1 — FIXED (default):** two front A2212 rotors fixed facing up (hover lift only), plus one big tail pusher motor for forward flight. No tilt mechanism, simplest build.

**Variant 2 — TILT (alternate):** Concept A - front rotors tilt 0–90° via DS3218MG servo + pushrod; no tail pusher needed. Already designed and measured.

## Basis (measured, not guessed)
- Vyan CAD measured in FreeCAD 1.1.3 (scripted + GUI agree): pivot bore Ø32.0 mm, housing barrel Ø50–55 mm — high confidence. Plain plastic pivot replaced by 2× 6802-2RS bearings.
- Three concepts scored (mass/complexity/backlash/printability/service/strength/cost): A servo+pushrod 4.05, B direct-drive 3.95, C geared 2.45 → A.
- Fixed variant: front pylons simplified, big tail pusher added. Hover = 2-rotor lift, cruise = pusher + wing lift.

## Size (concept draft)  |  Mass (estimate - each line gets measured)

| Size | |
|---|---|
| Wingspan / Length | 1400 / 900 mm |
| Chord / Area / AR | 180 mm / 0.252 m² / 7.8 |
| Airfoil / dihedral | MH32 / 3° |
| Boom / props | 600 mm Ø16 / 10×6 lift + ~Ø250 pusher |
| Driveline | 2× A2212 + 1 tail motor, 4S |

| Mass | g |
|---|---|
| Structure + Avionics | 605 + 118 |
| Fixed propulsion (2×A2212, 2 ESC, 2 props) | 210 |
| Tail pusher (motor/ESC/prop) | ~180 |
| Power (4S + wiring) + Payload (camera) | 345 + 120 |
| Dry / AUW / +10% target | ~1200 / ~1425 / ~1640 |

Thrust: T/W 1.3–1.5. Front fixed pair must hover-lift AUW (~16 N at 1.3) — confirmed on thrust stand (T02). Pusher sized for cruise. Note: 2-point hover is pitch-weak — review with a small rear lift rotor or slight pusher tilt if tests show it.

## Printing  |  Buy list (~€40)

| Printing | |
|---|---|
| Filament | ~170 g PETG + PA6-CF, <€5 |
| Infill | clamp 50% / barrel 60% / mount 40% / horn-rod 60%; 0.2 mm, 4 walls, gyroid |
| First part | T00 coupon: Ø24.00 within 0.10 mm, bearing slip-fit |
| Fixed variant | fewer parts (no tilt housing) |

| Buy (~€40) | |
|---|---|
| Servo (tilt) | DS3218MG 20 kg·cm |
| Bearings + shaft | 2× 6802-2RS + Ø10×45 + collars |
| Pushrod | CF + Dubro ball-links |
| Stand-ins | Ø16×200 stub, 80–100 g dummy mass |
| Bench | plywood, 6 V BEC, tester, calipers, IR thermometer |

## Test gates
T00 coupon → T01 bench cycling (free, servo 0–45–90, 100/500/1000 cycles; backlash <1.0°, servo <60 °C) → T02 thrust stand → T03 tilted-thrust map → hover → transition (alt ≥10 m, spare props).

## References
[1] REI Drone – rootcastleco/rei-drone  [2] Vyan – GeneralVader/Tilt_Rotor_VTOL_UAV  [3] Underactuated – Sanassah/Underactuated-Tiltrotor  [4] OpenGeoDrone – enacuavlab/OpenGeoDrone. Clones unmodified; CAD measured FreeCAD 1.1.3. Source: `03_CAD/mechanism/`, `01_REFERENCES/*/notes.md`.