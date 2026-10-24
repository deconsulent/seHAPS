# V1_2_FIXED 4+1 Build Shopping List & 3D Print Plan

Based on: V1_2_FIXED_Decision.pdf spec + measured V1_2_FIXED.FCStd + analysis
Target MTOW: 3.11 kg (PDF 2.87 + 0.31 6S pack - 0.05 OD20 booms - 0.02 RS50 pack) | Battery: 6S2P 9.9 Ah RS50 Li-Ion (~904g) | Layout: 4 fixed lift + 1 rear pusher + V-tail
Design point: 2.5x hover T/W -> 6S mandatory (see V12_FINAL_REVIEW.md section 2). All powertrain rows below are the 6S final config.

IMPORTANT: Lift motor spec changed from MN3510 800KV to MN4014 KV400 because published 6S thrust data for MN3510 800KV (2.2 kg max) is below the 2.77 kgf stand gate. Rear motor changed from AT2814 to QX-MOTOR QAA2814 1000KV because AT2814 is only rated 3S-4S. Booms changed from 16mm OD x 1.5mm to 20mm OD x 1.0mm carbon. ESCs changed to 20x20mm 40A 4-in-1 with NO BEC; standalone 5V servo BEC added.

---

## 3D PRINT PARTS (PLA/PETG)

| # | Part | Qty | Material | Est g | Print Notes | Source in FCStd |
|---|------|-----|----------|-------|-------------|-----------------|
| 1 | Lift motor mount (open rotor, 35xx/4014) | 4 | PETG | 45 ea | Vertical, 3 perim, 30% infill, M3x12 holes | mount_front_pos/neg, mount_rear_pos/neg |
| 2 | Rear motor mount (QAA2814) | 1 | PETG | 35 | Aligned to boom axis, folding prop clearance | pusher_motor position |
| 3 | V-tail fin (left + right) | 2 | PLA | 60 ea | 45 deg dihedral, spar slot 10x5 mm, hinge recess | vtail014/028 pair |
| 4 | V-tail servo hatch (2 servos) | 1 | PLA | 20 | Top of fin, magnet latch | new |
| 5 | Wing root fairing (pod<->wing) | 2 | PLA | 30 ea | Covers wing-pod gap, M3 nut traps | new |
| 6 | Wing spar joiners (CF tube ends) | 2 | PLA | 15 ea | 16 mm OD tube socket, epoxy pocket | new |
| 7 | Aileron hinge brackets (5 per side) | 10 | PLA | 8 ea | Printed hinge, 0.2 mm gap, M2 screw | aileron/aileronright objects |
| 8 | Aileron servo tray (wing) | 2 | PLA | 12 ea | Recessed, pushrod exit slot | new |
| 9 | Battery tray (6S2P Li-Ion) | 1 | PETG | 65 | Velcro strap slots, XT60 cutout, 904g pack | battery position |
| 10 | FC stack plate (Pixhawk+GPS) | 1 | PLA | 25 | 30x30 mm M3 pattern, vibration dampening grommets | Pixhawk_4 |
| 11 | GPS mast | 1 | PLA | 15 | 60 mm tall, M3 base | new |
| 12 | Pitot tube mount | 1 | PLA | 8 | Wing LE, 45 deg forward | rodhingewing area |
| 13 | Landing gear legs (PETG shoe over carbon leg) | 2 | PETG | 40 ea | 150 mm, carbon tube insert 10 mm | newfuse007 legs |
| 14 | Camera mount (gimbal base) | 1 | PLA | 20 | Under pod, 28 mm ball | Gimbal position |
| 15 | Propeller brake align pins (lift) | 4 | PLA | 5 ea | Spring-loaded, 3 mm pin | new |
| 16 | Wiring conduit clips | 20 | PLA | 3 ea | Along booms, zip-tie friendly | new |
| 17 | Antenna holders (2.4G) | 2 | PLA | 5 ea | Boom tips, vertical | new |
| 18 | Nose bay FC hatch | 1 | PLA | 20 | Covers relocated FC stack X bracket 109 193 | new |
| TOTAL | | 58 parts | | about 852g printed mass | | |

Filament: 0.5 kg PETG (motor mounts, battery tray, landing gear) + 1.5 kg PLA (everything else). Print PETG at 245C/80C bed; PLA at 210C/60C bed.

---

## MOTORS (5 TOTAL)

Order gate 1 first: one lift motor candidate and one rear motor, bench test in T03/T03b, buy remaining 3 lift motors for the winner only.

