V1.2 VTOL Design Review and Options

Date: Oct 20 2026
Prepared for team review

1. Purpose
This document presents the V1.2 VTOL design review and hardware options. It is for team review. Send feedback to the group. I plan to send this to Ieva tomorrow or the day after tomorrow.

2. Current Configuration
Layout: 4 fixed lift rotors plus 1 rear pusher plus V-tail
Wingspan: 2473 mm
Wing chord: 324 mm
Wing area: 0.62 m2
Body length: 804 mm
Overall length: 2110 mm
MTOW: 3108 g
Battery: 6S2P RS50 9.9Ah 904 g
Lift motors: 4x MN3510 KV360
Rear motor: 1x QX-MOTOR QAA2814 1000KV
Lift props: 4x APC 15x5 or 14x4.8 carbon (T03 test)
Rear prop: 1x APC 11x8 folding

3. Options

3.1 Lift motors and props
None of the published 6S combinations reach the 2.77kgf gate. The gate assumes headroom at 70 percent throttle.
Option A: MN3510 KV360 with 15x5 carbon prop. Published data shows 1.9kgf at 12.5A at full throttle on 6S. Ratio about 2.4x. Lowest current and best hover endurance. Needs 381mm prop so boom wing and tail clearance must be redrawn. No throttle headroom at full thrust.
Option B: MN3510 KV360 with 14x4.8 carbon prop. Published data shows 1.7kgf at 10.6A at full throttle on 6S. Ratio about 2.2x. Smaller CAD change with 356mm prop. Lower ratio so target drops from 2.5x to about 2.2x.
Option C: Keep 12x4.5 and move to larger motor class such as 4014. No 6S table was checked. Only route that keeps 2.5x with 12 inch props. Mass and cost rise. Numbers must come from datasheet and stand test.
Option D: Accept 2.0x as design target. Needs 1.55kgf per motor. Within reach of option B. Gives less margin in gusts and motor transients.

Suggested path: order one motor for option A or B and one for option C. Test both in T03. Buy the other three only for the winner.

3.2 Rear motor
Option A: QX-MOTOR QAA2814 1000KV. Rated 3 to 6S. 92g weight. 50A max continuous current. 700W max continuous power. Published data at 22.2V with APC11x47 shows 19.5A 433W 2180g thrust. This is 2.18kgf. Enough for cruise thrust requirement of 0.71kgf at 70km/h.
Option B: Keep AT2814 on 6S with hard throttle limit. Cheapest but outside the 3S to 4S rating. Burnout risk if limit fails. Not recommended.

Suggested path: Option A. Order one QAA2814 1000KV and test at T03b.

3.3 Radio
Option A: 868MHz ExpressLRS receiver with matching transmitter module. Legal in Europe and better range. Needs new receiver and transmitter.
Option B: Keep 2.4GHz RP1. Cheapest and fine for early tests. Shorter range for a 2.5m aircraft on long flights.

Suggested path: Keep 2.4GHz RP1 for early tests. Decide on 868MHz later if range becomes an issue.

3.4 ESCs
Option A: Keep Hobbywing XRotor Micro 40A 4in1. 20x20mm. 40Ax4. 3-6S. No BEC output. 12g weight. 40x33x5mm size. Lightest option. Needs separate servo BEC. Needs thermal test and current check at full thrust.
Option B: Four single ESCs of about 40A. Easier cooling and failure affects one motor only. Heavier and more wiring.

Suggested path: Option A. Keep 4-in-1 and add separate servo BEC.

3.5 Video
The Caddx Ratel 2 is only a camera. It needs a video transmitter and antenna plus receiving side goggles or monitor. Check allowed output power on 5.8GHz in Latvia before ordering.

3.6 Prop alignment in cruise
Option A: Stopped props with ESC braking no alignment. Simplest. Drag is unknown and must be measured from flight logs. Matches what the endurance derate assumes.
Option B: Folding lift props. Lowest drag. Needs CAD changes at the hubs. Availability in 12 to 15 inch sizes was not checked.
Option C: Pin lock on each prop. Needs four small actuators and four more flight controller outputs. Adds mass and failure mode.
Option D: Position locking motors. Mentioned in ArduPilot forum thread. Example is large motor likely oversized for this aircraft.

Suggested path: V1 with stopped props. Measure drag. Revisit in V2.

4. Corrections between files
The PDFs and the shopping list look like older exports than the markdown files. Regenerate all of them from one corrected source before sending anything outside the team.
Dry airframe gate. Spec review gate 2 says 2060g. Correct value with 904g pack is 2084g. The 2060g comes from the old 928g pack.
Spec PDF weights. Rows add up to 3158g with body 950g but total says 3108g. Body is 900g in markdown. Fix the PDF row.
Mass and CG PDF. Says 3132g total 928g battery CG -139.9mm. Correct values are 3108g 904g CG -140.7mm as in markdown.
Battery capacity. Key numbers say 8.4Ah in spec markdown and PDF. Correct value is 9.9Ah everywhere else.
Lift stand gate. Spec markdown key numbers say 2.80kgf. All other places say 2.77kgf.
Flight time at 50km/h. Review spec markdown say 73min. Spec PDF and shopping list verdict say 63min. One value with derate shown.
Shopping list endurance table. Says 100 and 75min at 45km/h 41 and 30min dash. Review values are 115 and 86min 47 and 35min.
Hover endurance. Review says 27min ideal. Correct value is 31min at 171Wh at 327W.
Boom tube. Shopping list carbon table says 16x1.5mm. Adopted value in review is 20x1.0mm.
Telemetry. Shopping list says SiK 915MHz radio. Review removed it in favor of ELRS backhaul. Settle with the radio decision.
Power module. Listed as 8S 90A. Vendor page says 2S to 14S 90A continuous on board. XT60 and wire are 30A.
4-in-1 ESC. Listed as 5V 3A BEC 30x30mm. Actual is 5V 1.5A and 10V 1.5A 46x40mm.
Print list. Says 59 parts 1.1kg filament. Listed parts are 57, 58 with FC hatch. Printed mass about 852g.
Landing gear. Review says PETG shoe over carbon leg. Shopping list says PETG leg with carbon insert. Pick one design.
Grand total. Says 1421EUR. Line items add to 1423EUR because carbon is 208EUR not 206EUR.

