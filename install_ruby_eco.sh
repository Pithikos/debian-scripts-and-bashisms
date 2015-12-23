#!/bin/sh

# Install RVM (Ruby Version Manager) on Ubuntu
sudo mkdir -p /etc/pki/tls/certs/
sudo cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt
curl -sSL https://rvm.io/mpapis.asc | gpg --import -
\curl -L https://get.rvm.io | bash -s stable --ruby

# Let RVM install Ruby
source /home/manos/.rvm/scripts/rvm
rvm get stable --autolibs=enable
rvm install ruby
rvm --default use ruby

# Install Rails
gem install rails

# Install Bundler
gem install bundler

# Install Heroku client
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku login
