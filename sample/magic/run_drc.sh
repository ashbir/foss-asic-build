#!/bin/bash

magic -dnull -noconsole -rcfile $PDK_ROOT/$PDK/libs.tech/magic/$PDK.magicrc ./magic_drc.tcl; cat sky130_magic_drc.txt

