# ![PYOBD](/pyobd.gif) PYOBD 
## About the program<br>
**This is the remake of the free and open source PC program called pyOBD. It is used for car diagnostics, aka. reading and displaying your cars OBD2 data(tests, sensors, DTC faults/reset, graphs of live sensor data). Most if not all cars in Europe and USA support the OBD2 if they have been made in the last 20+ years. You will need an adapter called ELM327 to use it, and a laptop. The original program was made by Donour Sizemore. It was made in the Python programming language, hence the name pyOBD. The original program has not been touched for 15 years, so I decided then, that I will make it my personal project to first make it work on Python 3 (originally it was made in Python 2) and latest libraries, which I successfully did. After that I also expanded its functionality and made it use exclusively the rich Python OBD library, which was made by Brendan Whitfield. So now I have utilized two projects into one. I also added live graphs and many other improvements and made it more "bulletproof". The program is still free and open source. It works on Windows, Linux and MacOS. My name is Jure Poljsak, and this remake was made by me.**

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

**Which ELM327 adapters have been reported to work?**<br/>
-OBDPro USB Scantool (http://www.obdpros.com/product_info.php?products_id=133)<br/>
-OBDLink SX USB (https://www.obdlink.com/products/obdlink-sx/)<br/>
-Chinese OBD2 1.5 USB<br/>
-VGate iCar Pro BLE (Bluetooth 4.0).

**Please write to me which adapters you have tested working with the app, so I can include it in the list. My e-mail is at the bottom of this readme.**

**NOTE: Both USB and bluetooth adapters work with this app, but under Linux I had to pair the bluetooth adapter manually via command line and then manually connect to it. It's probably because bluetooth GUI managers under Linux are buggy.**

**Which adapters are good?**</br>
The Chinese clones may work but not fully and the ones that work (at least mostly) properly are $10 or more. There are multiple reasons why a good adapter is not the cheapest. OBDLink makes good adapters and also VGate - their adapters also receive firmware updates so while they are already very good, they keep improving. I recommend USB adapters for stable and fast connection. Bluetooth is slower and less reliable and wireless has been reported as the worst. If you really want to go buy a Chinese clone, I recommend that it has PIC18F25K80 chip and FTDI chip(for USB) - but even then, the firmware is also a factor - 1.5 should be best(for a Chinese clone), but who knows what you will get. If you want a trusted good adapter, then I think currently for USB vLinker FS USB is the best and with a good price. And if you want to go with a good bluetooth adapter, then I recommend Vgate iCAR Pro, which is also priced good. If you want an ok affordable Chinese elm327, that is branded, then go with KONNWEI KW903. It's about $15 with postage included. But iCar pro is better. This is what I found out by googling and reading about it for 3 days.<br/>

# Installation

## Windows
Download the standalone executable and install the driver for your ELM327 device. 

If you have not received a driver with your adapter, then the drivers can be found here:</br>
http://www.totalcardiagnostics.com/support/Knowledgebase/Article/View/1/0/how-to-install-elm327-usb-cable-on-windows-and-obd2-software <br/>

## Linux
Download the standalone executable and add your user account the privileges of accesing USB and serial ports:
> sudo usermod -a -G dialout $USER </br>
> sudo usermod -a -G tty $USER </br>

After you run these two commands you have to log out and log back in for it to take effect(or restart).

On some distributions you also have to install the libnsl library.

For bluetooth adapters, you will probably need to install this:
> sudo apt-get install bluetooth bluez-utils blueman

## MacOS
Download the standalone executable and add your user account the privileges of accesing USB and serial ports:
> sudo usermod -a -G dialout $USER </br>
> sudo usermod -a -G tty $USER </br>

After you run these two commands you have to log out and log back in for it to take effect(or restart).

# Usage
For bluetooth adapters, you will need to pair the adapter once and then connect to it(for some reason on Linux I had to connect to it manually via command line).

Run the executable or the script, connect the ELM327 to the computer and the car's OBD port, set the iginition on the car to on(you don't have to start the engine) and click CONNECT in the app. To connect, go to Configure, select the right port and the right baudrate and click connect. You can leave it at AUTO and connect, but it will take longer to connect and in some cases it will not connect. Manual is safest and fastest, but AUTO works in most cases. **UPDATE: automatic port and baud detection should now work every time!**

The data will display once you are connected, although most of the sensors display data only when the engine is running. If you connected and then turn the engine on, you have to wait a bit so that the program reconnects.

The program was made with ease of use in mind. With it you can view TESTS data, SENSORS data, FREEZE FRAME data, display and clear the TROUBLE CODES and view live GRAPHS. Currently it only displays live data - no recording and replay is possible.

**NOTE: The program only displays the engine data, not airbags, ABS and body control systems. Even if your adapter supports that, you will need a more specialized program for that.**

### Video presentation on YouTube(click on it):
[![PYOBD Youtube video 2021](https://img.youtube.com/vi/u3oWU_zEY5E/0.jpg)](https://www.youtube.com/watch?v=u3oWU_zEY5E)

# Running the script
## Windows
Install Python3, then run:
> pip install -r requirements.txt </br>

The script is executed by running:
> python3 pyobd.py </br>
## Linux
On Debian 10 and 11 and on Ubuntu, type these commands to install the requirements(on Ubuntu replace libgstreamer-plugins-base1.0 with libgstreamer-plugins-base1.0-0): 
> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev gettext python3-dev python3-pip</br>
> pip3 install -r requirements.txt </br>
> sudo usermod -a -G dialout $USER </br>
> sudo usermod -a -G tty $USER </br>

After you run these two commands you have to log out and log back in for it to take effect(or restart).

In some cases you also have to install the libnsl library.

The script is executed by running:
> python3 pyobd.py </br>

## MacOS
Make sure Python3 is installed, then run:
> pip install -r requirements.txt </br>
> sudo usermod -a -G dialout $USER </br>
> sudo usermod -a -G tty $USER </br>

Now restart or logoff and log back in.

The script is executed by running:
> python3 pyobd.py </br>

# Creating the executable
## Windows
Install Python3. Then run these commands:
> pip3 install -r requirements.txt </br>
> pip3 install pyinstaller </br>
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico;." pyobd.py </br>
## Linux
On Debian 10 and 11 and on Ubuntu, type these commands to install the requirements(on Ubuntu replace libgstreamer-plugins-base1.0 with libgstreamer-plugins-base1.0-0): 
> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev gettext python3-dev python3-pip</br>

In some cases you also have to install the libnsl library.</br>

> pip3 install -r requirements.txt </br>
> pip3 install pyinstaller </br>
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico:." pyobd.py </br>
## MacOS
Make sure that you have Python 3 installed. Then run these commands:
> pip3 install -r requirements.txt </br>
> pip3 install pyinstaller </br>
> pyinstaller --onefile -w -i pyobd.ico --add-data "pyobd.ico:." pyobd.py </br>

# Troubleshooting:
If you encounter any bugs or problems you can e-mail me at
![email](/email.png)
and I will try to fix the bug/problem as soon as possible.

You don't have to, but you are welcome to support me, so I can keep this project running. Even better, I can improve it.</br>
[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/jpoljsak/)

## ON THE TO-DO LIST:<br />
-adding sensor data recording and replay feature.</br>
![ELM327](/elm327.jpg)
