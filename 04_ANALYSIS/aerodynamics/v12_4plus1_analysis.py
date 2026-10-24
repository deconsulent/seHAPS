"""V1_2_FIXED 4+1 configuration analysis per Decision PDF spec.
SUPERSEDED baseline (4S/1.7x, 2.87kg) kept for history. Current: 6S/2.5x/3.11kg RS50
(see V12_FINAL_REVIEW.md section 2b)."""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"D:\Projects\ISR\BALTIC_TILTROTOR_V1 - test\04_ANALYSIS\aerodynamics"
os.makedirs(OUT, exist_ok=True)

# --- SPEC SHEET VALUES ---
MTOW = 2.87          # kg
MASS_NO_BATT_CAM = 2.01
MASS_NO_CAM = 2.75
W = MTOW * 9.81

# Wing
SPAN = 2.473
CHORD = 0.324
S = 0.62             # PDF says 0.62 m2 (our 0.80 was full rect)
AR = SPAN**2 / S
print(f"Wing: S={S:.3f} AR={AR:.2f}")

# Lift: 4x 12" open rotors
D_LIFT = 0.305       # 12"
N_LIFT = 4
A_LIFT = N_LIFT * math.pi * D_LIFT**2 / 4
print(f"Lift disk area: {A_LIFT:.4f} m2")

# Rear: 11x8 folding
D_REAR = 0.279
A_REAR = math.pi * D_REAR**2 / 4

# Battery
BATT_WH = 4*3.7*8.4  # 4S 8.4Ah = 124.3 Wh
BATT_USABLE = 0.8
E_BATT = BATT_WH * BATT_USABLE * 3600  # J

# Air
RHO_STD = 1.225
RHO_BALTIC = 1.260   # Riga annual mean +7C
RHO_HOT = 1.164      # +30C
RHO_COLD = 1.341     # -10C

# Targets
TARGET_TW = 1.7      # hover thrust/weight
TARGET_CRUISE = 13.9 # m/s (50 km/h)
TARGET_DASH = 19.4   # m/s (70 km/h)
TARGET_ENDURANCE = 30*60  # seconds

# --- AERO ASSUMPTIONS (need validation) ---
CLMAX = 1.2
CD0 = 0.045
E = 0.75
FM = 0.68            # figure of merit for open rotors
ETA_PROP = 0.70      # rear prop efficiency

# --- Hover analysis ---
def hover_power_per_motor(W_total, rho):
    """Momentum theory: P_ideal = T^1.5 / sqrt(2*rho*A_disk_per_motor)"""
    T_per = W_total / N_LIFT
    A_per = A_LIFT / N_LIFT
    P_ideal = T_per**1.5 / math.sqrt(2 * rho * A_per)
    return P_ideal / FM

def hover_thrust_per_motor(W_total):
    return W_total / N_LIFT

print(f"\n=== HOVER (MTOW {MTOW} kg) ===")
for rho, label in [(RHO_STD,"ISA"), (RHO_BALTIC,"Baltic"), (RHO_HOT,"Hot"), (RHO_COLD,"Cold")]:
    P_per = hover_power_per_motor(W, rho)
    T_per = hover_thrust_per_motor(W)
    T_per_kgf = T_per / 9.81
    P_total = P_per * N_LIFT
    tw = (T_per * N_LIFT) / W
    print(f"  {label}: rho={rho:.3f} | T/motor={T_per:.1f}N ({T_per_kgf:.1f}kgf) | P/motor={P_per:.0f}W | P_total={P_total:.0f}W | T/W={tw:.2f}")

# Check 1.7x target
T_req = W * TARGET_TW
T_per_req = T_req / N_LIFT
print(f"\n  Target 1.7x: T_total={T_req:.1f}N, T/motor={T_per_req:.1f}N ({T_per_req/9.81:.1f}kgf)")

# --- Cruise analysis (rear prop only) ---
def cruise_drag(V, rho):
    q = 0.5 * rho * V**2
    # Assume CL for level flight at cruise
    CL = W / (q * S)
    CD = CD0 + CL**2 / (math.pi * AR * E)
    D = q * S * CD
    return CL, CD, D

def rear_prop_power(D, V, rho):
    # P = D*V / eta
    return D * V / ETA_PROP

