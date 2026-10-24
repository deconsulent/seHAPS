# V1_2_FIXED Baltic aero — low-order analysis
Method: lifting-line wing (AR=7.64) + parabolic drag + momentum-theory hover. NOT CFD.
Geometry: span=2.473m chord=0.324m S=0.8004m2 AR=7.64, 4xD=305mm.
Assumptions (need validation): CLmax=1.2, CD0=0.045, e=0.75, FM=0.65, eta_cruise=0.6.

## 1. Stall speed vs mass (ISA std)
- MTOW 4kg: Vs=8.2 m/s, 1.3Vs=10.6 m/s
- MTOW 5kg: Vs=9.1 m/s, 1.3Vs=11.9 m/s
- MTOW 6kg: Vs=10.0 m/s, 1.3Vs=13.0 m/s
- MTOW 7kg: Vs=10.8 m/s, 1.3Vs=14.0 m/s
- MTOW 8kg: Vs=11.5 m/s, 1.3Vs=15.0 m/s

## 2. Baltic density effect (6 kg)
- ISA std (+15C): rho=1.225, Vs=10.00 m/s, hover=822 W elec
- Riga annual mean (+7C): rho=1.260, Vs=9.86 m/s, hover=810 W elec
- Summer hot (+30C): rho=1.164, Vs=10.26 m/s, hover=843 W elec
- Winter cold (-10C): rho=1.341, Vs=9.56 m/s, hover=785 W elec

## 3. Cruise @18 m/s, ISA std
- 4kg: CL=0.247 CD=0.0484 D=7.7N Pelec=231W cruise_endurance(6S5000)=23min
- 5kg: CL=0.309 CD=0.0503 D=8.0N Pelec=240W cruise_endurance(6S5000)=22min
- 6kg: CL=0.371 CD=0.0526 D=8.4N Pelec=251W cruise_endurance(6S5000)=21min
- 7kg: CL=0.432 CD=0.0554 D=8.8N Pelec=264W cruise_endurance(6S5000)=20min
- 8kg: CL=0.494 CD=0.0586 D=9.3N Pelec=279W cruise_endurance(6S5000)=19min

## 4. Hover endurance (6S 5000mAh, 80% usable)
- 4kg: hover Pelec=447W -> 11.9 min
- 5kg: hover Pelec=625W -> 8.5 min
- 6kg: hover Pelec=822W -> 6.5 min
- 7kg: hover Pelec=1035W -> 5.1 min
- 8kg: hover Pelec=1265W -> 4.2 min

## 5. Baltic wind assessment (Riga: mean 3-6 m/s, winter gusts ~10 m/s)
- 6kg Vs=10.0 m/s std. Steady 6 m/s = 60% Vs: OK for cruise, marginal for hover position-hold (tilt authority needed).
- Gust 10 m/s ~= Vs: NO-GO for V1 transition tests. Limit T08/T09 to steady <6 m/s, gust spread <3 m/s.
- Winter -10C: +9.6% density helps lift/hover (-4.5% power) but LiPo capacity -20%: net endurance DOWN. Pre-warm battery.
- Rain/icing: no-fly (ducted props + film covering, pitot/IMU risk). August precip max.