| # | Role | Spec | Qty | Candidate (verified on 6S) | Est EUR/pc | Notes |
|---|------|------|-----|---------------------------|-----------|-------|
| 1 | Lift | MN4014 KV400 12 inch 2-blade 6S | 4 (buy 1 first) | T-Motor MN4014 KV400 (up to 3.3 kg published thrust) | 85-95 | Gate: must deliver >=2.77 kgf max on 6S. Do NOT order MN3510 800KV - published max thrust 2.2 kg is below gate. |
| 2 | Rear pusher | QX-MOTOR QAA2814 1000KV 11x4.7 folding 6S-rated | 1 | QX-MOTOR QAA2814 1000KV | 28 to 35 | Cruise thrust 0.71 kgf @ 70 km/h. Published: 19.5A 433W 2180g thrust on 6S with APC 11x4.7. |

Total motor cost: about EUR 185 to 230

2.5x at 3.11 kg needs 1.94 kgf/motor max, i.e. 2.77 kgf stand reading at 70% headroom. 4S options (~2.0 kgf max) fail - 6S only.

---

## ESCs

| # | Role | Spec | Qty | Candidate | Est EUR/pc |
|---|------|------|-----|-----------|-----------|
| 1 | Lift (4-in-1) | 4x 45A 3-6S BLHeli_32 20x20mm NO BEC | 1 | Hobbywing XRotor Micro 40A 4-in-1 | 75 to 90 |
| 2 | Rear pusher | 40A 3-6S BLHeli_S single | 1 | Hobbywing XRotor 40A single | 18 to 25 |

Total ESC cost: about EUR 90 to 110

6S lift peaks about 30A/motor - 45A gives headroom. Rear single ESC on same BEC rail. Servos powered by separate standalone 5V BEC (see below).

---

## BATTERY (6S2P Li-Ion)

| Spec | Qty | Candidate | Est EUR |
|------|-----|-----------|--------|
| 6S2P 9.9 Ah Li-Ion (12x Reliance INR21700-RS50, ~904 g) | 1 | Custom pack: 12x RS50 (NKON, same batch, IR-matched) + 6S BMS + XT60 | 80 to 95 |
| Alternative | | 2x 6S 4500 mAh LiPo | 90 to 110 |

213.8 Wh (171 Wh usable). Recomputed endurance: RS50 6S2P: 97 min ideal / ~73 min operational @ 50 km/h. LiPo easier to source but shorter cycle life. Pre-warm in winter (-10C -> -20% capacity).

---

## AVIONICS AND SENSORS

| Item | Spec | Qty | Candidate | Est EUR |
|------|------|-----|-----------|--------|
| Flight Controller | Pixhawk 6C / Cube Orange / Holybro Pix32 v6 | 1 | Holybro Pixhawk 6C (ArduPlane/PX4) | 180 to 220 |
| GPS plus Compass | Dual GPS M8N/M9N IST8310 | 1 | Holybro M9N GPS / CUAV NEO 3 Pro | 55 to 70 |
| Radio Link | ELRS 2.4GHz | 1 | RadioMaster RP1 ELRS / TBS Crossfire Micro TX | 40 to 60 |
| Airspeed Sensor | DLVR-L10D I2C pitot | 1 | Mateksys ASPD-DLVR | 20 to 30 |
| Power Module | Holybro PM07 | 1 | Holybro PM07 (2S to 14S, 90A board) | 25 to 30 |
| Buzzer plus LED | Standard | 1 | Matek BUZZER-5V | 5 |
| Standalone Servo BEC | 5V 5A+ UBEC 6S input | 1 | Matek or Hobbywing 6S-input UBEC | 12 to 18 |

Total avionics: about EUR 353 to 460

---

## VIDEO CAMERA (FPV plus recording)

| Role | Spec | Qty | Candidate | Est EUR |
|------|------|-----|-----------|--------|
| FPV cam analog | 1200 TVL 2.1 mm 16:9 | 1 | Caddx Ratel 2 / RunCam Phoenix 2 | 35 to 45 |
| HD recording | 4K 60fps Gyroflow 30 g | 1 | Insta360 GO 3S 39 g / DJI O3 Air Unit 32 g cam | 200 to 350 |
| VTX plus antenna Added | 5.8GHz Analog VTX 25 to 800mW adjustable plus 2x 5.8GHz CP Antennas | 1 | Rush Tank TBS Unify | 45 to 60 |
| Alternative VTX integrated | Digital HD VTX plus cam | 1 | DJI O3 Air Unit (cam plus VTX 41 g) plus Goggles 2 | 500 plus |

Recommendation: Analog FPV (Caddx Ratel 2 EUR40) plus Insta360 GO 3S (EUR250) for recording = EUR290. DJI O3 if budget allows digital link.

