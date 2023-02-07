v {xschem version=3.1.0 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 370 -280 370 -250 {
lab=VDD}
N 370 -190 370 -160 {
lab=VSS}
N 340 -220 370 -220 {
lab=in}
N 470 -220 510 -220 {
lab=out}
N 510 -220 510 -200 {
lab=out}
N 510 -140 510 -120 {
lab=VSS}
N 70 -160 70 -130 {
lab=VDD}
N 160 -150 160 -130 { lab=VSS}
N 160 -70 160 -50 {
lab=GND}
N 240 -160 240 -130 {
lab=in}
N 70 -70 70 -50 {
lab=GND}
N 240 -70 240 -50 {
lab=GND}
C {inv.sym} 390 -220 0 0 {}
C {devices/capa.sym} 510 -170 0 0 {name=C1
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 370 -270 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 370 -180 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 510 -220 2 0 {name=p3 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 350 -220 0 0 {name=p4 sig_type=std_logic lab=in}
C {devices/vsource.sym} 70 -100 0 0 {name=V1 value=1.8}
C {devices/vsource.sym} 160 -100 0 0 {name=V3 value=0}
C {devices/lab_pin.sym} 160 -150 0 1 {name=l3 sig_type=std_logic lab=VSS}
C {devices/gnd.sym} 160 -50 0 0 {name=l1 lab=GND}
C {devices/lab_pin.sym} 70 -150 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 510 -130 0 1 {name=l5 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 240 -100 0 0 {name=V2 value="PULSE(0 1.8 0.1e-9 0.1e-9 0.1e-9 0.4e-9 1e-9)"}
C {devices/lab_pin.sym} 240 -150 0 1 {name=l7 sig_type=std_logic lab=in}
C {devices/simulator_commands_shown.sym} 240 -470 0 0 {name=COMMANDS2
simulator=ngspice
only_toplevel=false 
value="
**** interactive sim
.control
save all
tran 1p 5n
write test_inv_ngspice.raw
.endc
"}
C {sky130_fd_pr/corner.sym} 30 -470 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/gnd.sym} 70 -50 0 0 {name=l2 lab=GND}
C {devices/gnd.sym} 240 -50 0 0 {name=l6 lab=GND}
