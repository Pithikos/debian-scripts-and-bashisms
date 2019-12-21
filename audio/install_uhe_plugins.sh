#! /bin/bash
# source: https://www.kvraudio.com/forum/viewtopic.php?f=31&t=424953&hilit=diva+linux+bazille
# serial number: 
function install_uhe()
(
  product="$1"
  rev="$2"
  cd /tmp &&
  wget http://uhedownloads.heckmannaudiogmb.netdna-cdn.com/penguin/release/$rev/$product-$rev.tar.gz -O $product-$rev.tar.gz &&
  tar xf $product-$rev.tar.gz &&
  cd $product-$rev &&
  ./install.sh --quiet &&
  cd /tmp &&
  rm -rf $product-$rev $product-$rev.tar.gz
)

for product in ACE Bazille Diva Filterscape Hive MFM2 Podolski Presswerk Protoverb "Repro 4365" Satin TrippleCheese Uhbik "Zebra2 4458"
do
  install_uhe $product 4408
done
