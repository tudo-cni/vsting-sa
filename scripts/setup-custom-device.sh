#!/bin/bash

ifaces=$@

echo $ifaces > .release-config.txt

# create vSTING network bridge
bash create-vsting-bridge.sh $ifaces

# configure vsting installation
echo "initiating release configuration with provided network interfaces: $ifaces"
python3 update_configs.py $ifaces
config_ok=$?
if [[ $config_ok != "0" ]]; then
    echo "relase configuration failed. will now exit!"
    exit 1
fi

# setup user home in systemd services
echo "configuring home path and username in systemd services ..."
vstingservices=( "api" "daemon" "ui" "logs" )
for service in "${vstingservices[@]}"
do
    (cd ~/vsting/systemd && sed -i "s/adrz/$USER/g" drz-vsting-${service}.service)
done
echo "systemd services configured."
