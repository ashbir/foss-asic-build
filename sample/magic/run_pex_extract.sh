#!/bin/bash


magic -dnull -noconsole -rcfile $PDK_ROOT/$PDK/libs.tech/magic/$PDK.magicrc ./magic_pex.tcl; cat inv_pex_extracted.spice
