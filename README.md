# Rowing-Simulator-Bloomfiled-Science-Museum

### Setup 

To install the app correctly please follow these steps: 
or run the setup script. 

```
./install.sh
```

#### Install all of the required packages

pip3 - `sudo apt-get install python3-pip`

libusb - `pip install libusb`

ubs packages - `sudo apt-get install python-usb python3-usb`

pyyaml - `pip install pyyaml`

pyusb - `pip install pyusb`

ffmpeg - `sudo apt-get install ffmpeg`

requests - `pip install requests`

apache2 - `sudo apt-get install apache2`

#### Clone the project 

cd to the desktop:

`cd ~/Desktop`

clone the project

`git clone https://github.com/jerusalem-science-museum/swim_simulator`

#### Configure the Apache2 server 
The app requires an apache server in order to run.
After you installed apache2 on the machine you have to edit the configuration. 
run:

`sudo nano /etc/apache2/sites-enabled/000-default.conf`

add the following lines to the configuration:
```
ServerAdmin webmaster@localhost
        DocumentRoot /home/mada/Desktop/swim_simulator/src/www/
		<Directory /home/mada/Desktop/swim_simulator/src/www/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Require all granted
        </Directory>
```
After that run:

`sudo a2ensite 000-default.conf`

than reload apache for the changes to take effect

`service apache2 reload`

change the user ownership on the video file 

`sudo chown www-data:mada src/www/video.mp4`

navigate to `http://127.0.0.1` to make sure the installation was successful. 


### Running the app 

The app requires root permissions in order to run correctly.

run:

`./run.sh`

If you want to close the app run:

`pkill python 'or run' ./stop.sh`


### Video Format 

due to a bug in firefox some specific encoding of MP4 files dont load correctly. 
there for the video that is being used should be encoded to WEBM format. 