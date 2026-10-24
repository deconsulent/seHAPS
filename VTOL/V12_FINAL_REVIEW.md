# V1_2_FIXED — Final Build Review & Buy List (2.5x thrust, Baltic)
**Date:** 2026-10-20 | **Spec:** V1_2_V2_Decision.md | **CAD:** V1_2_FIXED_V2.FCStd (flat wing, 0°)
**MTOW:** 3.11 kg (PDF 2.87 + 0.31 6S pack - 0.05 OD20 booms - 0.02 RS50 pack) | **Layout:** 4 fixed lift + 1 rear pusher + V-tail | **Battery:** 6S2P 9.9Ah RS50 (~904g)

---

## 1. CARBON vs ALUMINUM — simulator verdict

Beam-theory comparison, identical tubes (16mm OD x 1.5mm wall booms/spars, 10x1mm tail/gear).
Script: `04_ANALYSIS/structure/carbon_vs_alu.py`, full table in `tube_carbon_vs_alu.txt`.

| Tube (qty) | Carbon mass | Alu mass | CF tip defl | AL tip defl | CF margin | AL margin |
|---|---|---|---|---|---|---|
| Wing spar 1.0m (x2) | 109g ea | 185g ea | 5.8mm | 11.3mm | 16.0x | 6.0x |
| Boom 1.76m (x2) | 193g ea | 325g ea | 119mm | 234mm | 3.2x | **1.2x** |
| Boom 1.76m (x2), **adopted: OD20x1.0** | **168g ea** | — | **80mm** | — | **3.8x** | — |
| Tail arm 0.5m (x2) | 23g ea | 38g ea | 8.5mm | 16.7mm | 5.8x | 2.2x |
| Gear leg 0.15m (x2) | 7g ea | 12g ea | 0.9mm | 1.7mm | 5.2x | 1.9x |
| **TOTAL** | **663g** | **1119g** | — | — | — | — |

**Saving: 456g (41%) = 16% of MTOW. Stiffness CF = 1.96x AL.**
**Adopted: booms in OD20x1.0 carbon** — 80mm deflection (vs 119), margin 3.8x, and 25g lighter per boom than OD16x1.5 (-50g airframe, -24g pack -> MTOW **3.11kg**). Thin-wall rule: hard saddles + inner sleeves at all 4 motor clamps (crush protection), torque clamps to 1.5 Nm max.

Why carbon, per part:
1. **Booms — CARBON, mandatory.** Alu margin 1.2x is below any safe FoS (gust + motor-out transient snaps it), and 234mm tip flex risks prop strike on wing/tail and couples into the FC gyro loop. Carbon gives 3.2x + halves flex. This alone kills aluminum.
2. **Wing spars — CARBON.** 150g saved at the worst place (span mass raises roll inertia). Deflection 5.8 vs 11.3mm keeps aileron gaps constant.
3. **Tail arms — CARBON.** 30g saved at the tail = about 90g of nose ballast avoided (long moment arm). Alu margin 2.2x looks OK but fails the CG argument.
4. **Gear legs — either, carbon preferred.** Loads tiny; carbon saves 9g and won't permanently bend on a hard landing (alu 6061 yields and stays bent). Keep the PETG shoe over it for abrasion.
5. **Motor-mount cross-rods (your 2-rod idea) — REJECTED, both materials.** 2x alu rods + 4 clamp brackets = about 330g vs 4x printed PETG mounts 180g. 2x carbon rods + brackets = about 240g, still heavier + adds clamp slip failure mode + galvanic isolation hassle. Printed mounts win on weight, vibration damping, and part count.

Baltic-specific: coastal salt + humidity -> bare alu needs anodize AND isolation tape wherever it touches carbon (galvanic cell). Carbon is inert; only needs UV sleeve/paint on booms (epoxy matrix degrades in sun). Cold -10C: both fine.

**Verdict: full carbon tube airframe. No aluminum primary structure.**

---

## 2. THRUST 2.5x — motor verdict (6S required)

At updated 3.11kg (RS50 6S2P pack): hover per motor 7.6N (0.78kgf). 2.5x -> max 1.94kgf/motor; at 70% throttle headroom -> stand must read **>=2.77kgf max**.
MN3510-800KV on 4S peaks about 1.8-2.2kgf -> **fails**. 4S is dead for 2.5x. **6S mandatory.**
MN3510 KV360 on 6S published max thrust ~1.9kgf with 15x5 prop — below the 2.77kgf gate. Option C 4014-class motor with 12x4.5 is the only route that keeps 2.5x. Test both candidates in T03 before buying all four lift motors.

---

