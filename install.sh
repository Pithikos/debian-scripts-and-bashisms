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

# Other
sudo apt-get install chromium-browser -y
sudo apt-get install deluge -y

# Installation
./install_unix_basic.sh
./install_unix_extra.sh
./install_social.sh
./install_firefox_addons.sh
./install_dev_eco.sh
./install_ruby_eco.sh
./install_python_eco.sh
./install_artsy_eco.sh
