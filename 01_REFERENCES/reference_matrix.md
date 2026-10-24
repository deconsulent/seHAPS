# Reference Matrix (Guide Sec 6) — live, update after each inspection
| Reference | Architecture | CAD | Simulation | Flight Evidence | Testing Docs | Main Use | Confidence |
|---|---|---|---|---|---|---|---|
| REI Drone | Quad tilt-rotor (4x tilting) | None (renders only) | Strong (6-DOF MATLAB + transition + aero/power) | Claimed (paper Table 2, no raw logs) | Medium (paper + code, no failure log) | Systems/control | High: logic / Low: numbers, geometry |
| Vyan (IIT Bombay) | Hybrid: 4x ducted, front tilt + rear shutoff, inverted V-tail | STEP AP214 measured in FreeCAD 1.1 (hinge barrel Ø50-55, push-plate 161x83x5.1, ducts Ø257-291) + SolidWorks tiltmech (MG90S servo) | None | Design-event only (TechFest) | None | Mechanism/CAD | Medium-High: geometry measured / Low: bearing + tilt range need GUI confirm |
| Underactuated | Servo-less tiltrotor (Vertiq pulse-tilt hinge) | Verify (has CAD, check `NemoFlightController`) | Control (dRehmFlight fork) | Yes (hover ok, crash on speed attempt) | Strong (dated photo journey + failure) | Test/failure study | High: lessons / N/A: mechanism not for V1 |
| OpenGeoDrone | Quad-hover + pusher (NOT tilt-rotor) | Parametric OpenSCAD + STL/3MF | Some (perf table) | Project-dependent | Manufacturing | CAD/printing | High: workflow |

**Key mismatch:** V1 = twin-motor tilt-rotor. None of the four is twin-motor. Extract principles, not dimensions.
