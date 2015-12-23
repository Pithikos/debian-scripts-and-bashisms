#!/bin/sh


## UPGRADE
sudo apt-get update && sudo apt-get upgrade -y

## PREREQUISITES
cd /tmp
sudo apt-get install git -y


## DESKTOP CUSTOMIZATION

# Icons
sudo add-apt-repository ppa:tiheum/equinox -y
sudo apt-get update
sudo apt-get install faenza-icon-theme

# Tweak Tool
# need to open manually atm

# Templates
git clone https://github.com/Pithikos/ubuntu-fresh-install.git
cp ubuntu-fresh-install/Templates/* ~/Templates/


## CONFIGURATION
git config --global user.email 'manossef@gmail.com'
git config --global user.name 'Johan Hanssen Seferidis'


## PACKAGES

# Multimedia
sudo add-apt-repository ppa:videolan/stable-daily -y
sudo apt-get update
sudo apt-get install vlc -y

# Graphics
sudo apt-get install gimp inkscape -y

# Web & net
sudo apt-get install wireshark -y
sudo apt-get install chromium-browser -y
sudo apt-get install deluge -y

# System tools
sudo apt-get install gparted -y

# Installation
./install_unix_basic.sh
./install_social.sh
./install_firefox_addons.sh
