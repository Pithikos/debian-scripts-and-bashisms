#!/bin/sh

# Anaconda
anaconda2='https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda3-2.4.1-Linux-x86_64.sh'
anaconda3='https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh'
wget "$anaconda2"
wget "$anaconda3"
bash Anaconda2-2.4.1-Linux-x86_64.sh
bash Anaconda3-2.4.1-Linux-x86_64.sh

# Pip
sudo apt-get install python3-pip -y
sudo apt-get install python-pip -y
