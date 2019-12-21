Install JACK
------------

Install packages

		sudo apt-get install qjackctl pulseaudio-module-jack

Add to Ubuntu "startup applications" the below

		sh -c '/home/manos/workspace/ubuntu-fresh-install/audio/start-jack.sh &> /tmp/jackstart.log'
