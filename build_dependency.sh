#!/usr/bin/sh

# Build Dependency for ubuntu 20.04

## magic and netgen

  apt install -y git m4 tcsh csh libx11-dev tcl-dev tk-dev libcairo2-dev mesa-common-dev libglu1-mesa-dev libncurses-dev
  
## xschem  
  apt install -y git libx11-6 libx11-dev libxrender1 libxrender-dev libxcb1 libx11-xcb-dev libcairo2 libcairo2-dev tcl8.6 tcl8.6-dev tk8.6 tk8.6-dev flex bison libxpm4 libxpm-dev libjpeg-dev

## gaw3-xschem
  apt install -y git build-essential autoconf autopoint libgtk-3-dev libasound2-dev
  

## ngspice 
  apt install -y build-essential autoconf bison flex libtool libreadline-dev git adms libxaw7-dev

## klayout
  apt install -y git gcc g++ make qt5-default qttools5-dev libqt5xmlpatterns5-dev qtmultimedia5-dev libqt5multimediawidgets5 libqt5svg5-dev ruby ruby-dev python3 python3-dev python3-pip
  python3 -m pip install pandas

## openroad
  apt install -y tcl-tclreadline
  mkdir -p /tmp/build_foss
  cd /tmp/build_foss
  wget https://github.com/google/or-tools/releases/download/v9.5/or-tools_amd64_ubuntu-20.04_cpp_v9.5.2237.tar.gz
  mkdir -p /opt/or-tools
  tar --strip 1 --dir /opt/or-tools/ -xf or-tools_amd64_ubuntu-20.04_cpp_v9.5.2237.tar.gz
  rm -rf /tmp/build_foss

## yosys
  apt install -y git build-essential clang bison flex \
    libreadline-dev gawk tcl-dev libffi-dev git \
    graphviz xdot pkg-config python3 libboost-system-dev \
    libboost-python-dev libboost-filesystem-dev zlib1g-dev

## iverilog
  apt install -y git build-essential autoconf gperf bison flex libreadline-dev
  apt install -y gtkwave
