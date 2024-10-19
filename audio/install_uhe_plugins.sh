#! /bin/bash
function list_linux_packages()
{
  curl https://u-he.com/downloads/releases/ | grep 'Linux.tar.xz' | cut -d '<' -f 3 | cut -d '>' -f 2
}

# Download all u-he plugins
dir=$(mktemp -d)
cd $dir
for package in $(list_linux_packages); do
  echo "Downloading $package to $dir"
  wget https://u-he.com/downloads/releases/$package
done

# Install all u-he plugins
for package in $(ls); do
  echo "Installing $package"
  install_dirname=$(echo $package | cut -d '.' -f 1)
  mkdir $install_dirname
  tar -xvf $package -C $install_dirname

  cd $install_dirname/*
  ./install.sh --quiet
  cd ../..
done