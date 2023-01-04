# ![PYOBD](/pyobd.gif) PYOBD 
**This is the remake of the free PC program for car diagnostics, aka. reading and displaying your cars OBD2 data(tests, sensors, DTC faults/reset, graphs of live sensor data). If your car supports obd2(which for the last 20 years most of the cars do), then you only need an elm327 adapter and a laptop with this program to diagnose your car. The program is free and open source and it is the only free program that exists for obd2, with this level of functionality, as far as I know. The program is the remake of the program PYOBD. It is much improved over the original pyobd, features live graphs, more displayable data and works on Python3 and all the new libraries. It was tested on Linux, Windows, and it should work on Mac too.**

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/jpoljsak/)

Operating systems on which pyobd was tested so far:
Debian 10, Debian 11, Ubuntu, Windows 7 and 10, MacOSX Monterey.

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for Windows(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13windows-32-bit.exe)
<!-- END LATEST DOWNLOAD BUTTON -->

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for Linux(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13linux)
<!-- END LATEST DOWNLOAD BUTTON -->

<!-- BEGIN LATEST DOWNLOAD BUTTON -->Download for MacOSX(standalone executable - no install needed):
[![Download Windows Executable](https://custom-icon-badges.herokuapp.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download zip")](https://github.com/barracuda-fsh/pyobd/releases/download/v1.13/pyobd1.13macosx.app.zip)
<!-- END LATEST DOWNLOAD BUTTON -->

NOTE: On Windows you will need a suitable driver for your ELM327 device(on Linux it is not needed). You can download drivers from here:  http://www.totalcardiagnostics.com/support/Knowledgebase/Article/View/1/0/how-to-install-elm327-usb-cable-on-windows-and-obd2-software <br/>

**About the program:<br>
The program was made on top of the pyOBD program, which was made by Donour Sizemore. The original program has not been touched for 15 years, which came to my huge surprise, as to why noone worked on it. I decided then, that I will make it my personal project to first make it work on Python 3 and latest libraries, which I successfully did. After that I also expanded its functionality and made it use exclusively the rich Python OBD library, which was made by Brendan Whitfield. So now I have utilized two projects into one. The program is ofcourse still free and open source. So, special thanks goes to Donour Sizemore and Brendan Whitfield. And last, but not least, my name is Jure Poljsak, and this remake was made by me.**

> pyOBD (aka pyOBD-II or pyOBD2) is an OBD-II compliant car diagnostic tool. It is designed to interface with low-cost ELM 32x OBD-II diagnostic interfaces such as ELM327. It will basically allow you to talk to your car's ECU,... display fault codes, display measured values, read status tests, etc. All cars made since 1996 (in the US) or 2001 (in the EU) must be OBD-II compliant, i.e. they should work with pyOBD.

How do you know if your car is OBD-II compliant?
https://www.scantool.net/blog/how-do-i-know-whether-my-car-is-obd-ii-compliant/

**Which ELM327 device am I using and which will work?**<br/>
I am using this one(I bought it 10 years ago):<br/>
-OBDPro USB Scantool (http://www.obdpros.com/product_info.php?products_id=133)<br/>
Others that have been reported to work:<br/>
-OBDLink SX (https://www.obdlink.com/products/obdlink-sx/)<br/>
The Chinese clones may work but not fully and the ones that work (at least mostly) properly are $10 or more. There are multiple reasons why a good adapter is not the cheapest. OBDLink makes good adapters and also VGate - their adapters also receive firmware updates so while they are already very good, they keep improving. I recommend USB adapters for stable and fast connection. Bluetooth is slower and less reliable and wireless has been reported as the worst(I did not check this myself though). If you really want to go buy a Chinese clone, I recommend that it has PIC18F25K80 chip and FTDI chip(for USB) - but even then, the firmware is also a factor - 1.5 should be best(for a Chinese clone), but who knows what you will get. If you want a trusted good adapter, then I think currently for USB vLinker FS USB is the best and with a good price. And if you want to go with a good bluetooth adapter, then I recommend Vgate iCAR Pro, which is also priced good. If you want an ok affordable Chinese elm327, that is branded, then go with KONNWEI KW903. It's about $15 with postage included. But iCar pro is better. This is what I found out by googling and reading about it for 3 days.<br/>

### Video presentation on YouTube(click on it):
[![PYOBD Youtube video 2021](https://img.youtube.com/vi/u3oWU_zEY5E/0.jpg)](https://www.youtube.com/watch?v=u3oWU_zEY5E)
 
On Windows, you can create an .exe file with these three commands(make sure you install Python 3 first):
> pip install -r requirements.txt

> pip install pyinstaller

> pyinstaller --onefile -i pyobd.ico --add-data "pyobd.ico;." pyobd.py

On Debian 10 and 11 and on Ubuntu, type these commands to install the requirements(on Ubuntu replace libgstreamer-plugins-base1.0 with libgstreamer-plugins-base1.0-0): 

> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev

> pip3 install -r requirements.txt

In some cases you need to add to your username the privileges of accessing the USB and serial ports(adding it to the group) for it to work:
> sudo usermod -a -G dialout $USER

> sudo usermod -a -G tty $USER

After that, you have to restart the computer.

If your port is still not listed, you can try just running the program with superuser rights:

> sudo python3 pyobd.py

Otherwise, the program is run by typing: 
> python3 pyobd.py

.... or on Windows by running pyobd.exe if you make the .exe.

The ignition must be on, to connect to the car and display data(key turned one level before engine start). Although most of the sensors display data only when the engine is running. If you connected and then turn the engine on, you must connect to the car again.

The program works nice and I will also add new functionalities to it. I am working on adding graphs and data export/saving(and bugfixes ofcourse).

TO DO LIST:<br />
-add sensor data exporting and replay.

![ELM327](/elm327.jpg)