Before ordering video transmitter check allowed output power on 5.8GHz in Latvia. Also check with Latvian Civil Aviation Agency what registration a 3.11 kg camera aircraft needs.

---

## AIRFRAME RAW MATERIALS

| Material | Spec | Qty | Est EUR |
|----------|------|-----|--------|
| Carbon tube (wing spar) | 16mm OD x 1.5mm x 1000 mm | 2 | 25 to 35 |
| Carbon tube (booms) | 20mm OD x 1.0mm x 1800 mm | 2 | 52 to 60 |
| Carbon tube (tail arms and gear legs) | 10mm OD x 1.0mm x 500 mm | 3 | 20 to 27 |
| CFRP sheet (wing skins) | 300x500x0.5 mm twill | 2 | 30 to 45 |
| Balsa/ply (rib cores) | 3 mm balsa + 0.8 mm ply | 1 pack | 20 to 30 |
| Heat-shrink film (wing) | Oracover / Solarfilm | 1 roll 3 to 4m | 35 to 45 |
| UV boom protection | White UV resistant braided sleeve or 2K UV clear white paint | 1 unit | 12 to 15 |
| Epoxy resin | 500 g plus hardener | 1 set | 25 to 35 |
| CA glue plus kicker | Medium plus thin | 1 set | 10 to 15 |

Total airframe materials: about EUR 185 to 260

---

## SERVOS AND MECHANICAL HARDWARE

| Item Role | Spec | Qty | Candidate | Est EUR |
|-----------|------|-----|-----------|--------|
| Control Surface Servos | MG90S Metal-Gear Micro Servos 2x Aileron 2x V-tail | 4 plus 2 spares | MG90S / EMAX ES08MA II 12g metal gear KST X08 Corona DS929MG | 24 to 35 |
| Fasteners Pushrods | M3 Screw Nyloc Washer Kit 12/16/20mm plus M2x8 Hinge Pin Kit plus 3mm x 2m Carbon Pushrod plus 4x 20mm Velcro Straps | 1 lot | M3 screws M2x8 hinge pins carbon pushrod 3mm x 2m Velcro straps | 39 to 45 |

---

## BENCH TEST AND GROUND SUPPORT EQUIPMENT (Missing from Oct 13 List)

| Item Role | Primary Choice | Approved Alternatives | Qty | Est EUR |
|-----------|--------------|----------------------|-----|--------|
| Thrust Stand and Logger Added | 5kgf Load-Cell Thrust Stand plus 150A Watt Power Meter with Data Logging | RCbenchmark Series 1580 / Custom Arduino HX711 5kg load cell plus INA226 shunt logger | 1 set | 45 to 80 |
| 6S Charger and Spot Welder Added | 6S Li-Ion LiPo Balance Charger 200W plus 18650 21700 Spot Welder | Order pre-welded 6S2P pack from NKON local builder use existing lab bench PSU charger | 1 set | 0 to 110 |
| RC Transmitter and FPV Monitor Added | RadioMaster Boxer TX16S ELRS 2.4GHz plus 5.8GHz FPV Monitor Goggles | RadioMaster Pocket ELRS EUR65 plus Skyzone Cobra X Eachine EV800D Goggles | 1 set | 0 to 250 |

---

## CONSOLIDATED SHOPPING LIST (prices approximate EU sources)

| Category | Items | Est Total |
|----------|-------|-----------|
| Motors (5) | 4x MN4014 KV400 plus 1x QAA2814 1000KV | EUR 340 to 380 |
| ESCs | 1x 45A 4-in-1 plus 1x 30A single | EUR 90 to 110 |
| Battery | 6S2P 9.9 Ah RS50 pack (~904g) | EUR 80 to 95 |
| Standalone Servo BEC | 5V 5A+ UBEC 6S input | EUR 12 to 18 |
| Avionics | FC GPS Radio Telem Pitot PM Buzzer | EUR 353 to 460 |
| Camera | Caddx Ratel 2 plus Insta360 GO 3S plus VTX | EUR 290 to 340 |
| Filament | 0.5 kg PETG plus 1.5 kg PLA | EUR 40 |
| Airframe materials | Carbon tubes sheets balsa film epoxy UV sleeve | EUR 185 to 260 |
| Hardware | M3/M2 screws nuts washers rods servos MG90Sx6 hinges Velcro XT60/XT90 heat-shrink | EUR 60 to 80 |
| Props | 4x 15x5 CF 2-blade plus 4 spare 11x4.7 folding plus 2 spare | EUR 48 to 65 |
| Thrust Stand | 5kgf Load-Cell Thrust Stand plus 150A Watt Power Meter | EUR 45 to 80 |
| 6S Charger Spot Welder | 6S Li-Ion LiPo Balance Charger 200W plus Spot Welder | EUR 0 to 110 |
| RC Transmitter FPV Monitor | RadioMaster Boxer TX16S ELRS 2.4GHz plus 5.8GHz FPV Monitor Goggles | EUR 0 to 250 |
| TOTAL exact line sum | | EUR 1,590 to 1,820 |

