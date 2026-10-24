# DAY 5 — Three Candidate Tilt Mechanisms (Guide Sec 29)
**Date:** 2026-09-14  
**Baseline from refs:** Vyan push-plate 161.2×82.8×5.1 mm, pivot Ø32 mm plain bore, MG90S undersized, ducts Ø257–291 mm; REI S-curve + `tilt_can_transition()` gate; Underactuated T/W+altitude crash chain

## Concept A — Servo + Pushrod (Vyan-derivative, recommended)
**Layout:** offset servo (≥MG996R/DS3218MG class, NOT MG90S) → 15–22 mm servo horn → M3 pushrod with ball-links → 30–40 mm hinge horn → Ø32 mm steel pivot in 6805-2RS bearings in printed + carbon clamp housing; motor arm clamped to hinge barrel (Ø50–55 outer from Vyan); `hingeback`-analogue boom clamp 55 mm block.
```
[servo]--(horn)--[pushrod w/ M3 ball-links]--(horn)--[hinge barrel pivot Ø32]--[motor mount]
   \___boom clamp / printed bracket___/          \___boom___
```
- **Geometry reused:** Vyan rod/servohinge ratio proven; V1 tightens tolerances: horn hole Ø5.0 mm (measured) → use 4.8 mm ball-link, backlash target <0.8°
- **S-curve** from REI `tilt_transition.m:60` applied in FC (3p²−2p³), slew-limited
- **Pros:** servo isolated from flight loads, field-replaceable rod, proven kinematics, cheap, easy T01 cycling
- **Cons:** 2 extra joints = backlash source, pushrod can buckle under ~15 N thrust moment if length >140 mm (Vyan 161 mm is long for twin 10×6 prop — shorten to ~90–110 mm for V1)

## Concept B — Direct Servo Drive (coaxial)
**Layout:** servo output shaft directly coaxial with tilt axis; motor/duct cradle bolts to 25T servo horn + aluminum servo-block; pivot and servo are same axis; bearings still in housing but servo spline carries moment.
```
[boom]--[housing+bearings]--[servo body fixed]--[servo spline = pivot]--[motor cradle]
```
- **Pros:** fewest parts, ~40–60 g lighter than A (no rod/hinges), near-zero linkage backlash, compact boom
- **Cons:** servo takes full bending/thrust moment (≈ thrust × 18 mm offset + inertia × accel). MG90S 2.2 kg·cm stalls; twin 10×6 at 70% = ~12 N vertical → moment ~0.22 N·m just static — needs ≥20 kg·cm steel-gear servo (e.g., DSSERVO DS3218MG), vibration fatigues spline, crash destroys servo

## Concept C — Geared/Linkage (worm or 4-bar with mechanical advantage)
**Layout:** servo drives worm (reduction ~5:1) or spur-gear sector (40T sector) → hinge barrel; or 4-bar parallelogram keeping motor vertical through range. Worm self-locking holds tilt without power.
```
[servo]--[worm 15T]--[sector 60T on pivot]--[motor mount]  OR  [servo]--[4-bar]--[motor mount]
```
- **Pros:** torque amplification (~3–5× in Vyan-ratio terms), can use smaller servo, worm holds position at zero current, smoother transition
- **Cons:** heaviest (+70–120 g vs B), needs CNC gear/sector or printed herringbone (wear, dust), alignment critical, cost, field service needs backlash shimming

---

## Scoring (1=poor, 5=excellent; higher = better for V1 prototype)

| Criterion | Weight | A: Servo+Pushrod | B: Direct | C: Geared/4-bar |
|---|---:|---:|---:|---:|
| Mass | 0.20 | 3 (baseline ~85–110 g per side incl. servo/housing/rod) | 5 (~45–65 g) | 2 (~130–170 g) |
| Complexity | 0.15 | 4 (3 printed parts + rod) | 5 (2 parts) | 2 (5+ parts) |
| Backlash | 0.15 | 3 (~0.5–1.2° with ball-links) | 4 (~0.3–0.6° spline) | 3–4 (worm great, spur moderate) |
| Manufacturability (print + carbon) | 0.15 | 5 (all printable + off-shelf M3) | 4 (needs precise servo-block) | 2 (needs CNC/sector) |
| Serviceability | 0.10 | 5 (rod swapped in field) | 3 (replace servo = disassemble) | 2 (gear mesh shimming) |
| Strength / load path | 0.15 | 4 (bearings isolate servo) | 2 (servo spline is weak link) | 4 (load on gear/housing) |
| Cost | 0.10 | 5 (MG-type servo + M3) | 4 (strong servo pricier) | 2 (gears/CNC) |
| **Weighted total** | 1.00 | **4.05** | **3.95** | **2.45** |

*Method: weighted sum of 1–5 scores; see raw matrix in `DAY5_scoring.csv`*

## Recommendation
**Select Concept A for V1 bench prototype (T01), with Concept B as fallback if mass budget tight.**

- A scores highest (4.05), inherits Vyan's only validated mechanism, decouples crash load from servo, and matches the Guide's simplest-robust principle. Upgrade from Vyan baseline: **Ø32 mm hardened pivot + 6805-2RS pair** (Vyan was plain bore), **DS3218MG / JX PDI-HV7232MG (≥20 kg·cm, 0.10–0.14 s/60°)** instead of MG90S, **90–110 mm carbon pushrod with Dubro ball-links** (shorten Vyan 161 mm to reduce buckling), adjustable horn holes for tilt-range trimming.
- B is lightest but transfers all moment to servo spline — marginal for twin-motor 10×6 thrust; keep as lightweight V2 study after T02 thrust data.
- C rejected for V1 — weight, wear, and manufacturing risk outweigh self-locking benefit; revisit if T03 tilted-thrust shows servo cannot hold position under transition aero load.

## Geometry deltas vs Vyan (for `03_CAD/reference_rebuild/`)
- Pivot: plain Ø32 → steel Ø8–10 mm shaft in 2×6805 (Ø25×37×7 would actually house 32 barrel — check; use 6802 Ø15×24×5 for Ø10 shaft if barrel thinned) — decide after housing CAD
- Horn radius: servo 15–18 mm, hinge 28–35 mm → mechanical advantage 1.6–2.0 reduces servo torque demand
- Pushrod: CF tube Ø6×4 mm + M3 threads, length 95–110 mm (vs Vyan 161 mm)
- Housing: PETG/PA6-CF printed + M3 inserts + carbon tube boom clamp (match Vyan 55 mm block but split for service)

## Risks → Mitigations → Tests
| Risk | Concept where critical | Mitigation | Test ID |
|---|---|---|---|
| Backlash >1° → transition limit-cycle | A | Ball-links + preload, dual shear horn | T01-B servo cycle + T01-C repeated |
| Pushrod buckling / free-play | A | Shorten to <110 mm, CF tube | T04 coupon bending |
| Servo stall/hold under 12 N thrust moment | A,B | ≥20 kg·cm servo, measure in T01-B | T01-B + T03 0–90° thrust map |
| Spline fatigue/gear wear | B,C | Bearing-isolated pivot (A solves) | T01-C 1000-cycle + inspect |
| Print bore creep | A | Bearing insert, not plastic bore | T00 dimensional + heat |

## Next — DAY 6–7 (Guide)
Build **only** the selected Concept A mechanism + representative motor mass (no aircraft): T01-A free movement, T01-B servo cycling (0→45→90, temp/current), T01-C 100/500/1000 cycles — gate to proceed is *repeatable 0–90° with <1° backlash, no binding, <60 °C servo*.
