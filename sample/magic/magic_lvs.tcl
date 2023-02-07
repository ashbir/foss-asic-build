#    batch script for running Magic LVS
crashbackups stop
snap internal
gds flatglob *__example_*
gds flatten true
gds read ../klayout/inv.gds
load inv
select top cell
expand
extract all
ext2spice lvs 
ext2spice subcircuit off
ext2spice -f ngspice -o inv_lvs_extracted.spice
quit
