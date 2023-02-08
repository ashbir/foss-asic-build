#clone and download tools
sudo apt update && sudo apt upgrade
cd ~
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
cd ~
cd ./foss-build
chmod +x build_dependency.sh
sudo ./build_dependency.sh

#create folders to store tools and extract them
cd /
sudo rm -rf cad/
sudo mkdir cad
cd cad
sudo mkdir foss
cd foss
sudo mkdir tools
cd ~
sudo tar -xf ~/cadtar/gaw.tar -C /cad/foss/tools/
sudo tar -xf ~/cadtar/iverilog.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/klayout.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/magic.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/netgen.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/ngspice.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/openroad.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/xschem.tar -C /cad/foss/tools
sudo tar -xf ~/cadtar/yosys.tar -C /cad/foss/tools
