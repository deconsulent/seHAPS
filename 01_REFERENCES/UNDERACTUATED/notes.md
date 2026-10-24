# Underactuated Tiltrotor — Study Notes (DAY 4)
**Source:** `01_REFERENCES/UNDERACTUATED/source/` cloned from https://github.com/Sanassah/Underactuated-Tiltrotor  
**Date:** 2026-09-13

## 1. Concept (why it matters for us)
- Concordia capstone (7 students), inspired by NEMO tiltrotor UAV
- **Underactuated:** NO tilt servos — Vertiq motors + hinge vector thrust via per-revolution voltage pulsing (accel/decel angling). Opposite philosophy to our V1 (servo + pushrod). Study as failure/test-method ref, NOT as mechanism to copy.
- Custom Teensy 4.1 FC forked from `dRehmFlight` (included as `dRehmFlight/`); `NemoFlightController/`, `Firmwares/Firmware2306|2314/`, test-stand “Dory” + attitude stand “Marlin”, `Test/DataStreamer.xlsx`, elevon-actuation paper in `Ressources/`

## 2. Test journey (from README, dated photos)
- 2024-02-02: design + assembly (many hours)
- 2024-02-04: 3D-printed parts on attitude stand “Marlin”
- 2024-02-09: electrical integration
- 2024-02-11: full drone assembled
- 2024-03-11: ground-restrained attitude test → “Bunny Hop” (chipped props, thrust shortfall noted same day)
- 2024-03-25: first hover success → horizontal-speed attempt → **fatal crash** (nacelles struck ground, T/W too low to recover, expensive Vertiq props destroyed → testing paused)

## 3. Failure table (per Guide Sec 4)
| Test | Result | Failure | Suspected Cause | Lesson for V1 |
|---|---|---|---|---|
| Test stand (Dory/Marlin) | Pass | — (proved servo-less vectoring on stand) | — | Keep a restrained stand (T03-style) before free flight; stand success ≠ flight success |
| Electrical integration | Pass | — | — | Bench electronics with props OFF first (our T05) |
| Ground restraint (2024-03-11) | Partial | Limited authority on tether | Tether dynamics mask control margins | Log tether tension; do NOT tune gains solely on tether |
| Bunny hop (2024-03-11) | Partial | Chipped props + “missing some thrust” | Low T/W margin, possible prop damage / voltage sag / overweight | Hover requires measured T/W ≥ ~1.3–1.5 on fresh battery (verify in our T02); abort on prop damage |
| Hover (2024-03-25) | Pass (brief) | — first hover achieved | — | Freeze config after first hover; expand envelope gradually (our T08) |
| Transition / horizontal-speed attempt (2024-03-25) | **Fail — crash** | Nacelles touched ground, could not recover, props destroyed | Low T/W + low altitude + tilt-induced descent/ground contact; no abort margin; expensive props = no spares | **Never attempt transition on low hover margin; keep altitude ≥10 m (REI gate), define abort (return-to-hover) criteria, keep landing gear clearance for tilt geometry, stock spare props** |

## 4. What caused the failure? (synthesis)
Crash chain: marginal hover thrust → attempted forward flight at low altitude → thrust vector tilted away from vertical without wing lift yet → sink + nacelle ground strike → insufficient excess thrust to arrest → prop destruction. Stand tests did not expose the T/W + altitude-margin problem. This is exactly why our Guide mandates Gates 3 (measured propulsion) → 7 (controlled hover) → 9 (transition authorized) with abort criteria.

## 5. Classification
**Underactuated Tiltrotor = test-method and failure-analysis reference.** Copy their discipline (stands → restraint → hop → hover → incremental envelope, photo/video per test), avoid their architectural risk (exotic servo-less tilt) for V1.

## 6. Reuse for V1
- Test-ID log + photo per date (adopt `TR-V1-Txx-xxx` + `Test/DataStreamer.xlsx`-style sheet for our T-series)
- `dRehmFlight`-based Teensy FC as reminder: custom FC = large scope; prefer Pixhawk + PX4/ArduPilot for V1 (per REI stack)
- Spare-props rule, T/W margin rule, no-transition-on-first-hover rule → add to `07_FAILURES/` FMEA