## 2b. ENDURANCE — final config recomputed (this was missing)

6S2P RS50 9.9Ah = 213.8Wh, 80% usable = 171Wh. Riga-mean air (rho=1.260), +28W avionics/FPV/camera load. Script: `04_ANALYSIS/aerodynamics/` rerun 2026-10-20.

| Speed | Rear power | Total | Ideal still-air | Operational (~x0.75 wind/climb/reserve) |
|---|---|---|---|---|
| 45 km/h | 61W | 89W | 115 min | **~86 min** |
| 50 km/h | 78W | 106W | 97 min | **~73 min** |
| 52 km/h | 86W | 114W | 90 min | **~68 min** |
| 70 km/h dash | 192W | 219W | 47 min | **~35 min** |
| Hover (all 4) | 299W | 327W | 27 min | n/a (hover phases are minutes) |

Honest caveats: CD0=0.045 excludes stopped-prop drag from the 4 braked 12" lift rotors — real cruise burn is higher, which is exactly what the x0.75 derate is for. Even derated, the 30-40 min PDF target is met with margin at 45-52 km/h. Winter -10C: Li-Ion capacity -20% -> derate operational numbers by another ~20% (about 50 min @50 km/h).

---

## 3. EXACT BUY LIST (with reason per line)

### Motors (5) — test 1 lift motor on stand BEFORE buying 4

| # | Exact item | Qty | ~€/ea | Why this one |
|---|---|---|---|---|
| M1 | MN4014 KV400 (alt: iFlight XING 3510-800KV / 4014-class 400 to 500 KV) | 4 order 1 plus 1 first | 85 to 95 | KV400 on 6S + 15x5 CF peaks ~3.3kg -> gate is 2.77kgf stand reading; T03 decides between KV360 and 4014-class before buying remaining 3. Do NOT order MN3510 800KV — published max thrust 2.2kg is below gate. |
| M2 | QX-MOTOR QAA2814-1000KV (spec-locked, 3 to 6S rated) | 1 | 28 to 35 | Dash needs 0.71kgf @70km/h; **T03b gate (new): static >=1.6kgf on 6S** — prior 1.0 to 1.3kgf figures were not 6S data. No avionics order before T03b. |

Motors subtotal: **~€185 to 230**

### ESCs

| # | Exact item | Qty | ~€ | Why |
|---|---|---|---|---|
| E1 | Hobbywing XRotor Micro 40A 4-in-1, 3-6S, BLHeli_32, 20x20mm, NO BEC | 1 | 75 to 90 | One board for 4 lift motors = 3 fewer failure points; 45A covers KV400 bursts on 6S; NO onboard BEC so servos need separate 5V BEC |
| E2 | Hobbywing XRotor 30A to 40A single, 3-6S | 1 | 18 to 25 | Rear pusher independent (can kill lift ESC in cruise, keep rear alive) |

ESC subtotal: **~€90 to 110**

6S lift peaks about 30A/motor — 45A gives headroom. Rear single ESC on same BEC rail. Servos powered by separate standalone 5V BEC.

### Battery (6S2P Li-Ion)

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| 12x Reliance INR21700-RS50 (NKON, same batch, IR-matched) + 6S BMS + XT60 (6S2P 9.9Ah, 213.8Wh, ~904g) | 1 pack | 86 | Tabless 70A/4mOhm — worst punch ~53A/cell brief, cruise 2.5A. Cells EUR4.65 ea (EUR55.80/12) + BMS/materials ~30. BMS 100A+ burst or charge-only + fuse (punch ~105A pack). Charge <=1C. Pre-warm pack. |

### Avionics

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| Holybro Pixhawk 6C | 1 | 195 | ArduPlane quadvtolan support (4 lift + 1 pusher + V-tail), dual IMU |
| Holybro M9N GPS + compass | 1 | 55 | M9N acquires faster on Baltic overcast vs M8N; mast-mount away from 6S noise |
| RadioMaster RP1 ELRS 2.4GHz | 1 | 45 | EU-legal 2.4GHz, telemetry backhaul so no separate SiK modem |
| Mateksys ASPD-DLVR-L10D pitot | 1 | 25 | Transition logic needs airspeed (GPS speed lies in 6m/s Baltic headwind) |
| Holybro PM07 PDB (2S to 14S, 90A board) | 1 | 28 | Single power hub for 4-in-1 + rear ESC + servos, current sensing for endurance logging. Upgrade main battery lead from 14AWG/XT60 for full-thrust tests. |
| Standalone 5V servo BEC | 1 | 12 to 18 | Mandatory: Micro 40A 4-in-1 has NO BEC. Four MG90S servos can pull more than 1.5A together when loaded. |
| Matek 5V buzzer | 1 | 5 | Lost-model + arming tones |

