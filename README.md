# Rowing-Simulator-Bloomfiled-Science-Museum

### Setup 

To install the app correctly please follow these steps:

#### Install all of the required packages

pip3 - `sudo apt-get install python3-pip`

libusb - `pip install libusb`

ubs packages - `sudo apt-get install python-usb python3-usb`

pyusb - `pip install pyusb`

ffmpeg - `sudo apt-get install ffmpeg`

requests - `pip install requests`

apache2 - `sudo apt-get install apache2`

#### Clone the project 

cd to the desktop:

`cd ~/Desktop`

make a directory for the git clone

`mkdir git`

cd into git

`cd git`

clone the project

`git clone https://github.com/jerusalem-science-museum/swim_simulator`

#### Configure the Apache2 server 
The app requires an apache server in order to run.
After you installed apache2 on the machine you have to edit the configuration. 
run:

`sudo nano /etc/apache2/sites-enabled/000-default.conf`

add the following lines to the configuration:
```
		DocumentRoot /home/mada/git/swin_simulator/src/www/
		<Directory /home/mada/git/>swin_simulator/src/www/>
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

`sudo chown www-data:mada video.mp4`

navigate to `http://127.0.0.1` to make sure the installation was successful. 

