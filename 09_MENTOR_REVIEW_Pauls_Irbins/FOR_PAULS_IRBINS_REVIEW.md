# Baltic Tilt-Rotor V1 — Mentor Review Pack
**For:** Pauls Irbins  
**From:** V1 Tilt-Rotor Team (ISR)  
**Date:** 2026-09-14  
**Program:** Engineering Working Guide Sep 2026 (`Baltic_Tiltrotor_V1_Reference_Study_and_Test_Program.md:1`)  
**Status:** Reference study + CAD measurement + trade study complete. **Request: green light to print T00 coupon + Concept A bench rig (T01).**
**Folder:** `BALTIC_TILTROTOR_V1/09_MENTOR_REVIEW_Pauls_Irbins/` — all proof artifacts linked.

---

## 1. Executive Summary
- **Architecture frozen:** twin-motor tilt-rotor, VTOL + wing-borne cruise, 3D-print non-primary + carbon primary, V1 experimental not production (`decisions.md:9`)
- **No shortcut to fixed-wing** — guide principle respected
- **Four references cloned unmodified** and measured — not blindly copied
- **Mechanism measured in FreeCAD 1.1.3** (`D:\Installation\FreeCAD 1.1\bin\`): Vyan STEP 432 objs / 270 features, pivot Ø32 mm High confidence
- **Three concepts scored** — **Concept A Servo+Pushrod selected** for V1 (4.05/5 weighted) → bench rig STLs exported and ready
- **Gate:** T00 dimensional + T01 bench must pass before any propulsion (T02) or airframe (T04) — per guide decision gates Sec 26
- **Ask:** approve print of `bearing_pocket_test.stl` + `boom_clamp/hinge_barrel/servo_mount` for T01 bench; motors/props deferred.

---

## 2. Folder Proof — Where Everything Lives
```
BALTIC_TILTROTOR_V1/
├── 00_ADMIN/project_log.md, decisions.md
├── 01_REFERENCES/
│   ├── REI_DRONE/source/ (7f57962) + notes.md + figures/
│   ├── IIT_VYAN/source/ (8fa76a8) + STEP/VTOL Steps/ (vtol 64.3 MB) + screenshots/ (6 PNGs) + notes.md
│   ├── UNDERACTUATED/source/ (09c0213) + notes.md
│   ├── OTHER/OpenGeoDrone/ (4c61197) + notes.md
│   └── reference_matrix.md
├── 03_CAD/mechanism/DAY5_concepts.md, DAY5_scoring.csv, BOM.md, print_list.md, concept_A_tilt_mechanism.py, concept_A.scad
├── 03_CAD/exports/ (4 STLs, see §6)
├── 05_TESTING/T01_tilt_mechanism/test_sheet.md + T00_component/T00-001.md
└── 09_MENTOR_REVIEW_Pauls_Irbins/FOR_PAULS_IRBINS_REVIEW.md (this file)
```
Clones are full `git clone` with `.git` intact — hashes above prove unmodified history.

---

## 3. Reference Study — What Was Learned (not copied)

### 3.1 REI Drone — Systems/Control Reference
- **Source:** `01_REFERENCES/REI_DRONE/source/` 7f57962 — `matlab/` 11 files, `firmware/src/` 11 files, `paper/paper.pdf` 10 pp
- **Key extraction (`REI_DRONE/notes.md:1`):** 6-DOF equations, S-curve tilt 3p²−2p³ (`tilt_transition.m:60`), cascade PID, `tilt_can_transition()` altitude gate ≥10 m, weight/CG table 29 components
- **Finding:** **No CAD** — renders only. Quad tilt-rotor (4 motors) ≠ our twin — reuse logic, not dims. Confidence High (code) / Low (claimed 100 km/h, no raw logs)

### 3.2 Vyan (IIT Bombay) — Mechanical/CAD Reference *Primary*
- **Source:** `01_REFERENCES/IIT_VYAN/source/` 8fa76a8 — `tiltmech/` 9 SLDPRT + `VTOL Steps.7z` 19→102 MB → `STEP/VTOL Steps/` vtol 64.3 MB (AP214, SW2018)
- **FreeCAD Headless + GUI verified 2026-09-14:**
  - Tool: `freecadcmd.exe` + GUI `measure_tilt_gui.py` / `measure_tilt_gui_v2.py` / `measure_single_side.py`
  - 432 objects / 270 Part::Feature, units mm
  - **Measured (both runs identical):**
    - `hingeback` 54.9×63.1×55.0 vol 17648 — cyl Ø 32.0 inner / 50.0/52.19/55.0 outer
    - `hinge1` Ø 50.5/52.0, `hinge2` Ø 32.0 inner, `servohinge` Ø 51.0, `rod` 161.2×82.8×5.1 holes Ø5/10, `rodhinge` Ø5/9.8/17.1
    - **Bearing: plain bore** (no bearing part) — must upgrade
    - MG90S CAD 16.6×6.1×19.1 **undersized vs real 22.8×12.2** — use datasheet
  - **Screenshots:** `screenshots/tilt_iso.png` 13751 B, `tilt_side.png` 11218 B, `tilt_top.png` 9886 B + single-side variants — 0.05–0.20% non-white (both mirrored clusters in view; tight `V+F` zoom recommended for presentation)
- **Cautions:** no mass/power data, TechFest concept, 10×5 vs 16×5.4 conflict — not for budgets

### 3.3 Underactuated Tiltrotor — Failure/Test-Method Reference
- **Source:** `01_REFERENCES/UNDERACTUATED/source/` 09c0213 — Teensy/dRehmFlight fork, test stands Dory/Marlin
- **Journey (`UNDERACTUATED/notes.md:1`):** 2024-02 design → 2024-03-11 bunny hop (chipped props, low thrust) → 2024-03-25 first hover → crash on horizontal speed (nacelles ground strike, T/W too low, expensive Vertiq props destroyed)
- **Lesson for V1:** Keep T/W ≥1.3–1.5 measured, altitude ≥10 m before transition, abort criteria, spare props — built into T01 gates

### 3.4 OpenGeoDrone — Manufacturing Reference
- **Source:** `01_REFERENCES/OTHER/OpenGeoDrone/` 4c61197 — OpenSCAD parametric + vase-mode, ~1200 mm span
- **Reuse:** one-file parametric → STL/3MF pipeline for our printable brackets (see `concept_A.scad`)

### 3.5 Reference Matrix
`01_REFERENCES/reference_matrix.md:1` — live matrix with confidence ratings; Vyan = mechanism, REI = control, Underactuated = test method, OpenGeoDrone = printing workflow. No single ref is twin-motor.

---

## 4. Current CAD — What Exists Now

### 4.1 Measured Vyan Mechanism (proof)
- **Files:** `IIT_VYAN/STEP/VTOL Steps/vtol.STEP` + `IIT_VYAN/notes.md:20` table (High confidence post-GUI)
- **Screenshots:** `IIT_VYAN/screenshots/` 6 PNGs (timestamps 2026-09-14 12:15–12:17)
- **Scripts:** `measure_tilt_gui.py`, `v2.py`, `measure_single_side.py` + headless logs `C:\Users\shiva\AppData\Local\Temp\opencode\`

### 4.2 Concept A Parametric Rig (ready to print)
- **Generators:** `03_CAD/mechanism/concept_A_tilt_mechanism.py` (FreeCAD) + `concept_A.scad` (OpenSCAD)
- **Headless run 2026-09-14:** `freecadcmd.exe concept_A_tilt_mechanism.py` → `03_CAD/exports/` 4 STLs (see §6)
- **Dims inherited from measurement:** barrel Ø32 ID / Ø52 OD ×55, shaft Ø10, clamp 63×55×30 for Ø16 boom, pushrod 105 mm (shortened from Vyan 161 mm to avoid buckling), servo mount pocket 40.5×20 for DS3218MG

### 4.3 Exports Ready
`03_CAD/exports/` — headless generated, not hand-edited:
- `bearing_pocket_test.stl` 308898 B
- `boom_clamp.stl` 242338 B
- `hinge_barrel.stl` 476338 B
- `servo_mount.stl` 8338 B

### 4.4 What Is NOT Modeled Yet (by plan — guide Sec 7)
- No airframe wing/fuselage/tail, no motors/ESCs — deliberately deferred until T01 bench passes (reference → measure → reproduce subsystem → bench test → modify → integrate)

---

## 5. Trade Study — Why Concept A
`03_CAD/mechanism/DAY5_concepts.md:1` + `DAY5_scoring.csv:1`

| Concept | Layout | Mass | Complexity | Backlash | Manufacturable | Serviceable | Strength | Cost | Weighted |
|---|---|---|---|---|---|---|---|---|---|
| **A Servo+Pushrod (selected)** | offset servo → M3 ball-link rod → Ø32 bearing pivot | 3 | 4 | 3 | 5 | 5 | 4 | 5 | **4.05** |
| B Direct | servo spline = pivot | 5 | 5 | 4 | 4 | 3 | 2 | 4 | 3.95 |
| C Geared/Worm | 5:1 worm/sector | 2 | 2 | 3–4 | 2 | 2 | 4 | 2 | 2.45 |

**Pick A** — highest score, isolates crash load from servo spline, proven Vyan kinematics, field-swappable rod, cheapest. Upgrades over Vyan: 2×6802 bearings, Ø10 hardened shaft, 95–110 mm CF rod with ball-links, ≥20 kg·cm servo (DS3218MG ≠ MG90S). B is lightest but servo bears all moment (0.22 N·m static from 12 N thrust) — keep as V2. C rejected for weight/CNC.

---

## 6. Test Plan & Gates (Guide Sec 8–10, 26)

### 6.1 Philosophy
Quantitative: `05_TESTING/T01_tilt_mechanism/test_sheet.md:1` lists every measurement; no “seems strong”.

### 6.2 T00 Coupon (print FIRST, today, no purchase)
`bearing_pocket_test.stl` → `05_TESTING/T00_component/T00-001.md` — caliper check Ø24.00 <0.10 mm error, bearing slip fit. **Must pass before housings.**

### 6.3 T01 Tilt Bench (Concept A rig only — no aircraft)
- **T01-A free:** hand 0→90° check binding, <0.3 mm play — `TR-V1-T01-A-001`
- **T01-B servo cycle:** 0→45→90 at 6 V, record V/A/temp/backlash — `<60 °C, <1.0° backlash`
- **T01-C endurance:** 100/500/1000 cycles — inspect wear, still <1.0°

**Abort:** if >1° backlash, current spike, cracked print → stop → `07_FAILURES/` per Underactuated lesson.

### 6.4 Gates
1 ref study ✅ → 2 T01 bench → 3 propulsion T02 → 4 structure T04 → 5 airframe → 6 electronics w/o props → 7 hover → 8 envelope → 9 transition authorized → 10 V1 review. **We are requesting Gate 2 entry (print).**

---

## 7. BOM & Print List — What You Approve

**Buy (lead time, order now):** `03_CAD/mechanism/BOM.md:1`
- DS3218MG 20 kg·cm ×1, 6802-2RS×2 + Ø10 shaft + collars, CF Ø6 + M3 ball-links×2, Ø16 tube 200 mm stub, dummy 80–100 g mass, M3 inserts, 6 V BEC
- **Not yet:** motors/ESCs/props, airframe — deferred to T02/T04

**Print (after T00 pass):** `03_CAD/mechanism/print_list.md:1`
- PETG or PA6-CF, 0.2 mm, 4 walls, 50–60% gyroid, 45° overhang
- Order: T00 coupon → `boom_clamp` (2.5 h) → `hinge_barrel` (1.5 h) → `servo_mount` (2 h)

---

## 8. Risk & Why Sequential
- **Underactuated crash** (low T/W + low altitude) → we measure thrust (T02) and keep ≥10 m gate
- **REI telemetry 17.8% sim error** → we compare sim vs bench, not trust sim alone
- **Vyan plain bore** → we add real bearings
- **Printing everything before buying** would waste filament if servo footprint mismatches — we propose **coupon-first then buy → final print**.

---

## 9. Ask
**Pauls — please green-light:**
1. Print `bearing_pocket_test.stl` today (T00)
2. Order Concept A BOM (servo/bearings/pushrod — ~€40)
3. On T00 pass + parts in hand, print final 3 STLs and run T01-A/B/C per `test_sheet.md`

Blue-sky: after T01 1000-cycle pass, we proceed to T02 thrust stand (A2212 10×6, restrained, not hand-held).

---

## 10. Appendices — Direct Links (open in VS Code / File Explorer)
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\REI_DRONE\notes.md`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\notes.md`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\IIT_VYAN\screenshots\tilt_iso.png` (and 5 others)
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\01_REFERENCES\UNDERACTUATED\notes.md`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\mechanism\DAY5_concepts.md`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\mechanism\DAY5_scoring.csv`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\mechanism\BOM.md`
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\03_CAD\exports\` (4 STLs)
- `D:\Projects\ISR\BALTIC_TILTROTOR_V1\05_TESTING\T01_tilt_mechanism\test_sheet.md`

*Tooling:* FreeCAD 1.1.3 (`D:\Installation\FreeCAD 1.1\bin\freecadcmd.exe`), 7-Zip 24.05, Python 3.14 — all runs logged.

---
*Prepared step-by-step from `Baltic_Tiltrotor_V1_Reference_Study_and_Test_Program.md` Sec 1–30. V1 dimensions remain conceptual (~1400/900 mm, MH32) until mass/thrust/mechanism tests revise them.*
