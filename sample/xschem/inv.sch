v {xschem version=3.1.0 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1070 -2180 1070 -2120 {
lab=out}
N 1070 -2260 1070 -2240 {
lab=vdd}
N 1070 -2090 1090 -2090 {
lab=vss}
N 1090 -2090 1090 -2060 {
lab=vss}
N 1070 -2050 1090 -2050 {
lab=vss}
N 1070 -2060 1070 -2040 {
lab=vss}
N 1070 -2150 1120 -2150 {
lab=out}
N 1010 -2210 1030 -2210 {
lab=in}
N 1010 -2210 1010 -2090 {
lab=in}
N 1010 -2090 1030 -2090 {
lab=in}
N 960 -2150 1010 -2150 {
lab=in}
N 1090 -2060 1090 -2050 {
lab=vss}
N 1070 -2280 1070 -2260 {
lab=vdd}
N 1100 -2260 1100 -2210 {
lab=vdd}
N 1070 -2260 1100 -2260 {
lab=vdd}
N 1060 -2210 1100 -2210 {
lab=vdd}
C {sky130_fd_pr/nfet_01v8.sym} 1050 -2090 0 0 {name=M1
L=0.15
W=0.65
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {devices/iopin.sym} 1070 -2280 0 0 {name=p1 lab=vdd}
C {devices/ipin.sym} 960 -2150 0 0 {name=p2 lab=in}
C {devices/opin.sym} 1120 -2150 0 0 {name=p3 lab=out}
C {devices/iopin.sym} 1070 -2040 0 0 {name=p4 lab=vss}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 1050 -2210 0 0 {name=M8
L=0.15
W=1
nf=1 mult=1
model=pfet_01v8_hvt
spiceprefix=X
}
