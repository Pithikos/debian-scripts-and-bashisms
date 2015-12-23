#!/bin/sh

# System tools
sudo apt-get insatll htop -y
sudo apt-get install gparted -y

# Wireshark
sudo apt-get install wireshark -y
sudo dpkg-reconfigure wireshark-common 
sudo usermod -a -G wireshark $USER
