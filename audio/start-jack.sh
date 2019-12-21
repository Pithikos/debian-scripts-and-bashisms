# /bin/bash/

# Partially inspired from; https://gist.github.com/gatlin/436fe265ce05574c84a9e3f0d2158650

# Suspend pulseaudio
pulseaudio --start
pacmd suspend true

# Start JACK in the background
killall jackd -q
/usr/bin/jackd -dalsa -dhw:0 -r44100 -p1024 -n2 &>/tmp/jackd.out &
sleep 1

# Run pulse audio and connect to JACK
pacmd suspend false
pacmd load-module module-jack-sink
pacmd load-module module-jack-source
pacmd set-default-sink jack_out