Avionics subtotal: **~€353 to 365**

### Camera

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| Caddx Ratel 2 analog 2.1mm | 1 | 40 | 0.01lux low-light for Baltic winter afternoons; analog = zero pairing, any goggles |
| Insta360 GO 3S (39g) | 1 | 250 | 4K + Gyroflow stabilization at 39g; detachable for test flights without cam (3.06kg) |
| 5.8GHz Analog VTX plus 2x 5.8GHz CP Antennas | 1 set | 45 to 60 | Mandatory: Caddx Ratel 2 has no transmitter. Verify Latvia 5.8GHz ERP limits. |

Camera subtotal: **~€290 to 340**

### Props

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| APC 15x5 MR or 14x4.8 MR 2-blade (CW+CCW pairs) | 4 sets plus spares | 48 to 65 | Stiff glass-nylon holds pitch at 2.8kgf load. T03 test props for KV360 motor selection. |
| APC 11x4.7 folding pusher | 3 | 24 to 36 | Matches QAA2814 published test prop on 6S. Matches QAA2814 published test table. |

Props subtotal: **~€72 to 101**

### Filament (PLA mostly, PETG only x3 reasons)

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| eSUN PLA+ 1.75mm, 1.5kg | 1.5kg | 25 | 80% of parts: fairings, hinges, trays, fins, hatches, mounts (non-heat), clips — PLA is stiffer than PETG (less flex in hinge gaps), prints without enclosure |
| eSUN PETG 1.75mm, 0.5kg | 0.5kg | 15 | ONLY: (1) 4x motor mounts — motor cans 80-100C > PLA Tg 55C, PETG Tg 80C; (2) battery tray — electrolyte + 904g structural + XT60 heat; (3) gear legs — landing impact, PETG doesn't shatter like PLA |

Filament subtotal: **~€40**

### Carbon (no aluminum — see section 1)

| Exact item | Qty | ~€ | Why carbon |
|---|---|---|---|
| Pultruded tube 20mm OD x 1.0mm x 1800mm (booms — adopted) | 2 | 52 | section 1: 80mm flex, margin 3.8x, -50g vs OD16; hard saddles at clamps |
| Pultruded tube 16mm OD x 1.5mm x 1000mm (spars) | 2 | 30 | section 1: saves 150g span mass, halves flex |
| Pultruded tube 10mm OD x 1mm x 500mm (tail arms) | 2 | 18 | section 1: tail weight costs 3x in nose ballast |
| CFRP sheet 0.5mm 300x500 twill | 2 | 35 | Wing skins: stiffness per gram unbeatable; alu sheet same size = 4x weight |
| 3mm balsa + 0.8mm ply pack (rib cores) | 1 | 25 | Ribs: balsa shear web + ply caps — lighter than any printed rib |
| Oracover 1m roll | 1 | 18 | Film skin over ribs: 60g/m2 vs 500g/m2 printed shell |
| Epoxy 500g + hardener | 1 set | 30 | Spar bonding; CA goes brittle at -10C, epoxy doesn't |

Carbon/materials subtotal: **~€206**

### Hardware

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| MG90S metal-gear servos | 4 plus 2 spares | 24 to 35 | Matches Vyan CAD envelopes; metal gears survive V-tail flutter; spares critical in one-shot order |
| M3 screw kit (12/16/20) + nylocs + washers | 1 | 15 | Nylocs mandatory — 6S vibration loosens plain nuts |
| M2x8 kit (hinges) | 1 | 8 | Aileron hinge pins |
| Carbon rod 3mm x 2m (pushrods) | 1 | 10 | Pushrods: carbon doesn't stretch like piano wire guides |
| Velcro straps 20mm | 4 | 6 | Battery retention (904g at 2.5x punch-outs) |
| XT90S anti-spark connectors plus 125A automotive blade fuse plus 12AWG silicone wire plus pure nickel strip | 1 kit | 25 to 35 | Mandatory: PM07 stock XT60/12AWG wire only rated 30A continuous; 6S pack peak ~105A |
| Wire/heat-shrink kit 14AWG/20AWG | 1 | 20 | 6S lift peaks ~30A/motor — 20AWG signal, 14AWG battery |

Hardware subtotal: **~€91 to 101**

### Bench Test and Ground Support Equipment

