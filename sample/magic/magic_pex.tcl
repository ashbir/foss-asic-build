#    batch script for running Magic PEX
crashbackups stop
snap internal
gds flatglob *__example_*
gds flatten true
gds read ../klayout/inv.gds
load inv
select top cell
expand
extract all
ext2sim labels on
ext2sim
extresist tolerance 10
extresist
ext2spice lvs
ext2spice cthresh 0.01
ext2spice extresist on
ext2spice -f ngspice -o inv_pex_extracted.spice
quit
