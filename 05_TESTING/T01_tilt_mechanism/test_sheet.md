# T01 — Tilt Mechanism Bench Test (Guide Sec 10) — Concept A

## Build (no aircraft)
```
dummy mass (80-100g) ~ A2212+prop
    |
hinge barrel (Ø32, Ø10 shaft + 2×6802)
    |
boom clamp on Ø16×200 stub
    |
pushrod 95-110 mm M3 ball-links
    |
servo DS3218MG in servo mount (25T horn)
```
Bench rig on plywood/Al extrusion. **No prop, no motor power for T01-A/B.**

## T00 — Bearing pocket coupon (do FIRST)
Print `bearing_pocket_test.stl`, measure:
```
CAD pocket Ø24.00: measured ____ error ____ tol 0.10 pass/fail ____
CAD bore Ø10.00: measured ____ error ____
```
Record: `05_TESTING/T00_component/T00-001.md` — must PASS before housings.

## T01-A — Free movement (manual, no servo power)
ID: `TR-V1-T01-A-001`  
Procedure: disconnect pushrod, rotate barrel by hand 0→90°, feel binding/interference/alignment; reconnect, move servo horn by hand.
Accept: smooth, no binding, no interference with boom, <0.3 mm axial play  
Photos: side + top

## T01-B — Servo movement (powered, dummy mass only)
ID: `TR-V1-T01-B-001`  
Supply: 6.0 V BEC, current meter  
Cycle: 0° → 45° → 90° → 45° → 0° (S-curve optional), 2 s dwell, 5 repeats — NOT rapid  
Record per step: `cycles: servo: supply V: current A: temp °C: backlash °: damage: pass/fail:`  
Inspect: servo temp <60 °C, current <1.8 A stall, backlash <1.0°, no cracking, no ball-link pop  
Video: 10 s per cycle

## T01-C — Repeated cycling
IDs: `TR-V1-T01-C-001` (100), `-002` (500), `-003` (1000) — inspect between  
Accept: after 1000 cycles still <1.0° backlash, no permanent deformation, ball-link wear <0.2 mm, shaft not scored

## Thresholds (from Vyan/REI)
- Backlash link budget: ball-link 2×0.15° + shaft play 0.2° = target <0.8° total
- Tilt range: 0–90° (vertical→horizontal); verify with digital protractor on barrel

## Abort / Underactuated lesson
If chipped/cracked print, current spike, or >1° backlash → STOP, log in `07_FAILURES/`, redesign housing/inserts before T02

## Next gate
Pass T01-A/B/C → authorize **T02 motor/prop thrust stand** (properly restrained, not hand-held) and **T03 tilted-thrust map** 0/15/30/45/60/75/90°
