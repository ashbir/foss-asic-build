#!/bin/bash

netgen -batch lvs "../xschem/simulations/inv.spice inv" "../magic/inv_lvs_extracted.spice inv" $PDK_ROOT/$PDK/libs.tech/netgen/$PDK_setup.tcl inv_netgen.log; cat inv_netgen.log
