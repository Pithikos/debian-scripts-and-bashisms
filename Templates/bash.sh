#!/bin/sh


# Looping through files
for file in "`ls | grep .xpi`"; do
	echo "$file"
done


# Check directory doesn't exists
if [ ! -d "$addon_id" ]; then
	echo "Directory doesn't exist"
fi


# Check file exists with a function
file_exists () {
	if [ -f "$1" ]; then
		echo "File exists"
	else
		echo "File doesn't exist"
	fi
}
