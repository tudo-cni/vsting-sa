#!/bin/bash
ifaces=$(head -n 1 .release-config.txt)
ifaces_l=($ifaces)
iface_robot=${ifaces_l[0]}
iface_operator=${ifaces_l[1]}
sudo nmcli con add type bridge ifname vsting-br connection.id bridge-vsting bridge.stp no
nmcli connection modify bridge-vsting ipv4.dhcp-timeout infinity
sudo nmcli con add type bridge-slave ifname $iface_robot master vsting-br connection.id vsting-br-robot
sudo nmcli con add type bridge-slave ifname $iface_operator master vsting-br connection.id vsting-br-operator
sudo iptables -A FORWARD -i vsting-br -o vsting-br -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables/rules.v4"
