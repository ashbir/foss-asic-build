#!/bin/bash

#clone and download tools 
CURR_DIR=$(pwd)
sudo apt -y update && sudo apt -y upgrade
mkdir FOSS
cd FOSS
git clone https://github.com/ashbir/foss-asic-build.git foss-build
mkdir cadtar
cd cadtar
wget -O gaw.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/gaw3-xschem-a4bb956.tar.gz"
wget -O iverilog.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/iverilog-4643f57ed.tar.gz"
wget -O klayout.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/klayout-e59484281.tar.gz"
wget -O magic.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/magic-adda409.tar.gz"
wget -O netgen.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/netgen-28a2950.tar.gz"
wget -O ngspice.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/ngspice-f9ed3fd08.tar.gz"
wget -O openroad.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/openroad-c7bfcda0d.tar.gz"
wget -O xschem.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/xschem-cac1caa7.tar.gz"
wget -O yosys.tar.gz "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/yosys-417fadbef.tar.gz"

#build dependency
cd $CURR_DIR/FOSS/foss-build
chmod +x build_dependency.sh
sudo ./build_dependency.sh


source ${CURR_DIR}/FOSS/dotfiles/bashrc
cat ${CURR_DIR}/FOSS/dotfiles/bashrc >> ${HOME}/.bashrc
mkdir -p $PDK_ROOT

#install volare
sudo apt-get -y install python3 python3-pip xz-utils
python3 -m pip install --upgrade --no-cache-dir volare
volare --version #check if volare has been installed correctly
## as per python 3.6, cited from https://pypi.org/project/volare/, one needs to add on .profile:
### export PATH="/home/test/.local/bin:$PATH" ###

#use volare to download and enable skywater130 PDK (MAKE SURE that you have already defined $PDK and $PDK_ROOT inside ~/.bashrc)
volare ls-remote --pdk sky130 #to list all available pre-built PDKs hosted
## Please copy the latest package commit hash (ex: 4cfc6af9ceba75a2f35c76f89ece76aa539f9a8d)
volare enable --pdk sky130 4cfc6af9ceba75a2f35c76f89ece76aa539f9a8d #change accordingly

#create folders to store tools and extract them
sudo mkdir -p /cad/foss/tools/gaw
sudo mkdir -p /cad/foss/tools/iverilog
sudo mkdir -p /cad/foss/tools/klayout
sudo mkdir -p /cad/foss/tools/magic
sudo mkdir -p /cad/foss/tools/netgen
sudo mkdir -p /cad/foss/tools/ngspice
sudo mkdir -p /cad/foss/tools/openroad
sudo mkdir -p /cad/foss/tools/xschem
sudo mkdir -p /cad/foss/tools/yosys

sudo tar -xf ${CURR_DIR}/FOSS/cadtar/gaw.tar.gz -C /cad/foss/tools/gaw --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/iverilog.tar.gz -C /cad/foss/tools/iverilog --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/klayout.tar.gz -C /cad/foss/tools/klayout --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/magic.tar.gz -C /cad/foss/tools/magic --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/netgen.tar.gz -C /cad/foss/tools/netgen --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/ngspice.tar.gz -C /cad/foss/tools/ngspice --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/openroad.tar.gz -C /cad/foss/tools/openroad --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/xschem.tar.gz -C /cad/foss/tools/xschem --strip 1
sudo tar -xf ${CURR_DIR}/FOSS/cadtar/yosys.tar.gz -C /cad/foss/tools/yosys --strip 1
