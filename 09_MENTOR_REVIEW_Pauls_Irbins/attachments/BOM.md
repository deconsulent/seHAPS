# Concept A Bench BOM — DAY 6–7 (buy vs print)

## Buy (order before printing — lead time)
| Qty | Part | Spec | Why | Source hint |
|---:|---|---|---|---|
| 1 | Servo | DS3218MG 20 kg·cm 0.14 s/60° @6 V (or JX HV7232MG) — **not MG90S** | Measured Vyan MG90S undersized; twin 10×6 moment needs ≥20 kg·cm | Amazon/Ali |
| 1 | Bearings | 6802-2RS 15×24×5, 2 pcs (or 6802 ZZ) + Ø10×45 mm hardened shaft + 2×M3 shaft collars | Replaces Vyan plain bore Ø32 barrel | Bearings shop |
| 1 | Pushrod | CF tube Ø6×4×110 mm + 2×M3×30 threaded rod + 2× Dubro 2-56 / M3 ball-links (5 mm ball) | Vyan 161 mm → 95–110 mm for V1 buckling | Hobby |
| 1 | Ball-link hardware | M3 nyloc + M3×12, M3 inserts (heat-set) ×8 | Housing + horn mounting |  |
| 1 | Carbon boom stub | Ø16×14 mm tube 200 mm (represents wing boom) | Rig support, not aircraft |  |
| 1 | Dummy mass | 80–100 g bar + M3 clamp (simulates A2212+prop 62 g + 18 g measured in REI) | T01 needs representative load, not live prop |  |
| — | Fasteners | M3×8/12/16, M2×8 servo screws, zip ties |  |  |
| — | Bench | 300×200 mm plywood + 40×40 mm Al extrusion or rig clamp | T01 support structure |  |
| — | Electronics | 6 V 5 A BEC / lab PSU, servo tester or Pixhawk PWM, calipers, IR thermometer | T01-B |  |

## Print (PETG or PA6-CF, 0.2 mm, 4 perimeters, 40–60% gyroid — no vase mode here)
| Part | Qty | File | Time est | Note |
|---|---|---|---|---|
| Boom clamp / hingeback | 1 | `boom_clamp.stl` from generator | ~2.5 h | Split clamp for Ø16 boom, M3 inserts |
| Hinge barrel (motor side) | 1 | `hinge_barrel.stl` | ~1.5 h | Ø32 outer, Ø10 bore, wire slot |
| Servo mount + hingeback mate | 1 | `servo_mount.stl` | ~2 h | DS3218MG footprint 40×20, 25 mm horn radius |
| Servo horn adapter | 1 | `servo_horn_adapter.stl` | ~0.3 h | 25T spline → M3 ball-link |
| Rod ends (if not buying Dubro) | 2 | `rod_end.stl` | ~0.4 h | Print in PA6-CF only as backup |

**Before any print:** run T00 coupon (below) — bearing pocket test `bearing_pocket_test.stl` (20×20×10 block with Ø24 pocket).

## You already have from refs
- `IIT_VYAN/STEP/` + `screenshots/` (mechanism dims)
- REI transition S-curve code for later FC

## Not needed yet
- Motors/ESCs/props (T02 after T01 passes)
- Airframe wing/fuselage/tail (T04–T06)
