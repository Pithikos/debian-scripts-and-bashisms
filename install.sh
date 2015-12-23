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


# VirtualBox


# Web & net
sudo apt-get install wireshark -y
sudo apt-get install chromium-browser -y
sudo apt-get install deluge -y


# Dev
sudo apt-get install docker.io -y

sudo add-apt-repository ppa:webupd8team/atom -y
sudo apt-get update
sudo apt-get install atom -y

sudo apt-get install geany -y
cd /tmp
git clone https://github.com/codebrainz/geany-themes.git
mkdir -p ~/.config/geany/colorschemes/
cp geany-themes/colorschemes/* ~/.config/geany/colorschemes/
cd $OLD


# Firefox extensions
./install_firefox_addons.sh
./install_unix_basic.sh


# System tools
sudo apt-get install gparted -y
