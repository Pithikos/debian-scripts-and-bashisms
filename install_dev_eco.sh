#!/bin/sh

# Install Docker
sudo apt-get install docker.io -y
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart

# IDEs
sudo add-apt-repository ppa:webupd8team/atom -y
sudo apt-get update
sudo apt-get install atom -y

sudo apt-get install geany -y
cd /tmp
git clone https://github.com/codebrainz/geany-themes.git
mkdir -p ~/.config/geany/colorschemes/
cp geany-themes/colorschemes/* ~/.config/geany/colorschemes/
cd $OLD

# VirtualBox
