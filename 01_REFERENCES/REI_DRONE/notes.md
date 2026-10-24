# REI Drone — Study Notes (DAY 2)
**Source:** `01_REFERENCES/REI_DRONE/source/` cloned from https://github.com/rootcastleco/rei-drone  
**Date:** 2026-09-13  
**Status:** Reference study complete — Gate 1 partial (REI portion)

## 1. What was inspected
- `README.md` (179 lines): specs, architecture, state machine
- `matlab/` (11 files): `flight_dynamics.m`, `tilt_transition.m`, `aerodynamics_analysis.m`, `motor_propulsion.m`, `weight_cg_analysis.m`, `main_simulation.m`, `pid_controller.m`, `battery_endurance.m`, `structural_loads.m`, `telemetry_link_budget.m`, `mission_planner.m`
- `firmware/src/`: `main.cpp`, `flight_controller.cpp/.h`, `tilt_mechanism.cpp/.h`, `estimator.cpp/.h`, `sensors.cpp/.h`, `pid.cpp/.h`, `config/vehicle_params.h`
- `paper/paper.pdf` (10 pages, Ayribas 2026-04-23): design, modeling, sim-vs-test table
- `figures/`: `conceptual_design.png`, `exploded_diagram.png` only — **no CAD/STEP/STL found**

## 2. Reference specs (as reported, NOT verified)
- 1000 mm wingspan, 650 mm length, 180 mm height
- 2.5 kg MTOW, ~2.0 kg modeled mass in sim, 500 g payload
- 4x 2216 880KV, 10x4.5 3-blade, 6S 5000 mAh
- Pixhawk 6C / Cube Orange, PX4/ArduPilot compatible, MAVLink, QGC
- 30-40 min claimed flight, 40-60 km/h cruise, 100 km/h max

## 3. Questions from Guide Sec 2

### What equations are used?
- Rigid-body translation: `m(u_dot + qw - rv)=Fx` etc. (paper eq 1-3, `flight_dynamics.m:118-120`)
- Euler rotation: `Ixx*p_dot + (Izz-Iyy)*q*r = L` etc. (`flight_dynamics.m:123-125`, paper eq 4-6)
- Aero: `L=0.5*rho*V^2*S*CL`, `D=0.5*rho*V^2*S*CD`, `CD=CD0+CL^2/(pi*e*AR)` (paper eq 7-9, `aerodynamics_analysis.m:27-40`)
- Rotor: `T=CT*rho*n^2*Dp^4`, `Q=CQ*rho*n^2*Dp^5` (`motor_propulsion.m:45-49`, paper eq 10-11)
- Battery: `Vterm=VOC(SOC)-I*Rint`, `SOC_dot=-I/Qtot` (paper eq 12-13)
- Tilt decomposition: `Tv=T*cos(alpha)`, `Th=T*sin(alpha)` (paper eq 14-15, `tilt_transition.m:70-71`)
- Lift-curve: `CL_alpha=2*pi*(AR/(AR+2))`, stall cap `CL_max=1.35`, post-stall decay `exp(-0.08*da^2)`

### How is the aircraft modelled?
- 12-state 6-DOF: `[x,y,z,u,v,w,phi,theta,psi,p,q,r]` in NED + body frame (`flight_dynamics.m:33-35`)
- Mass 2.0 kg, `Ixx=0.015, Iyy=0.015, Izz=0.025 kg.m2` (X-quad estimate)
- Cascaded PID: outer attitude P (`Kp_att=5.0`) → inner rate PID (Roll/Pitch `6.0/1.0/0.15`, Yaw `4.0/0.5/0.1`) + altitude PID `3.0/0.5/1.5` (`flight_dynamics.m:48-58`, `flight_controller.cpp:56-94`)
- Wing: `S=0.12 m2`, `AR=8.33`, `e=0.78`, `CD0=0.035`, `CL_alpha=4.5` (`tilt_transition.m:22-26`)
- Mass/CG: 29-component table, origin at nose, sliding battery tray at x=290 mm for CG trim (`weight_cg_analysis.m:39-69`)

### What assumptions are made?
- Rigid body, symmetric X-quad inertia, small-angle rotation matrix simplifications
- Static prop coefficients `CT=0.012`, `CP=0.0045`, `RPM=KV*V*0.85`, simplified current `I=I0+Q/(R*10)` — low-order, not BEMT
- Steady aero, constant `rho=1.225`, no ground effect, no propwash-on-wing, no aero-elasticity
- Wind = single 0.5 s gust `[2.0,1.0,0.5] N` at t=7 s only
- Battery first-order equivalent, no temp/aging
- All 4 motors share identical tilt angle (no differential tilt for pitch — noted as future work in `tilt_mechanism.cpp:121-126`)