5. Missing from buy list
Video transmitter and antenna for Caddx Ratel 2 which is only a camera. Plus receiving side goggles or monitor.
Radio transmitter with module on chosen band.
Thrust stand with load cell and power meter that logs current. Needed for T03 and T03b.
Balance charger for 6S Li-ion at 1C. Means to build pack nickel strip and spot welder or pack builder.
Fuse or anti-spark connector. Main connector and wire sized for real peak current.
Separate 5V servo supply with margin.
Spare props at least two sets lift props and two pusher props.
Pod and fuselage material. Film quantity checked against roll width.
UV sleeve or paint for booms. Review calls for it but list omits it.
Actuators for prop pin locks only if that option is chosen.

6. Next steps and review tasks
Nothing is frozen yet. The order below keeps spending low until the motor questions are answered.
1. Rebuild mass budget from CAD volumes and slicer weights. Then redo CG and thrust gate.
2. Settle lift motor option and rear motor class from datasheets with 6S data.
3. Run T03 on two lift motor candidates. Log thrust at 50 70 85 and 100 percent current and motor and ESC temperature after a minute at hover thrust.
4. Run T03b on rear motor with current and temperature logging.
5. Order gate-one parts only after steps 1 to 4. Keep dry weight gate at 2084g until budget rebuilt.
6. Keep wind limits and add tethered first hover.

7. Task distribution
Field Modeling Group
Task 1 Verify CAD model V1_2_FIXED_V2.FCStd against spec sheet.
Task 2 Check motor mount fit for MN3510 envelopes.
Task 3 Verify battery tray clearance with gimbal and FC stack.
Task 4 Confirm carbon tube cut lengths wing spar 2x1000mm booms 2x1800mm OD20x1.0.
Task 5 Verify print part dimensions for 57 PETG and PLA parts.
Task 6 Add nose bay hatch for relocated FC stack to print list.
Task 7 Export mass per part from V1_2_FIXED_V2 and replace lumped pod wing and tail masses.
Task 8 Confirm wing area mean chord leading edge station and spar length against span.
Task 9 Run clearance study for 12 14 and 15 inch props.
Task 10 State boom load case.

Electronics Guy
Task 1 Shortlist lift motors and 6S rated rear motor with 6S thrust current mass and price.
Task 2 Define power path main connector wire gauge BMS rating fuse servo BEC and ESC cooling.
Task 3 Decide radio band transmitter and video link including legal limits.
Task 4 Prepare stand for T03 and T03b with load cell power meter and logging.
Task 5 Verify Pixhawk 6C quadplane support for 4 lift plus 1 pusher plus V-tail.
Task 6 Check 6S BMS build for 12x RS50 cells.
Task 7 Test pitot sensor DLVR-L10D.
Task 8 Order avionics Pixhawk 6C M9N GPS RP1 ELRS radio PM07 power module.
Task 9 Power servos from separate BEC.
Task 10 Run ESC temperature test during T03.

Programming Team
Task 1 Set up ArduPlane quadplane frame configuration.
Task 2 Configure motor mixing for 4 lift motors plus 1 pusher.
Task 3 Configure V-tail mixing.
Task 4 Set up transition logic from hover to cruise.
Task 5 Configure failsafe settings.
Task 6 Set up telemetry and ground station.
Task 7 Draft ArduPlane setup for Pixhawk 6C output map for four lift motors pusher ailerons and V-tail DShot airspeed and transition parameters.
Task 8 Check what is possible for stopping lift props in ArduPilot and propose V1 approach.
Task 9 Set up logging for stand tests and flights so cruise drag can be calculated from current.
Task 10 Prepare simulation with final mass and thrust numbers.

8. Initial task
Order gate one parts only after steps 1 to 4. Gate 1 order 1x MN3510 motor 1x 12x4.5 prop 1x 6S ESC 1x 6S pack thrust stand. Bench test 1 motor on stand T03. Gate requires at least 2.77kgf. Do not buy 3 more motors until this passes.
Gate 1b bench test QX-MOTOR QAA2814-1000KV plus APC 11x8 folder on 6S. Must read at least 1.6kgf static and less than 24A sustained. Do not order avionics before this passes.

9. Team message
Everyone can give reviews and feedbacks about the shopping list and the CAD model if there is improvement needed. I keep sharing it.
Questions go in the group.

10. Sources
Holybro PM07 power module page
Reliance INR21700-RS50 at NKON
Hobbywing XRotor Micro 40A 4in1 BLHeli_32 6S page
QX-MOTOR QAA2814 1000KV product page
MN3510 KV700 specifications and thrust tables page
ArduPilot forum thread on aligning and braking props in plane mode
RadioMaster RP1 ExpressLRS 2.4GHz nano receiver page
ExpressLRS hardware selection page
ExpressLRS long range page
