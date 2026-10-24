# V1_2_FIXED_V2 — mass budget & CG (from CAD, flat wing + 6S final config)
**Source:** `V1_2_FIXED_V2.FCStd` (built 2026-10-13 by `build_V2_6S_update.py`, r2 relocation by script; stock power parts hidden)
**Method:** spec masses at measured CAD stations (lumped groups — first pass, bench-verify at T06)

## Mass rollup, r2 refined (12 groups, rows sum to 3108g — reconciles to MTOW exactly)
| Group | Mass | X station | Basis |
|---|---|---|---|
| Wing group | 400g | -208 | measured wing bbox center |
| Pod group | 300g | -48 | measured pod bbox center |
| Tail + mounts group | 200g | -500 | measured tail bbox center; −50g OD20x1.0 booms applied |
| Lift motors 4×120g | 480g | -159 | prop shaft stations (488/493/−808 avg) |
| Rear motor | 90g | -594 | measured QAA2814 envelope center |
| ESC boards (4-in-1 + rear) | 60g | +140 | new homes X[110,195] centroid |
| Props (4 lift + 1 rear) | 100g | -251 | 4×20g at lift stations + 20g at −618 |
| Wiring harness | 190g | -100 | pod→boom runs (assumed; ±50mm station error moves CG ±3mm) |
| Electronics (FC+GPS) | 84g | +150 | relocated nose bay X[109,193] |
| Battery 6S2P RS50 (slid fwd) | 904g | -30 | pack envelope X[-96,+36] |
| Camera | 120g | +5 | gimbal station |
| Servos + pitot + rods | 180g | -336 | aileron/tail midpoint (assumed) |

Numerator with RS50 pack: −437,424 g·mm / 3108 g → CG_X = **−140.7 → IN RANGE** [-143.5,-127.3] (model ±20mm — bench-verify at T06).

Reconciliation note (review 2026-10-13): an independent recompute got −117.7 — exactly reproduced here by moving the *whole* 350g ESC+props+wires lump to the nose bay (+350×199mm = +69,650 g·mm → −117.7). That lump was never stated as moved: only the ~60g of ESC boards relocated; props ride at the motors and the harness stays in the pod/booms. The 12-group split above removes the ambiguity — this was a documentation gap, not a math error.

## Packaging clearance (CAD-checked 2026-10-13, pack at [-96,+36]x[-74,+18]x[-24,+24])
- **Gimbal/camera: CLEAR.** All 12 gimbal parts miss the pack in Y (gap = 10mm: pack bottom -74 vs gimbal top -84). Constraint: tray floor ≤3mm, no fasteners protruding below tray inside X[-63,+69]/Z[-24,+24]; camera ball mount routes to pod keel, not through tray.
- **FC stack: RELOCATED.** Old FC station X[-91,-7] sat inside the slide corridor → moved to nose bay X[109,193]. Pod bay fits [109,193]; requires nose-bay hatch in pod shell (add to print list: 1x FC hatch).
- **ESCs: RELOCATED.** 4-in-1 → X[110,155] beside FC; rear ESC → X[160,195]/Z[35,60]. Both clear of pack and of each other (Z-separated).
- Pod shell overlap with pack is by design (battery lives inside pod).

## CAD deltas vs stock (all in V1_2_FIXED_V2.FCStd)
| Change | Old | New | Status |
|---|---|---|---|
| Battery | 85×45×70 (Part__Feature208, hidden) | 132×48×80 + BMS hump at X[-96,+36] (battery_6S2P_V2) | ENVELOPE |
| Lift motors 4× | bldc clusters ~35 dia (hidden, 28 parts) | MN3510 D44×36 + shaft + X-ring at prop stations | ENVELOPE — replace with vendor STEP after purchase |
| Rear motor | 38×32×32 (pusher_motor, hidden) | AT2814 D36×34 at X[-644,-610] | ENVELOPE — T03b 6S bench test required |
| ESCs | none modeled | 4-in-1 45×45 at X[110,155], rear 35×25 at X[160,195]/Z[35,60] | ENVELOPE |
| Booms | 16mm OD rods (stock) | **OD20x1.0 carbon** (buy list; +saddles at clamps) | SPEC CHANGE |
| Wing / pod / tail / mounts / props | — | untouched (flat wing kept) | stock |

## Files
- `01_REFERENCES/IIT_VYAN/STEP/VTOL Steps/V1_2_FIXED_V2.FCStd` (placements updated r2)
- `.../V1_2_FIXED_V2_FULL.STEP` (31.8 MB; re-export after final envelope swap)
- `.../build_V2_6S_update.py`, `V1_2_V2_build.log`, `V1_2_V2r2_build.log`
