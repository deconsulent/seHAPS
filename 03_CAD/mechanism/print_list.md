# Print List — Concept A (T01 bench)

## Step 0 — T00 dimensional coupon (print FIRST, before mechanism)
- `bearing_pocket_test.stl` (generated) — 20×20×10 mm block with Ø24.00 + Ø15.00 bearing seat and M3 hole
- Measure with calipers: `CAD 24.00 → measured ___ error ___ pass if <0.10 mm`
- If fail: calibrate flow / XY compensation, reprint before housings

## Mechanism parts (once coupon passes)
| Order | STL | Material | Infill | Supports | Inserts |
|---:|---|---|---|---|---|
| 1 | `boom_clamp.stl` | PETG / PA6-CF | 50% gyroid | No (split) | 4×M3 heat-set Ø4.2×5.7 |
| 2 | `hinge_barrel.stl` | PA6-CF preferred | 60% | No | 2×M3 |
| 3 | `servo_mount.stl` | PETG | 40% | Yes (servo pocket) | 4×M3 |
| 4 | `servo_horn_adapter.stl` | PA6-CF | 60% | No | M3 nyloc |
| 5 | `rod_end.stl` ×2 if printing | PA6-CF | 60% | No | M3 |

## Slicer (Prusa/Bambu/Cura)
- Layer 0.2 mm, 4 walls, 5 top/bottom, gyroid, 45° overhang threshold
- PETG 235/75 °C, PA6-CF 260/90 °C dry filament
- No vase mode (OpenGeoDrone workflow is for wings later)

## Post-print
- Ream Ø10 bore with 10 mm drill by hand, test-fit 6802 on shaft (slip fit, not press)
- Tap/inspect M3 inserts, install ball-links, check free rotation before servo install (T01-A)

## Exports location
`BALTIC_TILTROTOR_V1\03_CAD\exports\` after generator run
