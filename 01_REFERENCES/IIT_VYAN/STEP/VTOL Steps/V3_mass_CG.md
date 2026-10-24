# V3 Mass & CG

- Source CAD: `V1_2_FIXED_V2.FCStd`
- Built UTC: `2026-10-24T12:31:36.779652+00:00`
- Lift prop selector: `431.8 mm` (Preset 17x?)
- Datasheet citation status: network fetch unavailable in this execution environment; values used as configured in script inputs and explicit constants.

## Part table

| Name | Label | MassG | X station (mm) | Source |
|---|---|---:|---:|---|
| pusher_prop | pusher_prop | 20.000 | -618.000 | V2 |
| battery_6S2P_V2 | battery_6S2P_V2 [ENVELOPE 132x48x80] | 904.000 | 51.019 | V2 |
| lift_MN3510_V2_0 | lift_MN3510_V2_0 [ENVELOPE D44] | 120.000 | 488.000 | V2 |
| lift_MN3510_V2_1 | lift_MN3510_V2_1 [ENVELOPE D44] | 120.000 | 493.000 | V2 |
| lift_MN3510_V2_2 | lift_MN3510_V2_2 [ENVELOPE D44] | 120.000 | -808.000 | V2 |
| lift_MN3510_V2_3 | lift_MN3510_V2_3 [ENVELOPE D44] | 120.000 | -808.000 | V2 |
| rear_AT2814_V2 | rear_AT2814_V2 [ENVELOPE D36] | 90.000 | -627.000 | V2 |
| esc_4in1_45A_V2 | esc_4in1_45A_V2 | 12.000 | 132.500 | V2 |
| esc_rear_30A_V2 | esc_rear_30A_V2 | 18.500 | 177.500 | V2 |
| V3_lift_motor_MN4014_0 | V3_lift_motor_MN4014_0 [ENVELOPE D48.0x36.0] | 171.000 | 488.000 | CAD |
| V3_lift_motor_MN4014_1 | V3_lift_motor_MN4014_1 [ENVELOPE D48.0x36.0] | 171.000 | 493.000 | CAD |
| V3_lift_motor_MN4014_2 | V3_lift_motor_MN4014_2 [ENVELOPE D48.0x36.0] | 171.000 | -808.000 | CAD |
| V3_lift_motor_MN4014_3 | V3_lift_motor_MN4014_3 [ENVELOPE D48.0x36.0] | 171.000 | -808.000 | CAD |
| V3_lift_prop_disk_0 | V3_lift_prop_disk_0 [D=431.8mm] | 28.000 | 488.000 | CAD |
| V3_prop_brake_pin_housing_0 | V3_prop_brake_pin_housing | MISSING | 488.000 | CAD |
| V3_lift_prop_disk_1 | V3_lift_prop_disk_1 [D=431.8mm] | 28.000 | 493.000 | CAD |
| V3_prop_brake_pin_housing_1 | V3_prop_brake_pin_housing001 | MISSING | 493.000 | CAD |
| V3_lift_prop_disk_2 | V3_lift_prop_disk_2 [D=431.8mm] | 28.000 | -808.000 | CAD |
| V3_prop_brake_pin_housing_2 | V3_prop_brake_pin_housing002 | MISSING | -808.000 | CAD |
| V3_lift_prop_disk_3 | V3_lift_prop_disk_3 [D=431.8mm] | 28.000 | -808.000 | CAD |
| V3_prop_brake_pin_housing_3 | V3_prop_brake_pin_housing003 | MISSING | -808.000 | CAD |
| V3_rear_motor_AT3520 | V3_rear_motor_AT3520 [ENVELOPE D42.0x50.0] | 218.000 | -643.000 | CAD |
| V3_rear_prop_APC_13x6_5 | V3_rear_prop_APC_13x6_5 [D=330.2mm] | 30.000 | -618.000 | CAD |
| V3_esc_lift_4in1 | V3_esc_lift_4in1 [40x33x5] | 12.000 | 135.000 | CAD |
| V3_esc_rear_single | V3_esc_rear_single [50x21.6x12] | 18.500 | 185.000 | CAD |
| V3_ubec_duo | V3_ubec_duo [58x36x8] | 32.000 | 149.000 | CAD |
| V3_pm07 | V3_pm07 [68x50x10] | 43.800 | 162.000 | CAD |
| V3_fuse_125A_holder | V3_fuse_125A_holder | MISSING | 161.000 | CAD |
| V3_xt90s | V3_xt90s | MISSING | 200.000 | CAD |

- **Total mass:** `2674.800 g`
- **CG X:** `-135.400 mm` (target `-135.4`, window `[-143.5,-127.3]`)
- Hand-check reference from request: take-off mass ~3504 g, CG ~-156.7 mm @ battery X=-30, battery near X=+53 for target.

## Data-source notes

- **MN4014_KV400**: `{"diameter_mm": null, "height_mm": null, "mass_g": 171.0, "mass_note": "171 g with cables (150 g bare)", "source": "https://openelab.io/products/tmotor-mn4014-400kv-motor"}`
- **AT3520_KV550**: `{"diameter_mm": null, "height_mm": null, "mass_g": 218.0, "source": "https://store.tmotor.com/product/at3520-long-shaft-fixed-wing-motor.html"}`
- **PM07**: `{"size_mm": [68.0, 50.0, 10.0], "mass_g": 43.8, "source": "https://holybro.com/products/pixhawk-4-power-module-pm07", "source_note": "Requested current model listing: 68x50x10 mm, 43.8 g"}`
- **XT90S**: `{"size_mm": [30.0, 20.0, 16.0], "mass_g": null, "source": "MISSING"}`
- **Fuse_125A_MIDI**: `{"size_mm": [42.0, 12.0, 45.0], "mass_g": null, "source": "MISSING"}`
