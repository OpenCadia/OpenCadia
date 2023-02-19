#!/usr/bin/env python
###########################################################################
# odb_io.py
# 
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
# Copyright 2021 Jure Poljsak (https://github.com/barracuda-fsh/pyobd)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

from pdb import set_trace as bp
import serial
import string
import time
from math import ceil
import wx #due to debugEvent messaging

import re

import obd_sensors

from obd_sensors import hex_to_int

import obd
import decimal


def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

GET_DTC_COMMAND   = "03"
CLEAR_DTC_COMMAND = "04"
GET_FREEZE_DTC_COMMAND = "07"
import traceback
from debugEvent import *
import logging
logger = logging.getLogger(__name__)

#__________________________________________________________________________
def decrypt_dtc_code(code):
    """Returns the 5-digit DTC code from hex encoding"""
    dtc = []
    current = code
    for i in range(0,3):
        if len(current)<4:
            raise "Tried to decode bad DTC: %s" % code

        tc = obd_sensors.hex_to_int(current[0]) #typecode
        tc = tc >> 2
        if   tc == 0:
            type = "P"
        elif tc == 1:
            type = "C"
        elif tc == 2:
            type = "B"
        elif tc == 3:
            type = "U"
        else:
            raise tc

        dig1 = str(obd_sensors.hex_to_int(current[0]) & 3)
        dig2 = str(obd_sensors.hex_to_int(current[1]))
        dig3 = str(obd_sensors.hex_to_int(current[2]))
        dig4 = str(obd_sensors.hex_to_int(current[3]))
        dtc.append(type+dig1+dig2+dig3+dig4)
        current = current[4:]
    return dtc
#__________________________________________________________________________

class OBDConnection:

    def __init__(self,portnum,_notify_window, baud, SERTIMEOUT,RECONNATTEMPTS, FAST):
        self._notify_window = _notify_window
        if baud == 'AUTO':
            baud = None
        if portnum == 'AUTO':
            portnum = None
        if FAST == 'FAST':
            FAST = True
        else:
            FAST = False

        counter = 0
        while counter < RECONNATTEMPTS:
            counter = counter + 1
            wx.PostEvent(self._notify_window, DebugEvent([2, "Connection attempt:" + str(counter)]))
            try:
                self.connection.close()
            except:
                pass
            self.connection = obd.OBD(portstr=portnum,baudrate=baud,fast=FAST, timeout=truncate(float(SERTIMEOUT),1))
            if self.connection.status() == "Car Connected":
                wx.PostEvent(self._notify_window, DebugEvent([2, "Connected to: "+ str(self.connection.port_name())]))
                break
            else:
                self.connection.close()

    def close(self):
        """ Resets device and closes all associated filehandles"""
        self.connection.close()
        self.ELMver = "Unknown"

    def sensor(self , sensor_index):
        """Returns 3-tuple of given sensors. 3-tuple consists of
         (Sensor Name (string), Sensor Value (string), Sensor Unit (string) ) """
        ###for command in self.connection.supported_commands[1].name
        pass
        #sensor = obd_sensors.SENSORS[sensor_index]
        #r = self.get_sensor_value(sensor)
        #return (sensor.name,r, sensor.unit)

    def sensor_names(self):
        """Internal use only: not a public interface"""
        names = []
        for s in obd_sensors.SENSORS:
            names.append(s.name)
        return names
    """
    def get_tests_MIL(self):

        #if not r.is_null():
        #    print(r.value)

        statusText = ["Unsupported", "Supported - Completed", "Unsupported", "Supported - Incompleted"]
        # statusRes = self.sensor(1)[1] #GET values
        statusTrans = []  # translate values to text

        statusRes = []
        for i in range (0,len(self.connection.supported_commands[6])):
            #self.connection.supported_commands[6][i].desc
            #self.connection.supported_commands[6][i].desc
            r = self.connection.query(self.connection.supported_commands[6][i])
            statusRes[i] = str(r.value)
            print (statusRes[i])
            statusTrans.append(str(statusRes[i]))  # DTCs
            if statusRes[i] == 0:
                statusTrans.append("Off")
            else:
                statusTrans.append("On")
         
        #if statusRes[1]==0: #MIL
        #    statusTrans.append("Off")
        #else:
        #    statusTrans.append("On")
            
        for i in range(0,len(statusRes)): #Tests

            statusTrans.append(statusText[statusRes[i]]) 
        print (statusTrans)

        return statusTrans

     #
     # fixme: j1979 specifies that the program should poll until the number
     # of returned DTCs matches the number indicated by a call to PID 01
     #
    """
    def get_dtc(self):
        """Returns a list of all pending DTC codes. Each element consists of
        a 2-tuple: (DTC code (string), Code description (string) )"""
        pass
              
    def clear_dtc(self):
        """Clears all DTCs and freeze frame data"""
        #self.send_command(CLEAR_DTC_COMMAND)
        #r = self.get_result()
        r = self.connection.query(obd.commands["CLEAR_DTC"])
        return r

    def log(self, sensor_index, filename): 
        file = open(filename, "w")
        start_time = time.time() 
        if file:
            data = self.sensor(sensor_index)
            file.write("%s     \t%s(%s)\n" % \
                         ("Time", string.strip(data[0]), data[2])) 
            while 1:
                now = time.time()
                data = self.sensor(sensor_index)
                line = "%.6f,\t%s\n" % (now - start_time, data[1])
                file.write(line)
                file.flush()
          