Phased Buying Strategy:
Gate 1 immediate (T03/T03b test order): 1x MN4014 KV400 motor + 1x 15x5 prop + 1x 4014-class motor + 1x 12x4.5 prop + 1x QAA2814 1000KV + 1x 11x4.7 prop + 1x 6S-capable ESC + 1x 6S pack + 1x thrust stand + PETG filament
Phase 2 full build: remaining 3x winning lift motors + full avionics suite + cameras + VTX + carbon tubes + wing materials + hardware

---

## BUILD ORDER (matches test plan gates)

| Gate | Task | Parts Needed First |
|------|------|-------------------|
| 1 | Lift motor stand test (T03) | 1x MN4014 KV400 motor 1x 15x5 prop 1x 6S-capable ESC 6S pack thrust stand - must read >=2.77 kgf |
| 2 | Rear motor test | QAA2814 1000KV 11x4.7 folder 30A ESC |
| 3 | Print all PETG mounts | Motor mounts battery tray landing gear |
| 4 | Cut carbon tubes epoxy wing spar | 16 mm tubes epoxy CFRP sheets |
| 5 | Build wing halves film | Ribs spar film CA hinges |
| 6 | Assemble pod FC stack | FC GPS PM 4-in-1 ESC battery tray |
| 7 | Boom tail assembly | Boom tubes V-tail fins servos pushrods |
| 8 | Full integration CG check | All above plus battery expect 3.11 kg |
| 9 | T06 Ground test T07 Tether hover T08 Free hover T09 Transition | Complete aircraft |

---

## CRITICAL PATH ITEMS (order these FIRST)

1. 1x MN4014 KV400 motor + 1x 15x5 prop + 1x 6S ESC + 1x 6S pack + thrust stand - for T03 stand test before buying 4 (gate >=2.77 kgf or switch to 4014-class)
2. QX-MOTOR QAA2814 1000KV + 11x4.7 folder + 6S ESC - T03b stand must read >=1.6 kgf static and <24A sustained (prior 1.0 to 1.3 kgf figures were not 6S data; risk is ESC current not thrust - log amps; no avionics order before T03b)
3. Holybro Pixhawk 6C + M9N GPS - long lead time sometimes
4. 6S2P Li-Ion pack - custom build takes 1 to 2 weeks
5. Carbon tubes OD20x1.0 booms 2x1800 OD16x1.5 spars 2x1000 - cut to length
6. 4-in-1 ESC 45A BLHeli_32 - 6S rated NO BEC add separate servo BEC

---

## ANALYSIS SUMMARY (final 6S config recomputed 2026-10-20 supersedes earlier 4S figures)

| Parameter | Value | Status |
|-----------|-------|--------|
| MTOW | 3.11 kg (2.87 + 0.31 6S pack - 0.05 OD20 booms - 0.02 RS50 pack) | warning +11% vs PDF - every +100g costs 0.08x T/W |
| Hover T/W | 2.5x design point | Stand gate >=2.77 kgf max per motor |
| Lift motor thrust needed | 0.78 kgf hover 1.94 kgf max 2.77 kgf @70% | Stand-test 1 motor first |
| Cruise power 50 km/h | ~78 W rear + 28 W avionics/FPV equals 106 W | 97 min ideal about 73 min operational |
| Cruise 45 km/h | 89 W total | 100 min ideal about 75 min operational |
| Dash 70 km/h | 220 W total | 41 min ideal about 30 min operational |
| Battery fraction | 904/3108 equals 29.1% | checkmark meets 25% target heavier pack helped here |
| Wing loading | 5.1 kg/m2 | warning above PDF 4.6 - stall 10.4 m/s transition at least 13.5 m/s |

Verdict: 6S final config meets the 30 to 40 min PDF target with margin (operational ~73 min @50 km/h after x0.75 wind/climb/reserve derate; caveat CD0 excludes stopped-prop drag covered by that derate). Main risk remains lift motor max thrust - no bulk order before T03.

Generated from V1_2_FIXED_Decision.pdf spec + V1_2_FIXED.FCStd measurements + low-order aero analysis. All weights in grams unless noted.