| Exact item | Qty | ~€ | Why |
|---|---|---|---|
| 5kgf Load-Cell Thrust Stand plus 150A Watt Power Meter with Data Logging | 1 set | 45 to 80 | Required immediately to execute T03 and T03b |
| 6S Li-Ion LiPo Balance Charger 200W plus 18650 21700 Spot Welder | 1 set | 0 to 110 | Order pre-welded 6S2P pack from NKON local builder OR check if lab already has charger/spot welder |
| RadioMaster Boxer TX16S ELRS 2.4GHz plus 5.8GHz FPV Monitor Goggles | 1 set | 0 to 250 | Omit if team already owns ELRS handset and monitor/goggles |

Bench/ground support subtotal: **~€45 to 250**

### GRAND TOTAL: **€1,423** (line-item sum; ±8% vendor spread -> budget €1,310 to 1,540)

Phased Buying Strategy:
Gate 1 immediate (T03/T03b test order): 1x MN4014 KV400 motor + 1x 15x5 prop + 1x QAA2814 1000KV + 1x 11x4.7 prop + 1x 6S-capable ESC + 1x 6S pack + 1x thrust stand + PETG filament
Phase 2 full build order: remaining 3x winning lift motors + full avionics suite + cameras + VTX + carbon tubes + wing materials + hardware

---

## 4. EXACT 3D-PRINT LIST (58 parts, PLA unless marked PETG)

| # | Part | Qty | Mat | Why this material |
|---|---|---|---|---|
| 1 | Lift motor mount 35xx | 4 | **PETG** | Motor heat 80-100C; PLA creeps at 55C Tg |
| 2 | Rear motor mount QAA2814 | 1 | **PETG** | Same heat + folding-prop strike loads |
| 3 | Battery tray 6S2P + XT60 slot + straps | 1 | **PETG** | 904g crash load + electrolyte + connector heat |
| 4 | Gear leg shoe (over carbon leg) | 2 | **PETG** | Impact: PETG yields, PLA shatters |
| 5 | V-tail fin L/R (45 deg dihedral, spar slot) | 2 | PLA | No heat; PLA stiffer -> hinge gaps stable |
| 6 | V-tail servo hatch | 1 | PLA | Snap fit, no load |
| 7 | Wing root fairing L/R | 2 | PLA | Aero only |
| 8 | Spar joiner (16mm socket + epoxy pocket) | 2 | PLA | Bonded joint, no direct heat |
| 9 | Aileron hinge bracket (5/side) | 10 | PLA | 0.2mm printed hinge prints cleaner in PLA |
| 10 | Aileron servo tray | 2 | PLA | Recessed, cool |
| 11 | FC stack plate (30.5mm + grommets) | 1 | PLA | Isolated, <40C |
| 12 | GPS mast 60mm | 1 | PLA | No load |
| 13 | Pitot mount (LE) | 1 | PLA | Ambient temp |
| 14 | Camera ball mount 28mm | 1 | PLA | 39g cam only |
| 15 | Prop brake pin housing | 4 | PLA | Spring pin, low force |
| 16 | Boom conduit clip | 20 | PLA | Zip-tie only |
| 17 | Antenna holder | 2 | PLA | Tip, vertical |
| 18 | Nose bay FC hatch | 1 | PLA | Covers relocated FC stack X bracket 109 193 |

Print: PLA 210/60, 0.2mm, 3 walls, 25% gyroid, no enclosure. PETG 245/80, 0.2mm, 4 walls, 30% gyroid.

---

## 5. GO / NO-GO GATES BEFORE FIRST HOVER

1. **T03 stand:** 1x MN4014 KV400 + APC 15x5 or 14x4.8 + 6S must read >=2.77kgf. Below -> switch to 4014-class, do not buy 3 more.
2. **T03b stand (new):** QX-MOTOR QAA2814-1000KV + APC 11x4.7 folder on **6S** must read >=1.6kgf static **and log current at that point — pass requires <24A sustained** (40A ESC with headroom; the 4S-figure risk was current, not thrust). Prior 1.0 to 1.3kgf figures were not 6S data. No avionics order before T03b.
3. **Weigh-in:** airframe dry (no batt/cam) must be <=2084g (reconciled V2 budget). Every +100g costs 0.08x T/W.
4. **CG:** 25-30% chord (X in [-143.5,-127.3]) via **sliding battery tray** — see `04_ANALYSIS/mass/V2_mass_CG.md` (pack fwd station, FC/ESC relocated, gimbal 10mm keep-out). Bench-balance at T06; tray needs >=200mm slide + nose-bay hatch for relocated FC stack.
5. **Baltic wind:** hover tests only steady <6m/s, gust spread <3m/s. Gust 10m/s ≈ stall — no T08/T09.

Review and sign off each line — then we freeze the list and order gate-1 parts (1 motor + 6S ESC + props + PETG).
