#!/bin/bash

#clone and download tools
curr_dir = $(pwd)
sudo apt -y update && sudo apt -y upgrade
mkdir FOSS
cd FOSS
git clone https://github.com/ashbir/foss-asic-build.git foss-build
mkdir cadtar
cd cadtar
wget -O gaw.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/gaw3-xschem-a4bb956.tar.gz"
wget -O iverilog.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/iverilog-4643f57ed.tar.gz"
wget -O klayout.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/klayout-e59484281.tar.gz"
wget -O magic.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/magic-adda409.tar.gz"
wget -O netgen.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/netgen-28a2950.tar.gz"
wget -O ngspice.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/ngspice-f9ed3fd08.tar.gz"
wget -O openroad.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/openroad-c7bfcda0d.tar.gz"
wget -O xschem.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/xschem-cac1caa7.tar.gz"
wget -O yosys.tar "https://github.com/ashbir/foss-asic-build/releases/download/v0.0.2/yosys-417fadbef.tar.gz"

#build dependency
cd curr_dir
cd ./foss-build
chmod +x build_dependency.sh
sudo ./build_dependency.sh

#install volare
cd curr_dir
sudo apt-get -y install python3 python3-pip xz-utils
python3 -m pip install --upgrade --no-cache-dir volare
## as per python 3.6, cited from https://pypi.org/project/volare/, one needs to add on .profile:
### export PATH="/home/test/.local/bin:$PATH" ###

#use volare to download and enable skywater130 PDK (MAKE SURE that you have already defined $PDK and $PDK_ROOT inside ~/.bashrc)
cd curr_dir
mkdir PDK
cd PDK
volare ls-remote --pdk sky130 #to list all available pre-built PDKs hosted
## Please copy the latest package commit hash (ex: 4cfc6af9ceba75a2f35c76f89ece76aa539f9a8d)
volare enable --pdk sky130 4cfc6af9ceba75a2f35c76f89ece76aa539f9a8d #change accordingly

#create folders to store tools and extract them
cd /
sudo rm -rf cad/
sudo mkdir cad
cd cad
sudo mkdir foss
cd foss
sudo mkdir tools
cd curr_dir
sudo tar -xf ~/cadtar/gaw.tar -C /cad/foss/tools/
sudo tar -xf ~/cadtar/iverilog.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/klayout.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/magic.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/netgen.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/ngspice.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/openroad.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/xschem.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/yosys.tar -C /cad/foss/tools
