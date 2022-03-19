# ![PYOBD](/pyobd.gif) PYOBD 
**This is the remake of the free PC program for car diagnostics, aka. reading and displaying your cars OBD2 data(tests, sensors, DTC faults/reset, graphs of live sensor data). If your car supports obd2(which for the last 20 years most of the cars do), then you only need an elm327 adapter and a laptop with this program to diagnose your car. The program is free and open source and it is the only free program that exists for obd2, with this level of functionality, as far as I know. The program is the remake of the program PYOBD. It is much improved over the original pyobd, features live graphs, more displayable data and works on Python3 and all the new libraries. It was tested on Linux, Windows, and it should work on Mac too.**

**If you have any problems with the program, write to me at pyobd.jp@gmail.com and I will solve it either by helping you or by correcting the program.**

Operating systems on which pyobd was tested so far(please write to me if you have tested it on other OS-es, so I can add them here):
Debian 10, Debian 11, Windows 7 and 10.

You can download the Windows executable version from here - so no install is needed(it may be recognized as malware, but it is made from code you see here - so it is not malware):<br/>
https://drive.google.com/file/d/1OmU99RYv3QSN7z-KAGXjN9xb9ryiOAQd/view?usp=sharing

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
-Chinese USB ELM OBD2 (1.5a)<br/>
Probably any USB ELM327 adapter will work(but I can not be 100% sure).<br/>

### Video presentation on YouTube(click on it):
[![PYOBD Youtube video 2021](https://img.youtube.com/vi/4PHdCG6qKmQ/0.jpg)](https://www.youtube.com/watch?v=4PHdCG6qKmQ)

On Windows, you can create an .exe file with these three commands(make sure you install Python 3 first):
> pip install -r requirements.txt

> pip install pyinstaller

> pyinstaller --onefile -i pyobd.ico --add-data "pyobd.ico;." pyobd.py

On Debian 10 and 11, type these commands to install the requirements:

> sudo apt-get install dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base1.0 libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev libwebkit2gtk-4.0-dev libxtst-dev

> pip3 install -r requirements.txt

The program is run by typing: 
> python3 pyobd.py

.... or on Windows by running pyobd.exe if you make the .exe.

The ignition must be on, to connect to the car and display data(key turned one level before engine start). Although most of the sensors display data only when the engine is running. If you connected and then turn the engine on, you must connect to the car again.

The program works nice and I will also add new functionalities to it. I am working on adding graphs and data export/saving(and bugfixes ofcourse).

TO DO LIST:<br />
-add multiple graphs<br />
-add sensor data exporting and replay<br />
-catch and handle some errors when connection gets broken.

![ELM327](/elm327.jpg)
