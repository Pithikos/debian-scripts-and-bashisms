#!/bin/sh

#
# Installation of addon can be for a user or the whole system. After testing
# around both ways are a bit different.
#
# Direct installation (doesn't work for system install):
# extensions/<addon id>/<unzipped .xpi>
#
# Unzipped installation:
# extensions/<addon id>.xpi
#

EXTENSIONS_SYSTEM='/usr/share/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/'
EXTENSIONS_USER=`echo ~/.mozilla/firefox/*.default/extensions/`


# -------------------------- xpi tools ---------------------------------

get_addon_id_from_xpi () { #path to .xpi file
	addon_id_line=`unzip -p $1 install.rdf | egrep '<em:id>' -m 1`
	addon_id=`echo $addon_id_line | sed "s/.*>\(.*\)<.*/\1/"`
	echo "$addon_id"
}

get_addon_name_from_xpi () { #path to .xpi file
	addon_name_line=`unzip -p $1 install.rdf | egrep '<em:name>' -m 1`
	addon_name=`echo $addon_name_line | sed "s/.*>\(.*\)<.*/\1/"`
	echo "$addon_name"
}


# -------------------------- installations -----------------------------

# Installs .xpi given by relative path
# to the extensions path given
#
# extensions/<addon id>.xpi
install_zipped () {
	xpi="${PWD}/${1}"
	extensions_path=$2
	new_filename=`get_addon_id_from_xpi $xpi`.xpi
	new_filepath="${extensions_path}${new_filename}"
	addon_name=`get_addon_name_from_xpi $xpi`
	if [ -f "$new_filepath" ]; then
		echo "File already exists: $new_filepath"
		echo "Skipping installation for addon $addon_name."
	else
		cp "$xpi" "$new_filepath"
	fi
}

# Installs .xpi given by relative path
# to the extensions path given
#
# extensions/<addon id>/<unzipped .xpi>
install_unzipped () {
	xpi="${PWD}/${1}"
	extensions_path=$2
	new_foldername=`get_addon_id_from_xpi $xpi`
	mkdir -p "${extensions_path}${new_foldername}"
	cd "${extensions_path}${new_foldername}"
	unzip "$xpi"
	cd $OLDPWD
}


# -------------------------------------------------------------------

# Addons urls
base_url='https://addons.mozilla.org/firefox/downloads/latest/'
addon_email_notifier='4490/addon-4490-latest.xpi'
addon_toggle_proxy='51740/platform:2/addon-51740-latest.xpi'
addon_adblock_plus='1865/addon-1865-latest.xpi'

# Install addons
mkdir -p /tmp/firefox_extensions
cd /tmp/firefox_extensions

wget "${base_url}${addon_email_notifier}"
wget "${base_url}${addon_toggle_proxy}"
wget "${base_url}${addon_adblock_plus}"

for file in `ls | grep .xpi`; do
  install_zipped "$file" "$EXTENSIONS_USER"
done
