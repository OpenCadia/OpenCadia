# ![PYOBD](/pyobd.gif) PYOBD 
This is the free program for car diagnostics, aka. reading and displaying your cars OBD2 data(tests, sensors, DTC faults/reset, graphs of live sensor data). If your car supports obd2(which for the last 20 years most of the cars do), then you only need an elm327 adapter and a laptop with this program to diagnose your car. The program is free and open source and it is the only free program that exists for obd2, with this level of functionality, as far as I know. The program is the remake of the program PYOBD. It works on Python3 and all new libraries. It was tested on Linux, Windows, and it should work on Mac too. 

You can download the Windows version from here:
https://drive.google.com/file/d/1ezDw-8M1kAfoM-H2r4hrqO70i6d-q98i/view?usp=sharing

NOTE: On Windows you will need a suitable driver for your ELM327 device(on Linux it is not needed). You can download drivers from here:  http://www.totalcardiagnostics.com/support/Knowledgebase/Article/View/1/0/how-to-install-elm327-usb-cable-on-windows-and-obd2-software
NOTE2: Connect using fixed baud rate. Automatic baudrate works, but it takes a looong looong time.

**About the program:<br>
The program was made on top of the pyOBD program, which was made by Donour Sizemore. The original program has not been touched for 15 years, which came to my huge surprise, as to why noone worked on it. I decided then, that I will make it my personal project to first make it work on Python 3 and latest libraries, which I successfully did. After that I also expanded its functionality and made it use exclusively the rich Python OBD library, which was made by Brendan Whitfield. So now I have utilized two projects into one. The program is ofcourse still free and open source. So, special thanks goes to Donour Sizemore and Brendan Whitfield. And last, but not least, my name is Jure Poljsak, and this remake was made by me.**

> pyOBD (aka pyOBD-II or pyOBD2) is an OBD-II compliant car diagnostic tool. It is designed to interface with low-cost ELM 32x OBD-II diagnostic interfaces such as ELM327. It will basically allow you to talk to your car's ECU,... display fault codes, display measured values, read status tests, etc. All cars made since 1996 (in the US) or 2001 (in the EU) must be OBD-II compliant, i.e. they should work with pyOBD.

How do you know if your car is OBD-II compliant?
https://www.scantool.net/blog/how-do-i-know-whether-my-car-is-obd-ii-compliant/

### Video presentation on YouTube(click on it):
[![PYOBD Youtube video 2021](https://img.youtube.com/vi/TjCBmo5vCM8/0.jpg)](https://www.youtube.com/watch?v=TjCBmo5vCM8)

On Windows, you can create an .exe file with these three commands(make sure you install Python 3 first):
> pip install -r requirements.txt

> pip install pyinstaller

> pyinstaller --onefile -i pyobd.ico --add-data "pyobd.ico;." pyobd.py

On Debian 10 type these commands to install the requirements:

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
