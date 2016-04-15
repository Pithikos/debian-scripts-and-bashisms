#!/bin/sh

# Version control
sudo apt-get update
sudo apt-get install git subversion git-svn -y

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


# Oh my git
cd /tmp
git clone http://github.com/gabrielelana/awesome-terminal-fonts
cd awesome-terminal-fonts
git checkout patching-strategy
mkdir -p ~/.fonts
cp patched/*.ttf ~/.fonts
sudo fc-cache -fv ~/.fonts
# MANUALSTEP: set terminal font to sourcecodepro+..
# MANUALSTEP: set the red color from the terminal pallete to orange..


# VirtualBox
#dist=`lsb_release -d | cut -f2`
#dist_codename=`lsb_release -c | cut -f2`
#html_line=`curl https://www.virtualbox.org/wiki/Linux_Downloads | grep "$dist" | grep -i "$dist_codename"`
#download_link=`echo $html_line | sed "s/.*i386.deb//" | sed s/.*href=// | sed s/\>.*//`
#download_link=`python -c "print(${download_link}.strip())"`

#wget "$download_link"
#sudo dpkg -i virtualbox*${dist_codename}*.deb
#sudo apt-get -f install -y
#sudo /sbin/rcvboxdrv setup
