#!/bin/sh

mkdir -p ~/.mozilla/extensions/
cd ~/.mozilla/extensions/

# urls
base_url='https://addons.mozilla.org/firefox/downloads/latest/'
addon_email_notifier='4490/addon-4490-latest.xpi'
addon_toggle_proxy='51740/platform:2/addon-51740-latest.xpi'
addon_adblock_plus='1865/addon-1865-latest.xpi'

# Get addons
wget "${base_url}${addon_email_notifier}"
wget "${base_url}${addon_toggle_proxy}"
wget "${base_url}${addon_adblock_plus}"


# Install addons
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