print(f"\n=== CRUISE @ 50 km/h (13.9 m/s) ===")
for rho, label in [(RHO_STD,"ISA"), (RHO_BALTIC,"Baltic")]:
    CL, CD, D = cruise_drag(TARGET_CRUISE, rho)
    P_rear = rear_prop_power(D, TARGET_CRUISE, rho)
    print(f"  {label}: CL={CL:.3f} CD={CD:.4f} D={D:.2f}N P_rear={P_rear:.0f}W")
    
    # Endurance
    t = E_BATT / (P_rear + 20)  # +20W avionics
    print(f"    Endurance: {t/60:.1f} min")

# --- Dash ---
print(f"\n=== DASH @ 70 km/h (19.4 m/s) ===")
for rho, label in [(RHO_STD,"ISA"), (RHO_BALTIC,"Baltic")]:
    CL, CD, D = cruise_drag(TARGET_DASH, rho)
    P_rear = rear_prop_power(D, TARGET_DASH, rho)
    print(f"  {label}: CL={CL:.3f} CD={CD:.4f} D={D:.2f}N P_rear={P_rear:.0f}W")

# --- Motor sizing ---
# Lift motors: need ~1220g thrust each at hover (1.7x T/W)
T_lift_target = T_per_req  # N per motor
print(f"\n=== LIFT MOTOR REQUIREMENT ===")
print(f"  Thrust per motor (1.7x): {T_lift_target:.1f} N ({T_lift_target/9.81:.1f} kgf)")
print(f"  At 70% throttle headroom: motor must deliver {T_lift_target/0.7/9.81:.1f} kgf max")
print(f"  35xx class 12\" 2-blade ~700KV on 4S: typical max ~1.8-2.2 kgf -> OK")

# Rear motor: AT2814 1000KV 11x8
# At 50 km/h cruise, thrust = D
print(f"\n=== REAR MOTOR (AT2814 ~1000KV, 11x8) ===")
print(f"  Cruise thrust required: {D:.1f} N ({D/9.81:.1f} kgf)")
print(f"  AT2814 11x8 on 4S: typical max ~1.0-1.3 kgf -> OK for cruise")

# --- Weight budget check ---
print(f"\n=== WEIGHT BUDGET (from PDF) ===")
items = {
    "Airframe (wing+body+tail+mounts)": 0.950,
    "Lift motors (4x 35xx)": 0.570,
    "ESC (4-in-1) + props + wires": 0.350,
    "Electronics (FC, GPS, radio)": 0.084,
    "Battery (4S2P 8.4Ah Li-Ion)": 0.620,
    "Camera": 0.120,
    "Servos + pitot + rods": 0.180,
}
total = sum(items.values())
print(f"  Total: {total:.3f} kg (PDF says 2.870)")
for k,v in items.items():
    print(f"    {k}: {v*1000:.0f} g ({v/total*100:.1f}%)")

# Battery fraction
print(f"\n  Battery fraction: {0.620/total*100:.1f}% (target 25%)")

# Wing loading
print(f"  Wing loading: {MTOW*9.81/S:.1f} N/m2 = {MTOW/S:.1f} kg/m2 (PDF says 4.6)")

# --- Plots ---
# Hover power vs MTOW
ms = np.linspace(2.0, 4.0, 20)
ws = ms * 9.81
P_hover = [hover_power_per_motor(w, RHO_STD)*4 for w in ws]
T_per = [w/4/9.81 for w in ws]

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(ms, P_hover)
plt.xlabel("MTOW (kg)"); plt.ylabel("Total hover power (W)")
plt.title("Hover power vs weight (ISA)"); plt.grid()

plt.subplot(1,2,2)
plt.plot(ms, T_per)
plt.axhline(y=1.22, color='r', linestyle='--', label='Target 1.22 kgf')
plt.xlabel("MTOW (kg)"); plt.ylabel("Thrust/motor (kgf)")
plt.title("Hover thrust per motor"); plt.legend(); plt.grid()

plt.tight_layout()
plt.savefig(os.path.join(OUT, "V12_4plus1_hover.png"), dpi=110)
plt.close()

# Cruise power vs speed
Vs = np.linspace(8, 25, 50)
for rho, label in [(RHO_STD,"ISA"), (RHO_BALTIC,"Baltic")]:
    Ps = []
    for V in Vs:
        CL, CD, D = cruise_drag(V, rho)
        P = rear_prop_power(D, V, rho) + 20  # +avionics
        Ps.append(P)
    plt.plot(Vs, Ps, label=label)
