#!/bin/bash

# download next version
echo "downloading vsting release in your home folder..."
mkdir download
wget https://tu-dortmund.sciebo.de/s/UL0g6TDB7qJQqLx/download -O download/vsting.zip
unzip download/vsting.zip -d download
mv download/vsting-sa ~/vsting
chmod +x ~/vsting/*.sh
chmod +x ~/vsting/api/dist/run/run
chmod +x ~/vsting/combox_monitor/dist/cli/cli
chmod +x ~/vsting/combox_monitor/dist/daemon/daemon
echo "next vsting release downloaded."

