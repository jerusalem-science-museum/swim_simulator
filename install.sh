#! /usr/bin/bash

#install all the packages

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y git git-lfs python-usb python3-usb ffmpeg python3-pip apache2 

pip3 install --upgrade pip 
sudo pip3 install --upgrade libusb pyusb requests pyyaml

# clone the project
cd ~/Desktop
git clone https://github.com/jerusalem-science-museum/swim_simulator
cd swim_simulator
git lfs install
git lfs pull
# setup the apache2 configuration

sudo cp /src/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf 

sudo a2ensite 000-default.conf

service apache2 reload

# change ownership 
sudo chown www-data:mada src/www/video.mp4

mkdir src/logs