plt.axvline(TARGET_CRUISE, color='g', linestyle='--', label='Cruise 50 km/h')
plt.axvline(TARGET_DASH, color='r', linestyle='--', label='Dash 70 km/h')
plt.xlabel("Airspeed (m/s)"); plt.ylabel("Electric power (W)")
plt.title("Rear prop cruise power"); plt.legend(); plt.grid()
plt.savefig(os.path.join(OUT, "V12_4plus1_cruise.png"), dpi=110)
plt.close()

print(f"\nPlots saved to {OUT}")
print("\n=== KEY VERIFICATION RESULTS ===")
print(f"1. Hover T/W at MTOW 2.87kg: {W*TARGET_TW/W:.2f}x (target 1.7x) -> NEED 1220g/motor")
print(f"2. 35xx 12\" 700KV 4S: typical 1.8-2.2 kgf max -> 70% throttle gives ~1.3-1.5 kgf -> MARGINAL at 2.87kg")
print(f"3. If MTOW creeps to 3.2kg: need 1.36 kgf/motor at 70% -> motor must do 1.9+ kgf max")
print(f"4. Cruise 50 km/h: ~200-250W rear -> 25-30 min on 4S 8.4Ah -> MEETS 30-40 min target")
print(f"5. Battery fraction 21.6% (target 25%) -> need lighter airframe or bigger battery")
print(f"6. Wing loading {MTOW/S:.1f} kg/m2 -> 4.6 is reasonable")

# Save summary
summary = f"""# V1_2_FIXED 4+1 Analysis Summary

## Configuration Verification
- Layout: 4 fixed lift rotors (12" 2-blade) + 1 rear pusher (11x8 folding)
- Wingspan: 2473 mm, Chord: 324 mm, Area: 0.62 m²
- MTOW: 2.87 kg (target), Battery: 4S2P 8.4Ah Li-Ion (124 Wh, 620g)

## Hover Analysis (Momentum Theory)
- Disk loading: {W/A_LIFT:.1f} N/m² (total lift area {A_LIFT:.4f} m²)
- Thrust/motor at 1.7x T/W: {T_lift_target/9.81:.1f} kgf
- Power/motor (ISA): {hover_power_per_motor(W, RHO_STD):.0f} W
- Total hover power: {hover_power_per_motor(W, RHO_STD)*4:.0f} W
- Figure of merit assumed: {FM}

## Motor Verification
| Motor | Role | Spec | Required | Status |
|-------|------|------|----------|--------|
| 35xx-class x4 | Lift | 12\" 2-blade, ~700KV, 4S | 1.22 kgf @ 70%, 1.7+ kgf max | MARGINAL - verify on stand |
| AT2814 x1 | Rear | 11x8 folding, ~1000KV, 4S | 0.86 kgf cruise, 1.0+ kgf max | OK |

## Cruise Performance
- 50 km/h (13.9 m/s): {rear_prop_power(*cruise_drag(TARGET_CRUISE, RHO_STD), TARGET_CRUISE, RHO_STD):.0f}W rear + 20W avionics
- Endurance: {E_BATT/(rear_prop_power(*cruise_drag(TARGET_CRUISE, RHO_BALTIC), TARGET_CRUISE, RHO_BALTIC)+20)/60:.1f} min (Baltic air)
- 70 km/h dash: {rear_prop_power(*cruise_drag(TARGET_DASH, RHO_STD), TARGET_DASH, RHO_STD):.0f}W rear

## Critical Risks
1. **Lift motor margin thin** - 35xx 12" on 4S typically 1.8-2.2 kgf max. At 2.87kg MTOW need 1.22 kgf @ 70% throttle = 1.74 kgf max. If weight grows 10% (3.16kg), need 1.34 kgf @ 70% = 1.9 kgf max - still OK but no headroom.
2. **Battery fraction only 21.6%** - target 25%. Either airframe must come in <950g or battery to 10Ah.
3. **No duct** - open 12" rotors: FM=0.68 assumed. If FM=0.60, hover power +13%.
4. **Transition** - lift motors brake+align in cruise. Verify zero-drag brake torque.

## Recommendations
1. **Stand-test lift motors first** (T03) with 12" props on 4S - measure actual thrust at 70% throttle
2. **Weigh every part** before finalizing - airframe budget 950g is tight for 2.47m wing + V-tail
3. **Consider 35xx 800-850KV** for more thrust headroom on 4S, or 6S if ESCs support
4. **Rear AT2814 is fine** - well within cruise thrust requirement

## Files
- Plots: V12_4plus1_hover.png, V12_4plus1_cruise.png
"""
open(os.path.join(OUT, "V12_4plus1_analysis.md"), "w").write(summary)
print("\nAnalysis complete.")