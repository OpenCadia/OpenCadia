# ![PYOBD](/pyobd.gif) PYOBD 
## About the program<br>
**This is the remake of the free PC program for car diagnostics, aka. reading and displaying your cars OBD2 data(tests, sensors, DTC faults/reset, graphs of live sensor data). If your car supports obd2(which for the last 20 years most of the cars do), then you only need an elm327 adapter and a laptop with this program to diagnose your car. The program is free and open source and it is the only free program that exists for obd2, with this level of functionality, as far as I know. The program is the remake of the program PYOBD. It is much improved over the original pyobd, features live graphs, more displayable data and works on Python3 and all the new libraries. It was tested on Linux, Windows and MacOSX.**

**The program was made on top of the pyOBD program, which was made by Donour Sizemore. The original program has not been touched for 15 years, which came to my huge surprise, as to why noone worked on it. I decided then, that I will make it my personal project to first make it work on Python 3 and latest libraries, which I successfully did. After that I also expanded its functionality and made it use exclusively the rich Python OBD library, which was made by Brendan Whitfield. So now I have utilized two projects into one. The program is ofcourse still free and open source. So, special thanks goes to Donour Sizemore and Brendan Whitfield. And last, but not least, my name is Jure Poljsak, and this remake was made by me.**

## Downloads
<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for Windows 32-bit(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13windows-32-bit.exe)
<!-- END LATEST DOWNLOAD BUTTON -->

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for Windows 64-bit(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13windows-64-bit.exe)
<!-- END LATEST DOWNLOAD BUTTON -->

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for Linux 64-bit(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13linux)
<!-- END LATEST DOWNLOAD BUTTON -->

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for MacOSX 64-bit(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13macosx.app.zip)
<!-- END LATEST DOWNLOAD BUTTON -->

## Prerequisites:
You need an ELM327 adapter, a laptop and a car that supports OBD2 to use this program. All cars in Europe made since 2001 should support it. And in the USA all cars made since 1996.

**Which ELM327 device am I using and which will work?**<br/>
I am using this one(I bought it 10 years ago):<br/>
-OBDPro USB Scantool (http://www.obdpros.com/product_info.php?products_id=133)<br/>
Others that have been reported to work:<br/>
-OBDLink SX (https://www.obdlink.com/products/obdlink-sx/)<br/>
The Chinese clones may work but not fully and the ones that work (at least mostly) properly are $10 or more. There are multiple reasons why a good adapter is not the cheapest. OBDLink makes good adapters and also VGate - their adapters also receive firmware updates so while they are already very good, they keep improving. I recommend USB adapters for stable and fast connection. Bluetooth is slower and less reliable and wireless has been reported as the worst. If you really want to go buy a Chinese clone, I recommend that it has PIC18F25K80 chip and FTDI chip(for USB) - but even then, the firmware is also a factor - 1.5 should be best(for a Chinese clone), but who knows what you will get. If you want a trusted good adapter, then I think currently for USB vLinker FS USB is the best and with a good price. And if you want to go with a good bluetooth adapter, then I recommend Vgate iCAR Pro, which is also priced good. If you want an ok affordable Chinese elm327, that is branded, then go with KONNWEI KW903. It's about $15 with postage included. But iCar pro is better. This is what I found out by googling and reading about it for 3 days.<br/>

# Installation

## Windows
Download the standalone executable and install the driver for your ELM327 device. Drivers can be found here:
http://www.totalcardiagnostics.com/support/Knowledgebase/Article/View/1/0/how-to-install-elm327-usb-cable-on-windows-and-obd2-software <br/>

## Linux
Download the standalone executable and add your user account the privileges of accesing USB and serial ports:
> sudo usermod -a -G dialout $USER
> sudo usermod -a -G tty $USER
After you run these two commands you have to log out and log back in for it to take effect(or restart).

On some distributions you also have to install the libnsl library.

## MacOS
Download the executable and you should be ready for use.

## Usage
The ignition must be on, to connect to the car and display data(key turned one level before engine start). Although most of the sensors display data only when the engine is running. If you connected and then turn the engine on, you have to wait a bit so that the program reconnects.

To connect, go to Configure, select the right port and the right baudrate and click connect. You can leave it at AUTO and connect, but it will take longer to connect and in some cases it will not connect. Manual is safest and fastest, but AUTO works in most cases too.

### Video presentation on YouTube(click on it):
[![PYOBD Youtube video 2021](https://img.youtube.com/vi/u3oWU_zEY5E/0.jpg)](https://www.youtube.com/watch?v=u3oWU_zEY5E)

# Running the script
On Debian 10 and 11 and on Ubuntu, type these commands to install the requirements(on Ubuntu replace libgstreamer-plugins-base1.0 with libgstreamer-plugins-base1.0-0): 
> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev
> pip3 install -r requirements.txt
> sudo usermod -a -G dialout $USER
> sudo usermod -a -G tty $USER
After you run these two commands you have to log out and log back in for it to take effect(or restart).
In some cases you also have to install the libnsl library.
The script is executed by running:
> python3 pyobd.py

# Creating the executable
## Linux
On Debian 10 and 11 and on Ubuntu, type these commands to install the requirements(on Ubuntu replace libgstreamer-plugins-base1.0 with libgstreamer-plugins-base1.0-0): 
> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev
In some cases you also have to install the libnsl library.
> pip3 install -r requirements.txt
> pip3 install pyinstaller
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico:." pyobd.py
## Windows
Install Python3. Then run these commands:
> pip3 install -r requirements.txt
> pip3 install pyinstaller
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico;." pyobd.py
## MacOS
Make sure that you have Python 3 installed. Then run these commands:
> pip3 install -r requirements.txt
> pip3 install pyinstaller
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico:." pyobd.py

# Troubleshooting:
If you encounter any bugs and problems you can e-mail me at:
![email](/email.png)
and I will try to fix the bug/problem as soon as possible.

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/jpoljsak/)

### TO DO LIST:<br />
-add sensor data exporting and replay.

![ELM327](/elm327.jpg)
