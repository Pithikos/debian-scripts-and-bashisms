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
git config --global user.email manossef@gmail.com
git config --global user.name 'Pithikos'


## PACKAGES

# Multimedia
sudo add-apt-repository ppa:videolan/stable-daily -y
sudo apt-get update
sudo apt-get install vlc -y

# Programming
sudo add-apt-repository ppa:webupd8team/atom -y
sudo apt-get update
sudo apt-get install atom -y

sudo apt-get install vim -y

sudo apt-get install geany -y
cd /tmp
git clone https://github.com/codebrainz/geany-themes.git
mkdir -p ~/.config/geany/colorschemes/
cp geany-themes/colorschemes/* ~/.config/geany/colorschemes/
cd $OLD

# Graphics
sudo apt-get install gimp inkscape -y

# VirtualBox


# Networking
sudo apt-get install nmap -y
sudo apt-get install wireshark -y
sudo apt-get install curl -y

# Chrome
sudo apt-get install chromium-browser -y

# Firefox extensions
mkdir -p ~/.mozilla/extensions/
cd ~/.mozilla/extensions/

# email notifier
wget https://addons.mozilla.org/firefox/downloads/latest/4490/addon-4490-latest.xpi
# toggle proxy
wget https://addons.mozilla.org/firefox/downloads/latest/51740/platform:2/addon-51740-latest.xpi
# adblock
wget https://addons.mozilla.org/firefox/downloads/latest/1865/addon-1865-latest.xpi

mkdir tmp
for file in `ls | grep .xpi`; do
  cd tmp 
  unzip ../$file
  cd ..
  rm $file
  addon_id=`egrep {.*} tmp/install.rdf -m 1 | sed "s/.*\({.*}\).*/\1/"`
  if [ ! -d "$addon_id" ]; then
    mkdir $addon_id
    cp -R tmp/* $addon_id
  fi
  rm -fr tmp/*
done
rmdir tmp


# Torrent
sudo apt-get install deluge -y

# Docker
sudo apt-get install docker -y

# Skype

# System tools
sudo apt-get install gparted -y