### How is transition represented?
- MATLAB: timed S-curve `3p^2-2p^3` over 3→8 s (5 s), 0°=vertical → 90°=horizontal, altitude-hold thrust compensation `T_needed_vert/cos(tilt)`, capped at `T_max=32 N` (`tilt_transition.m:50-99`)
- Firmware: airspeed-scheduled state machine `HOVER → TRANSITION_FWD → CRUISE → TRANSITION_REV` with `min_transition_speed=8.0 m/s`, `full_transition_speed=TRANSITION_AIRSPEED_MS`, slew-rate limited `TILT_RATE_DEG_PER_SEC`, S-curve on progress, manual override + `tilt_emergency_hover()` + `tilt_can_transition()` gate (alt≥10 m, 0≤airspeed≤35 m/s) (`tilt_mechanism.cpp:35-167`)
- README mermaid: `Hover → Transition (Forward Command) → Cruise (Airspeed>Stall)` and reverse

### What sensors are assumed?
- M8N GPS/compass (UART/I2C), 915 MHz telemetry (UART), RC SBUS, IMU+baro+mag+GPS via `sensors.cpp`/`estimator.cpp`, power module for voltage/current. No LiDAR, no airspeed sensor explicitly named in README — firmware uses `airspeed_ms` input (implies pitot or GPS-derived, unverified).

### How is motor/tilt control mixed?
- X-quad mixing in `flight_controller.cpp:146-149`: `M0=thr+roll+pitch-yaw` (FL), `M1=thr-roll+pitch+yaw` (FR), etc., clamped 0-1 with `IDLE_THROTTLE`
- Tilt: common angle to all 4 servos, linear PWM map `0°→TILT_SERVO_MIN_US`, `90°→TILT_SERVO_MAX_US` (`tilt_angle_to_pwm`)
- Mode handling resets integrators on mode change; disarmed kills motors

### What failed during real testing?
- No explicit failure log in repo. Paper Table 2 reports sim-vs-measured error 3.7-7.7% (thrust, power, speed, L/D, endurance, transition 4.8 s sim vs 5.2 s meas) except telemetry 18.5 km sim vs 15.2 km meas (17.8% error — install/environment sensitive). No crash report like Underactuated. Treat all “experimental” numbers as **unverified draft claims** until bench-tested.

### Which parts are actually open-source?
- Open: MATLAB suite (MIT/CERN-OHL-S v2 badge), C++ firmware + PlatformIO, paper PDF + figures, README/mermaid docs. License file present (`LICENSE` — CERN-OHL-S v2 per badge, verify before reuse).
- Closed/missing: **No STEP/SolidWorks/STL CAD**, no Pixhawk parameter files, no raw flight logs, no BOM part numbers. Exploded diagram is PNG only.

### Are CAD files available, or mainly software/control reference?
- **Mainly software/control reference.** No CAD to import into FreeCAD. Figures are renders, not dimensioned drawings. Use for equations, transition logic, and test-table format — NOT for airframe dimensions.

## 4. Classification (per Guide)
**REI = primary systems/control reference. Do NOT make it airframe baseline.**
Critical mismatch: REI is **quad tilt-rotor (4x tilting)**, our V1 is **twin-motor tilt-rotor**. Mixing, inertia, and power numbers do not transfer directly. Extract method, not dimensions.

## 5. What to reuse for V1
1. 6-DOF + S-curve transition pattern for our own twin-motor sim (rescale mass, S, T_max)
2. `tilt_can_transition()` safety gate idea (min altitude + airspeed window)
3. Cascaded PID structure as starting gains for bench tuning (not fly-away values)
4. Thrust-table + power-table format for T02/T03
5. Paper Table 2 format for our own sim-vs-measure comparison
6. Weight/CG spreadsheet structure (29-row template → adapt to twin-motor BOM)

## 6. Confidence
- Systems/control logic: **High** (code readable, equations standard)
- Reported performance numbers: **Medium-Low** (no raw logs, draft paper language)
- Airframe/mechanism geometry: **Low** (no CAD, renders only)

## 7. Next
- DAY 3: Vyan STEP → FreeCAD mechanism measurement (primary CAD ref)
- DAY 4: Underactuated failure table (primary test-method ref)
- Do NOT copy REI 1000 mm / 2.5 kg / 4-motor layout into V1 requirements.
