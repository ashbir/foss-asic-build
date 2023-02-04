#!/usr/bin/sh

# Build Dependency for ubuntu 20.04

## magic and netgen

  apt install -y git m4 tcsh csh libx11-dev tcl-dev tk-dev libcairo2-dev mesa-common-dev libglu1-mesa-dev libncurses-dev
  
## xschem  
  apt install -y git libx11-6 libx11-dev libxrender1 libxrender-dev libxcb1 libx11-xcb-dev libcairo2 libcairo2-dev tcl8.6 tcl8.6-dev tk8.6 tk8.6-dev flex bison libxpm4 libxpm-dev libjpeg-dev

## ngspice 
  apt install -y build-essential autoconf bison flex libtool libreadline-dev git adms

## klayout
  apt install -y git gcc g++ make qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3 python3-dev python3-pip
  python3 -m pip install pandas
