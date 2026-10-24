# New V1.2 Engineering Spec Sheet — V2 (final config, 6S / 2.5x)

## Aircraft Size and Layout

| Parameter | Value |
|---|---|
| Layout | 4 lift propellers (fixed, open rotors) + 1 rear propeller + V-tail |
| Wingspan | 2473 mm |
| Wing width / wing area | ~324 mm / 0.62 m2 (measured, flat 0° — V1_2_FIXED_V2.FCStd) |
| Body length | 804 mm |
| Overall length | ~2110 mm |
| Lift propellers + motors | 4x open 15x5 or 14x4.8 carbon in 2-blade, fixed pointing up, MN3510 KV360, 6S |
| Rear propeller + motor | 11x8 folding, QX-MOTOR QAA2814-1000KV (3 to 6S rated), at tail |
| Tail | V shape, width ~860 mm, two tail arms (carbon, see §1 of review) |

## Weight (updated — 6S2P pack)

| Part | Weight (g) |
|---|---|
| Body (wing + main body + tail + mounts, no rings, OD20x1.0 booms) | 900 |
| Motors (4x MN3510 lift + 1x QAA2814 rear) | 570 |
| Speed controller (45A 4-in-1 + 30A rear) + propellers + wires | 350 |
| Electronics (flight controller, GPS, radio) | 84 |
| Battery (6S2P 9.9Ah RS50 Li-Ion) | 904 |
| Camera | 120 |
| Servos + pitot + rods | 180 |

Total = 3108 g — Without camera = 2988 g — Without battery and camera = 2060 g

## Performance Goals

| Parameter | Target |
|---|---|
| Hover lift (vs weight) | 2.5x (needs ~2.77 kgf per motor max on stand - T03 gate; T03b: QAA2814 >=1.6 kgf on 6S) |
| Cruise speed | 45-52 km/h (rear propeller only, lift motors braked + aligned) |
| Dash speed | 70 km/h (short, ~30 min pack-equivalent) |
| Flight time | 30-40 min at 45-50 km/h (recomputed operational: ~73 min @50) |
| Battery share of weight | ~29.1% (goal 25% — met) |
| Weight per wing area | ~5.05 kg/m2 |

## Key Numbers (measured in CAD — V1_2_FIXED_V2)

| Number | Value |
|---|---|
| Rings | none (open rotors, brake + align in cruise) |
| Propeller size | 305 mm (12x4.5 in, 2-blade, APC stiff) |
| Rear propeller | 279 mm (11x8, folding) |
| Rear motor | QX-MOTOR QAA2814-1000KV (~1000KV, locked) |
| Lift motors | 4x MN3510 KV360, 6S, 15x5 or 14x4.8 carbon prop, >=2.77 kgf stand (envelopes D44 in CAD) |
| Battery | 6S2P 9.9Ah RS50 Li-Ion, 132x48x80 envelope (~904 g), sliding tray |
| CG | 25-30% chord, closed in CAD r2 (pack X=-30, FC/ESC relocated, gimbal 10mm keep-out) - bench-verify at T06 |
| Structure | Full carbon tubes (booms/spars/arms), PLA + PETG prints (mounts/tray/gear in PETG) |
