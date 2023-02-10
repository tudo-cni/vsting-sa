#!/bin/bash

sudo iptables -D FORWARD -i vsting-br -o vsting-br -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables/rules.v4"
sudo nmcli con down bridge-vsting
sudo nmcli con del vsting-br-robot
sudo nmcli con del vsting-br-operator
sudo nmcli con del bridge-vsting
