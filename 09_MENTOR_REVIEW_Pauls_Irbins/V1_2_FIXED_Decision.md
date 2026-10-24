# New V1.2 Engineering Spec Sheet
> **SUPERSEDED by `V1_2_V2_Decision.md` (same folder) — 4S/1.7× baseline kept for history. Do not order from this sheet.**

## Aircraft Size and Layout

| Parameter | Value |
|---|---|
| Layout | 4 lift propellers (fixed, open rotors) + 1 rear propeller + V-tail |
| Wingspan | 2473 mm |
| Wing width / wing area | ~324 mm / 0.62 m2 (measured) |
| Body length | 804 mm |
| Overall length | ~2080 mm |
| Lift propellers + motors | 4x open 12 in 2-blade, fixed pointing up, 35xx-class |
| Rear propeller + motor | 11x8 size, AT2814 motor (~1000KV), at tail |
| Tail | V shape, width ~860 mm, two tail arms |

## Weight (early estimate)

| Part | Weight (g) |
|---|---|
| Body (wing + main body + tail + mounts, no rings) | 950 |
| Motors (4x 35xx lift + 1x AT2814 rear) | 570 |
| Speed controller (4-in-1) + propellers + wires | 350 |
| Electronics (flight controller, GPS, radio) | 84 |
| Battery (4S2P, 8.4 Ah Li-Ion) | 620 |
| Camera | 120 |
| Servos + pitot + rods | 180 |

Total = 2870 g — Without camera = 2750 g — Without battery and camera = 2010 g

## Performance Goals

| Parameter | Target |
|---|---|
| Hover lift (vs weight) | at least 1.7x (needs ~1220 g per motor - stand test) |
| Cruise speed | 45-52 km/h (rear propeller only, lift motors off) |
| Dash speed | 70 km/h (short) |
| Flight time | 30-40 min at 45-50 km/h |
| Battery share of weight | ~22% (goal 25%) |
| Weight per wing area | ~4.6 kg/m2 |

## Key Numbers (measured in CAD)

| Number | Value |
|---|---|
| Rings | none (open rotors, brake + align in cruise) |
| Propeller size | 305 mm (12 in, 2-blade) |
| Rear propeller | 279 mm (11x8, folding) |
| Rear motor | AT2814, ~1000KV (locked) |
| Lift motors | 4x 35xx-class ~700KV, 12 in, ~1220 g each (stand test) |
| Battery | 4S2P 8.4 Ah Li-Ion (~620 g) |
