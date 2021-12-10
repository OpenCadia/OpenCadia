#!/usr/bin/env python
############################################################################
#
# wxgui.py
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
############################################################################
import numpy as np
import multiprocessing
from multiprocessing import Queue, Process
# import wxversion
# wxversion.select("2.6")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
matplotlib.use('wxAgg')
import traceback
import wx
import pdb
import obd_io  # OBD2 funcs
import os  # os.environ
import decimal
import glob

import threading
import sys
import serial
import platform
import time
import configparser  # safe application configuration
import webbrowser  # open browser from python
#from multiprocessing import Process
#from multiprocessing import Queue

from obd2_codes import pcodes
from obd2_codes import ptest

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import obd
from obd import OBDStatus

ID_ABOUT = 101
ID_EXIT = 110
ID_CONFIG = 500
ID_CLEAR = 501
ID_GETC = 502
ID_RESET = 503
ID_LOOK = 504
ALL_ON = 505
ALL_OFF = 506

ID_DISCONNECT = 507
ID_HELP_ABOUT = 508
ID_HELP_VISIT = 509
ID_HELP_ORDER = 510

# Define notification event for sensor result window
EVT_RESULT_ID = 1000
EVT_MAF_ID = 1005
EVT_TPS_ID = 1006
EVT_TPS_GRAPH_ID = 1007
EVT_MAF_GRAPH_ID = 1008
EVT_GRAPH_VALUE_ID = 1036
EVT_GRAPH_ID = 1035
EVT_COMBOBOX = 1036
EVT_CLOSE_ID = 1037
EVT_BUILD_COMBOBOX_ID = 1038
EVT_DESTROY_COMBOBOX_ID = 1039
EVT_COMBOBOX_GETSELECTION_ID = 1040
EVT_INSERT_SENSOR_ROW_ID = 1041
EVT_INSERT_FREEZEFRAME_ROW_ID = 1042
EVT_FREEZEFRAME_RESULT_ID = 1043

lock = threading.Lock()

TESTS = ["MISFIRE_MONITORING",
    "FUEL_SYSTEM_MONITORING",
    "COMPONENT_MONITORING",
    "CATALYST_MONITORING",
    "HEATED_CATALYST_MONITORING",
    "EVAPORATIVE_SYSTEM_MONITORING",
    "SECONDARY_AIR_SYSTEM_MONITORING",
    "OXYGEN_SENSOR_MONITORING",
    "OXYGEN_SENSOR_HEATER_MONITORING",
    "EGR_VVT_SYSTEM_MONITORING",
    "NMHC_CATALYST_MONITORING",
    "NOX_SCR_AFTERTREATMENT_MONITORING",
    "BOOST_PRESSURE_MONITORING",
    "EXHAUST_GAS_SENSOR_MONITORING",
    "PM_FILTER_MONITORING"]

def EVT_RESULT(win, func, id):
    """Define Result Event."""
    win.Connect(-1, -1, id, func)

"""
class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.label = wx.StaticText(self, label="What Programming Language You Like?", pos=(50, 30))

        languages = ['Java', 'C++', 'C#', 'Python', 'Erlang', 'PHP', 'Ruby']
        self.combobox = wx.ComboBox(self, choices=languages, pos=(50, 50))

        self.label2 = wx.StaticText(self, label="", pos=(50, 80))

        self.Bind(wx.EVT_COMBOBOX, self.OnCombo)

    def OnCombo(self, event):
        self.label2.SetLabel("You Like " + self.combobox.GetValue())
"""
# event pro akutalizaci Trace tabu
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class FreezeframeResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_FREEZEFRAME_RESULT_ID)
        self.data = data

class InsertSensorRowEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_INSERT_SENSOR_ROW_ID)
        self.data = data

class InsertFreezeframeRowEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_INSERT_FREEZEFRAME_ROW_ID)
        self.data = data

class TPSEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TPS_ID)
        self.data = data

class BuildComboBoxEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BUILD_COMBOBOX_ID)
        self.data = data

class DestroyComboBoxEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DESTROY_COMBOBOX_ID)
        self.data = data

class GetSelectionComboBoxEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_COMBOBOX_GETSELECTION_ID)
        self.data = data



class TPSGraphEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TPS_GRAPH_ID)
        #self.data = data

class MAFEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_MAF_ID)
        self.data = data

class GraphValueEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_GRAPH_VALUE_ID)
        self.data = data

class MAFGraphEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_MAF_GRAPH_ID)
        #self.data = data

class GraphEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_GRAPH_ID)
        self.data = data

# event pro aktualizaci DTC tabu
EVT_DTC_ID = 1001


class DTCEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DTC_ID)
        self.data = data


# event pro aktualizaci status tabu
EVT_STATUS_ID = 1002


class StatusEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_STATUS_ID)
        self.data = data

class CloseEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_CLOSE_ID)
        self.data = data


# event pro aktualizaci tests tabu
EVT_TESTS_ID = 1003


class TestEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TESTS_ID)
        self.data = data


# defines notification event for debug tracewindow
from debugEvent import *


class MyApp(wx.App):
    # A listctrl which auto-resizes the column boxes to fill
    class MyListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
        def __init__(self, parent, id, pos=wx.DefaultPosition,
                     size=wx.DefaultSize, style=0):
            wx.ListCtrl.__init__(self, parent, id, pos, size, style)
            ListCtrlAutoWidthMixin.__init__(self)

    class sensorProducer(threading.Thread):
        def __init__(self, _notify_window, portName, SERTIMEOUT, RECONNATTEMPTS, BAUDRATE, FAST, _nb):
            from queue import Queue
            self.portName = portName
            self.RECONNATTEMPTS = RECONNATTEMPTS
            self.SERTIMEOUT = SERTIMEOUT
            self.port = None
            self._notify_window = _notify_window
            self.baudrate = BAUDRATE
            self.FAST = FAST
            self._nb = _nb
            threading.Thread.__init__(self)


        def initCommunication(self):
            self.connection = obd_io.OBDConnection(self.portName, self._notify_window, self.baudrate, self.SERTIMEOUT,self.RECONNATTEMPTS, self.FAST)
            # self.port     = obd_io.OBDPort(self.portName,self._notify_window,self.SERTIMEOUT,self.RECONNATTEMPTS)

            if self.connection.connection.status() != 'Car Connected':  # Cant open serial port
                return None
            else:
                wx.PostEvent(self._notify_window, DebugEvent([1, "Communication initialized..."]))
                return "OK"

            # if self.port.State==0: #Cant open serial port
            #    return None

        def run(self):
            wx.PostEvent(self._notify_window, StatusEvent([0, 1, "Connecting...."]))
            self.initCommunication()

            if not self.connection.connection.status() == 'Car Connected':
                wx.PostEvent(self._notify_window, StatusEvent([666]))  # signal apl, that communication was disconnected
                wx.PostEvent(self._notify_window, StatusEvent([0, 1, "Error cant connect..."]))
                self.stop()
                return None

            # if self.port.State==0: #cant connect, exit thread
            #    self.stop()
            #    wx.PostEvent(self._notify_window, StatusEvent([666])) #signal apl, that communication was disconnected
            #    wx.PostEvent(self._notify_window, StatusEvent([0,1,"Error cant connect..."]))
            #    return None

            wx.PostEvent(self._notify_window, StatusEvent([0, 1, "Car connected!"]))

            r = self.connection.connection.query(obd.commands.ELM_VERSION)
            self.ELMver = str(r.value)
            self.protocol = self.connection.connection.protocol_name()

            wx.PostEvent(self._notify_window, StatusEvent([2, 1, str(self.ELMver)]))
            wx.PostEvent(self._notify_window, StatusEvent([1, 1, str(self.protocol)]))
            wx.PostEvent(self._notify_window, StatusEvent([3, 1, str(self.connection.connection.port_name())]))
            try:
                r = self.connection.connection.query(obd.commands.VIN)
                if r.vale != None:
                    self.VIN = str(r.value)
                    wx.PostEvent(self._notify_window, StatusEvent([4, 1, str(self.VIN)]))
            except:
                pass
            """
            try:
                #r = self.connection.connection.query(obd.commands.ECU_NAME)
                #self.ECU_NAME = str(r.value)
                self.ECU_NAME = obd.commands.ECU_NAME
                wx.PostEvent(self._notify_window, StatusEvent([5, 1, str(self.ECU_NAME)]))
            except:
                pass
                #traceback.print_exc()
            """
            prevstate = -1
            curstate = -1
            #print(self.connection.connection.supported_commands)




            first_time_sensors = True
            first_time_freezeframe = True
            first_time_maf = True
            first_time_tps = True
            first_time_graph = True
            self.graph_x_vals = np.array([])
            self.graph_y_vals = np.array([])
            self.tps_counter = 0
            self.tps_dirty = False
            self.maf_counter = 0
            self.maf_dirty = False
            self.graph_counter = 0
            self.graph_dirty = False
            while self._notify_window.ThreadControl != 666:
                prevstate = curstate
                curstate = self._nb.GetSelection()  # picking the tab in the GUI
                if curstate != 5:
                    first_time_tps = True

                if curstate != 6:
                    first_time_maf = True

                if curstate != 7:
                    first_time_graph = True
                """
                if prevstate == 5 and curstate != 5:
                    try:
                        plt.close(app.fig_tps)
                    except:
                        pass
                if prevstate == 6 and curstate != 6:
                    try:
                        plt.close(app.fig_maf)
                    except:
                        pass
                """
                if prevstate == 7 and curstate != 7:
                    #try:
                    #    plt.close(app.fig_graph)
                    #except:
                    #    pass
                    wx.PostEvent(self._notify_window, GraphValueEvent([0, 0, ""]))
                    wx.PostEvent(self._notify_window, GraphValueEvent([0, 1, ""]))
                    wx.PostEvent(self._notify_window, GraphValueEvent([0, 2, ""]))

                if curstate == 0:  # show status tab

                    #first_time_tps = True
                    pass
                elif curstate == 1:  # show tests tab
                    #first_time_tps = True
                    r = self.connection.connection.query(obd.commands[1][1])
                    #counter = 0
                    #for val in dir(r.value):
                    #    print (val.available)
                    #    print (val.complete)

                    if r.value.MISFIRE_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([0, 1, "Available"]))
                        if r.value.MISFIRE_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([0, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([0, 2, "Incomplete"]))
                    if r.value.FUEL_SYSTEM_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([1, 1, "Available"]))
                        if r.value.FUEL_SYSTEM_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([1, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([1, 2, "Incomplete"]))
                    if r.value.COMPONENT_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([2, 1, "Available"]))
                        if r.value.COMPONENT_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([2, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([2, 2, "Incomplete"]))

                    if r.value.CATALYST_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([3, 1, "Available"]))
                        if r.value.CATALYST_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([3, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([3, 2, "Incomplete"]))

                    if r.value.HEATED_CATALYST_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([4, 1, "Available"]))
                        if r.value.HEATED_CATALYST_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([4, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([4, 2, "Incomplete"]))

                    if r.value.EVAPORATIVE_SYSTEM_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([5, 1, "Available"]))
                        if r.value.EVAPORATIVE_SYSTEM_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([5, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([5, 2, "Incomplete"]))

                    if r.value.SECONDARY_AIR_SYSTEM_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([6, 1, "Available"]))
                        if r.value.SECONDARY_AIR_SYSTEM_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([6, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([6, 2, "Incomplete"]))

                    if r.value.OXYGEN_SENSOR_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([7, 1, "Available"]))
                        if r.value.OXYGEN_SENSOR_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([7, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([7, 2, "Incomplete"]))

                    if r.value.OXYGEN_SENSOR_HEATER_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([8, 1, "Available"]))
                        if r.value.OXYGEN_SENSOR_HEATER_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([8, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([8, 2, "Incomplete"]))

                    if r.value.EGR_VVT_SYSTEM_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([9, 1, "Available"]))
                        if r.value.EGR_VVT_SYSTEM_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([9, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([9, 2, "Incomplete"]))

                    if r.value.NMHC_CATALYST_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([10, 1, "Available"]))
                        if r.value.NMHC_CATALYST_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([10, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([10, 2, "Incomplete"]))

                    if r.value.NOX_SCR_AFTERTREATMENT_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([11, 1, "Available"]))
                        if r.value.NOX_SCR_AFTERTREATMENT_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([11, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([11, 2, "Incomplete"]))

                    if r.value.BOOST_PRESSURE_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([12, 1, "Available"]))
                        if r.value.BOOST_PRESSURE_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([12, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([12, 2, "Incomplete"]))

                    if r.value.EXHAUST_GAS_SENSOR_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([13, 1, "Available"]))
                        if r.value.EXHAUST_GAS_SENSOR_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([13, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([13, 2, "Incomplete"]))

                    if r.value.PM_FILTER_MONITORING.available:
                        wx.PostEvent(self._notify_window, TestEvent([14, 1, "Available"]))
                        if r.value.PM_FILTER_MONITORING.complete:
                            wx.PostEvent(self._notify_window, TestEvent([14, 2, "Complete"]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([14, 2, "Incomplete"]))
                    try:
                        r = self.connection.connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_1)
                        result = r.value.MISFIRE_COUNT
                        if not result.is_null():
                            wx.PostEvent(self._notify_window, TestEvent([15, 2, str(result.value)]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([15, 2, "Misfire count wasn't reported"]))
                        r = self.connection.connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_2)
                        result = r.value.MISFIRE_COUNT
                        if not result.is_null():
                            wx.PostEvent(self._notify_window, TestEvent([16, 2, str(result.value)]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([16, 2, "Misfire count wasn't reported"]))
                        r = self.connection.connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_3)
                        result = r.value.MISFIRE_COUNT
                        if not result.is_null():
                            wx.PostEvent(self._notify_window, TestEvent([17, 2, str(result.value)]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([17, 2, "Misfire count wasn't reported"]))
                        r = self.connection.connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_4)
                        result = r.value.MISFIRE_COUNT
                        if not result.is_null():
                            wx.PostEvent(self._notify_window, TestEvent([18, 2, str(result.value)]))
                        else:
                            wx.PostEvent(self._notify_window, TestEvent([18, 2, "Misfire count wasn't reported"]))
                    except:
                        #traceback.print_exc()
                        pass
                    """
                    "MISFIRE_MONITORING",
                    "FUEL_SYSTEM_MONITORING",
                    "COMPONENT_MONITORING",
                    "CATALYST_MONITORING",
                    "HEATED_CATALYST_MONITORING",
                    "EVAPORATIVE_SYSTEM_MONITORING",
                    "SECONDARY_AIR_SYSTEM_MONITORING",
                    "OXYGEN_SENSOR_MONITORING",
                    "OXYGEN_SENSOR_HEATER_MONITORING",
                    "EGR_VVT_SYSTEM_MONITORING",
                    "NMHC_CATALYST_MONITORING",
                    "NOX_SCR_AFTERTREATMENT_MONITORING",
                    "BOOST_PRESSURE_MONITORING",
                    "EXHAUST_GAS_SENSOR_MONITORING",
                    "PM_FILTER_MONITORING"
                    """
                    #for t in TESTS:
                        #print (t)
                        #app.OBDTests.SetItem(counter, 1, r.value.MISFIRE_MONITORING.available)
                        #app.OBDTests.SetItem(counter, 2, r.value.MISFIRE_MONITORING.complete)
                        #available = globals()["r.value."+t+".available"]
                        #complete = globals()["r.value."+t+".complete"]
                        #wx.PostEvent(self._notify_window, TestEvent([0, 1, r.value.MISFIRE_MONITORING.available]))
                        #wx.PostEvent(self._notify_window, TestEvent([0, 2, r.value.MISFIRE_MONITORING.complete]))
                        #counter = counter + 1

                    #for i in range(0, len(res)):
                    #    app.PostEvent(self._notify_window, TestEvent([i, 1, res[i]]))
                    pass
                elif curstate == 2:  # show sensor tab

                    if first_time_sensors:
                        sensor_list = []
                        counter = 0
                        first_time_sensors = False
                        for command in obd.commands[1]:
                            if command:
                                if command.command not in (b"0100" , b"0101" , b"0102" , b"0113" , b"0120" , b"0121", b"0140"):
                                    s = self.connection.connection.query(command)
                                    if s.value == None:
                                        continue
                                    else:
                                        sensor_list.append([command.command, command.desc, str(s.value)])

                                        #app.sensors.InsertItem(counter, "")
                                        wx.PostEvent(self._notify_window, InsertSensorRowEvent(counter))
                                        wx.PostEvent(self._notify_window, ResultEvent([counter, 0, str(command.command)]))
                                        wx.PostEvent(self._notify_window, ResultEvent([counter, 1, str(command.desc)]))
                                        wx.PostEvent(self._notify_window, ResultEvent([counter, 2, str(s.value)]))
                                        counter = counter + 1
                    else:
                        #for i in range(0, app.sensors.GetItemCount()):
                        #    app.sensors.DeleteItem(0)
                        counter = 0
                        for sens in sensor_list:
                            for command in obd.commands[1]:
                                if command.command == sens[0]:
                                    s = self.connection.connection.query(command)
                                    sensor_list[counter] = [command.command, command.desc, str(s.value)]
                                    counter = counter + 1
                        counter = 0
                        for sens in sensor_list:
                            wx.PostEvent(self._notify_window, ResultEvent([counter, 0, str(sens[0])]))
                            wx.PostEvent(self._notify_window, ResultEvent([counter, 1, str(sens[1])]))
                            wx.PostEvent(self._notify_window, ResultEvent([counter, 2, str(sens[2])]))
                            counter = counter + 1
                    if self._notify_window.ThreadControl == 666:
                        break
                elif curstate == 3:  # show DTC tab
                    #first_time_tps = True
                    if self._notify_window.ThreadControl == 1:  # clear DTC
                        self.connection.clear_dtc()

                        if self._notify_window.ThreadControl == 666:  # before reset ThreadControl we must check if main thread did not want us to finish
                            break

                        self._notify_window.ThreadControl = 0
                        prevstate = -1  # to reread DTC
                    if self._notify_window.ThreadControl == 2:  # reread DTC

                        prevstate = -1

                        if self._notify_window.ThreadControl == 666:
                            break

                        self._notify_window.ThreadControl = 0

                        pass
                    if prevstate != 3:

                        wx.PostEvent(self._notify_window, DTCEvent(0))  # clear list
                        DTCCodes = self.connection.get_dtc()
                        print(len(DTCCodes))
                        if len(DTCCodes) == 0:
                            wx.PostEvent(self._notify_window, DTCEvent(["", "", "No DTC codes (codes cleared)"]))
                        for i in range(0, len(DTCCodes)):
                            wx.PostEvent(self._notify_window,
                                         DTCEvent([DTCCodes[i][0], DTCCodes[i][1], DTCCodes[i][2]]))

                        pass

                elif curstate == 4:  # show freezeframe tab

                    if first_time_freezeframe:
                        freezeframe_list = []
                        counter = 0
                        first_time_freezeframe = False
                        for command in obd.commands[2]:
                            if command:
                                s = self.connection.connection.query(command)
                                if s.value == None:
                                    continue
                                else:
                                    freezeframe_list.append([command.command, command.desc, str(s.value)])
                                    wx.PostEvent(self._notify_window, InsertFreezeframeRowEvent(counter))
                                    wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 0, str(command.command)]))
                                    wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 1, str(command.desc)]))
                                    wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 2, str(s.value)]))
                                    counter = counter + 1
                    else:
                        counter = 0
                        for sens in freezeframe_list:
                            for command in obd.commands[2]:
                                if command.command == sens[0]:
                                    s = self.connection.connection.query(command)
                                    freezeframe_list[counter] = [command.command, command.desc, str(s.value)]
                                    counter = counter + 1
                        counter = 0
                        for sens in freezeframe_list:
                            wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 0, str(sens[0])]))
                            wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 1, str(sens[1])]))
                            wx.PostEvent(self._notify_window, FreezeframeResultEvent([counter, 2, str(sens[2])]))
                            counter = counter + 1
                    if self._notify_window.ThreadControl == 666:
                        break










                elif curstate == 5:  # show TPS tab
                    s = self.connection.connection.query(obd.commands[1][17])
                    wx.PostEvent(self._notify_window, TPSEvent([0, 0, obd.commands[1][17].command]))
                    wx.PostEvent(self._notify_window, TPSEvent([0, 1, obd.commands[1][17].desc]))
                    wx.PostEvent(self._notify_window, TPSEvent([0, 2, str(s.value)]))

                    if first_time_tps:
                        first_time_tps = False
                        self.tps_x_vals = np.array([])
                        self.tps_y_vals = np.array([])
                        self.tps_max_y_val = 0
                        self.tps_min_y_val = 0

                    #self.tps_x_vals.append(self.tps_counter)
                    self.tps_x_vals = np.append(self.tps_x_vals, self.tps_counter)
                    if float(s.value.magnitude) > self.tps_max_y_val:
                        self.tps_max_y_val = float(s.value.magnitude)
                    if float(s.value.magnitude) < self.tps_min_y_val:
                        self.tps_min_y_val = float(s.value.magnitude)

                    #self.tps_y_vals.append(float(s.value.magnitude))
                    self.tps_y_vals = np.append(self.tps_y_vals, float(s.value.magnitude))
                    if len(self.tps_x_vals) > 300:
                        self.tps_x_vals = np.delete(self.tps_x_vals, (0))
                        self.tps_y_vals = np.delete(self.tps_y_vals, (0))
                    self.tps_counter = self.tps_counter + 1
                    self.tps_dirty = True
                    wx.PostEvent(self._notify_window, TPSGraphEvent())

                elif curstate == 6:  # show MAF tab

                    s = self.connection.connection.query(obd.commands[1][16])
                    wx.PostEvent(self._notify_window, MAFEvent([0, 0, obd.commands[1][16].command]))
                    wx.PostEvent(self._notify_window, MAFEvent([0, 1, obd.commands[1][16].desc]))
                    wx.PostEvent(self._notify_window, MAFEvent([0, 2, str(s.value)]))
                    if first_time_maf:
                        first_time_maf = False
                        #self.maf_x_vals = []
                        #self.maf_y_vals = []
                        self.maf_x_vals = np.array([])
                        self.maf_y_vals = np.array([])
                        self.maf_max_y_val = 0
                        self.maf_min_y_val = 0


                    #self.maf_x_vals.append(self.maf_counter)
                    self.maf_x_vals = np.append(self.maf_x_vals, self.maf_counter)
                    self.maf_y_vals = np.append(self.maf_y_vals, float(s.value.magnitude))
                    #self.maf_y_vals.append(float(s.value.magnitude))
                    if float(s.value.magnitude) > self.maf_max_y_val:
                        self.maf_max_y_val = float(s.value.magnitude)
                    if float(s.value.magnitude) < self.maf_min_y_val:
                        self.maf_maf_y_val = float(s.value.magnitude)
                    if len(self.maf_x_vals) > 300:
                        self.maf_x_vals = np.delete(self.maf_x_vals, (0))
                        self.maf_y_vals = np.delete(self.maf_y_vals, (0))

                    self.maf_counter = self.maf_counter + 1
                    self.maf_dirty = True
                    wx.PostEvent(self._notify_window, MAFGraphEvent())
                elif curstate == 7:  # show Graph tab
                    if first_time_graph:
                        wx.PostEvent(self._notify_window, DestroyComboBoxEvent([]))
                        self.graph_x_vals = np.array([])
                        self.graph_y_vals = np.array([])
                        self.graph_counter = 0
                        self.graph_max_y_val = 0
                        self.graph_min_y_val = 0
                        graph_commands = []
                        self.current_command = None
                        self.graph_dirty = True
                        wx.PostEvent(self._notify_window, GraphEvent(self.current_command))
                        prev_command = None
                        first_time_graph = False
                        for command in obd.commands[1]:
                            if command:
                                if command.command not in (b"0100" , b"0101" , b"0102" , b"0113" , b"0120" , b"0121", b"0140"):
                                    s = self.connection.connection.query(command)
                                    if s.value == None:
                                        continue
                                    else:
                                        graph_commands.append(command)
                        sensor_descriptions = []
                        for command in graph_commands:
                            sensor_descriptions.append(command.desc)
                        wx.PostEvent(self._notify_window, BuildComboBoxEvent(sensor_descriptions))

                    else:
                        app.combobox_sel_finished = False
                        wx.PostEvent(self._notify_window, GetSelectionComboBoxEvent([]))
                        while not app.combobox_sel_finished:
                            time.sleep(0.01)
                        curr_selection = app.combobox_selection

                        if curr_selection != -1:
                            prev_command = self.current_command
                            self.current_command = graph_commands[curr_selection]
                        else:
                            self.current_command = None

                        if self.current_command != None:
                            if (prev_command == None) or (prev_command != self.current_command):
                                #self.graph_x_vals = []
                                #self.graph_y_vals = []
                                self.graph_x_vals = np.array([])
                                self.graph_y_vals = np.array([])

                                self.graph_counter = 0
                                self.graph_max_y_val = 0
                                self.graph_min_y_val = 0

                                self.graph_dirty = True
                                wx.PostEvent(self._notify_window, GraphEvent(self.current_command))
                            else:
                                s = self.connection.connection.query(self.current_command)
                                wx.PostEvent(self._notify_window, GraphValueEvent([0, 0, self.current_command.command]))
                                wx.PostEvent(self._notify_window, GraphValueEvent([0, 1, self.current_command.desc]))
                                wx.PostEvent(self._notify_window, GraphValueEvent([0, 2, str(s.value)]))


                                #self.graph_x_vals.append(self.graph_counter)
                                #self.graph_y_vals.append(float(s.value.magnitude))
                                self.graph_x_vals = np.append(self.graph_x_vals, self.graph_counter)
                                self.graph_y_vals = np.append(self.graph_y_vals, float(s.value.magnitude))

                                if float(s.value.magnitude) > self.graph_max_y_val:
                                    self.graph_max_y_val = float(s.value.magnitude)
                                if float(s.value.magnitude) < self.graph_min_y_val:
                                    self.graph_min_y_val = float(s.value.magnitude)
                                if len(self.graph_x_vals) > 300:
                                    self.graph_x_vals = np.delete(self.graph_x_vals, (0))
                                    self.graph_y_vals = np.delete(self.graph_y_vals, (0))

                                self.graph_counter = self.graph_counter + 1
                                #prev_command = self.current_command
                                self.graph_dirty = True
                                wx.PostEvent(self._notify_window, GraphEvent(self.current_command))
                else:

                    pass
            self.stop()


        """
        def off(self, id):
            if id >= 0 and id < len(self.active): 
                self.active[id] = 0
            else:
                debug("Invalid sensor id")
        def on(self, id):
            if id >= 0 and id < len(self.active): 
                self.active[id] = 1
            else:
                debug("Invalid sensor id")

        def all_off(self):
            for i in range(0, len(self.active)):
                self.off(i)
        def all_on(self):
            for i in range(0, len(self.active)):
                self.off(i)
        """

        def stop(self):
            try: # if stop is called before any connection port is not defined (and not connected )
                self.connection.connection.close()
            except:
                pass

            # if self.port != None: #if stop is called before any connection port is not defined (and not connected )
            #  self.port.close()
            wx.PostEvent(self._notify_window, StatusEvent([0, 1, "Disconnected"]))
            wx.PostEvent(self._notify_window, StatusEvent([1, 1, "----"]))
            wx.PostEvent(self._notify_window, StatusEvent([2, 1, "----"]))
            wx.PostEvent(self._notify_window, StatusEvent([3, 1, "----"]))
            wx.PostEvent(self._notify_window, StatusEvent([4, 1, "----"]))
            #wx.PostEvent(self._notify_window, StatusEvent([5, 1, "----"]))
            wx.PostEvent(self._notify_window, CloseEvent([]))

            #lock.release()
            self.process_active = False
    # class producer end

    def sensor_control_on(self):  # after connection enable few buttons
        self.settingmenu.Enable(ID_CONFIG, False)
        self.settingmenu.Enable(ID_RESET, False)
        self.settingmenu.Enable(ID_DISCONNECT, True)
        self.dtcmenu.Enable(ID_GETC, True)
        self.dtcmenu.Enable(ID_CLEAR, True)
        self.GetDTCButton.Enable(True)
        self.ClearDTCButton.Enable(True)

        def sensor_toggle(e):
            sel = e.m_itemIndex
            state = self.senprod.active[sel]
            print (sel, state)
            if   state == 0:
                self.senprod.on(sel)
                self.sensors.SetItem(sel,1,"1")
            elif state == 1:
                self.senprod.off(sel)
                self.sensors.SetItem(sel,1,"0")
            else:
                traceback.print_exc()
                #debug("Incorrect sensor state")
        
        self.sensors.Bind(wx.EVT_LIST_ITEM_ACTIVATED,sensor_toggle,id=self.sensor_id)                


    def sensor_control_off(self):  # after disconnect disable few buttons
        self.dtcmenu.Enable(ID_GETC, False)
        self.dtcmenu.Enable(ID_CLEAR, False)
        self.settingmenu.Enable(ID_DISCONNECT, False)
        self.settingmenu.Enable(ID_CONFIG, True)
        self.settingmenu.Enable(ID_RESET, True)
        self.GetDTCButton.Enable(False)
        self.ClearDTCButton.Enable(False)
        # http://pyserial.sourceforge.net/                                                    empty function
        # EVT_LIST_ITEM_ACTIVATED(self.sensors,self.sensor_id, lambda : None)




    def build_sensor_page(self):
        HOFFSET_LIST = 0
        # tID = wx.NewId()
        tID = wx.NewIdRef(count=1)
        self.sensor_id = tID
        panel = wx.Panel(self.nb, -1)

        self.sensors = self.MyListCtrl(panel, tID, pos=wx.Point(0, HOFFSET_LIST),
                                     style=
                                     wx.LC_REPORT |
                                     wx.SUNKEN_BORDER |
                                     wx.LC_HRULES |
                                     wx.LC_SINGLE_SEL)

        self.sensors.InsertColumn(0, "PID", width=70)
        self.sensors.InsertColumn(1, "Sensor", format=wx.LIST_FORMAT_RIGHT, width=200)
        self.sensors.InsertColumn(2, "Value")


        ####################################################################
        # This little bit of magic keeps the list the same size as the frame
        def OnPSize(e, win=panel):
            panel.SetSize(e.GetSize())
            self.sensors.SetSize(e.GetSize())

            w, h = self.frame.GetSize()

            self.sensors.SetSize(0, HOFFSET_LIST, w - 10, h - 35)

        panel.Bind(wx.EVT_SIZE, OnPSize)
        ####################################################################

        self.nb.AddPage(panel, "Sensors")

    def build_freezeframe_page(self):
        HOFFSET_LIST = 0
        # tID = wx.NewId()
        tID = wx.NewIdRef(count=1)
        self.freezeframe_id = tID
        panel = wx.Panel(self.nb, -1)

        self.freezeframe = self.MyListCtrl(panel, tID, pos=wx.Point(0, HOFFSET_LIST),
                                       style=
                                       wx.LC_REPORT |
                                       wx.SUNKEN_BORDER |
                                       wx.LC_HRULES |
                                       wx.LC_SINGLE_SEL)

        self.freezeframe.InsertColumn(0, "PID", width=70)
        self.freezeframe.InsertColumn(1, "Sensor", format=wx.LIST_FORMAT_RIGHT, width=200)
        self.freezeframe.InsertColumn(2, "Value")

        ####################################################################
        # This little bit of magic keeps the list the same size as the frame
        def OnPSize(e, win=panel):
            panel.SetSize(e.GetSize())
            self.freezeframe.SetSize(e.GetSize())

            w, h = self.frame.GetSize()

            self.freezeframe.SetSize(0, HOFFSET_LIST, w - 10, h - 35)

        panel.Bind(wx.EVT_SIZE, OnPSize)
        ####################################################################

        self.nb.AddPage(panel, "Freeze frame")


    def build_DTC_page(self):
        HOFFSET_LIST = 30  # offset from the top of panel (space for buttons)
        # tID = wx.NewId()
        tID = wx.NewIdRef(count=1)
        self.DTCpanel = wx.Panel(self.nb, -1)
        self.GetDTCButton = wx.Button(self.DTCpanel, -1, "Get DTC", wx.Point(15, 0))
        self.ClearDTCButton = wx.Button(self.DTCpanel, -1, "Clear DTC", wx.Point(100, 0))

        # bind functions to button click action
        self.DTCpanel.Bind(wx.EVT_BUTTON, self.GetDTC, self.GetDTCButton)
        self.DTCpanel.Bind(wx.EVT_BUTTON, self.QueryClear, self.ClearDTCButton)

        self.dtc = self.MyListCtrl(self.DTCpanel, tID, pos=wx.Point(0, HOFFSET_LIST),
                                   style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self.dtc.InsertColumn(0, "Code", width=100)
        self.dtc.InsertColumn(1, "Status", width=100)
        self.dtc.InsertColumn(2, "Trouble code")

        ####################################################################
        # This little bit of magic keeps the list the same size as the frame
        def OnPSize(e, win=self.DTCpanel):
            self.DTCpanel.SetSize(e.GetSize())
            self.dtc.SetSize(e.GetSize())
            w, h = self.frame.GetSize()
            # I have no idea where 70 comes from
            # self.dtc.SetDimensions(0,HOFFSET_LIST, w-16 , h - 70 )
            self.dtc.SetSize(0, HOFFSET_LIST, w - 16, h - 70)

        self.DTCpanel.Bind(wx.EVT_SIZE, OnPSize)
        ####################################################################

        self.nb.AddPage(self.DTCpanel, "DTC")

    def TraceDebug(self, level, msg):
        if self.DEBUGLEVEL <= level:
            self.trace.Append([str(level), msg])

    def OnInit(self):
        self.ThreadControl = 0  # say thread what to do
        self.COMPORT = 0
        self.senprod = None
        self.DEBUGLEVEL = 0  # debug everything

        # tID = wx.NewId()
        tID = wx.NewIdRef(count=1)
        # read settings from file
        self.config = configparser.RawConfigParser()

        # print platform.system()
        # print platform.mac_ver()[]

        if "OS" in os.environ.keys():  # runnig under windows
            self.configfilepath = "pyobd.ini"
        else:
            self.configfilepath = os.environ['HOME'] + '/.pyobdrc'
        if self.config.read(self.configfilepath) == []:
            self.COMPORT = "/dev/ttyACM0"
            self.RECONNATTEMPTS = 5
            self.SERTIMEOUT = 1
            self.BAUDRATE = "AUTO"
            self.FAST = "FAST"
        else:
            try:
                self.COMPORT = self.config.get("pyOBD", "COMPORT")
                self.RECONNATTEMPTS = self.config.getint("pyOBD", "RECONNATTEMPTS")
                self.SERTIMEOUT = self.config.get("pyOBD", "SERTIMEOUT")
                self.BAUDRATE = self.config.get("pyOBD", "BAUDRATE")
                self.FAST = self.config.get("pyOBD", "FAST")
            except:
                self.COMPORT = "/dev/ttyACM0"
                self.RECONNATTEMPTS = 5
                self.SERTIMEOUT = 1
                self.BAUDRATE = "AUTO"
                self.FAST = "FAST"

        frame = wx.Frame(None, -1, "pyOBD-II")
        self.frame = frame
        ico = wx.Icon('pyobd.gif', wx.BITMAP_TYPE_GIF)
        frame.SetIcon(ico)

        EVT_RESULT(self, self.OnResult, EVT_RESULT_ID)
        EVT_RESULT(self, self.OnDebug, EVT_DEBUG_ID)
        EVT_RESULT(self, self.OnDtc, EVT_DTC_ID)
        EVT_RESULT(self, self.OnStatus, EVT_STATUS_ID)
        EVT_RESULT(self, self.OnTests, EVT_TESTS_ID)
        EVT_RESULT(self, self.OnTPS, EVT_TPS_ID)
        EVT_RESULT(self, self.OnMAF, EVT_MAF_ID)
        EVT_RESULT(self, self.OnTPSGraph, EVT_TPS_GRAPH_ID)
        EVT_RESULT(self, self.OnMAFGraph, EVT_MAF_GRAPH_ID)
        EVT_RESULT(self, self.OnGraphValue, EVT_GRAPH_VALUE_ID)
        EVT_RESULT(self, self.OnGraph, EVT_GRAPH_ID)
        EVT_RESULT(self, self.OnClose, EVT_CLOSE_ID)
        EVT_RESULT(self, self.BuildComboBox, EVT_BUILD_COMBOBOX_ID)
        EVT_RESULT(self, self.DestroyComboBox, EVT_DESTROY_COMBOBOX_ID)
        EVT_RESULT(self, self.GetSelectionComboBox, EVT_COMBOBOX_GETSELECTION_ID)
        EVT_RESULT(self, self.InsertSensorRow, EVT_INSERT_SENSOR_ROW_ID)
        EVT_RESULT(self, self.InsertFreezeframeRow, EVT_INSERT_FREEZEFRAME_ROW_ID)
        EVT_RESULT(self, self.OnFreezeframeResult, EVT_FREEZEFRAME_RESULT_ID)

        # Main notebook frames
        self.nb = wx.Notebook(frame, -1, style=wx.NB_TOP)

        self.status = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.status.InsertColumn(0, "Description", width=200)
        self.status.InsertColumn(1, "Value")
        self.status.Append(["Link State", "Disconnnected"]);
        self.status.Append(["Protocol", "----"]);
        self.status.Append(["Cable version", "----"]);
        self.status.Append(["COM port", "----"]);
        self.status.Append(["VIN number", "----"]);
        #self.status.Append(["ECU NAME", "----"]);

        self.nb.AddPage(self.status, "Status")

        self.OBDTests = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.OBDTests.InsertColumn(0, "Description", width=300)
        self.OBDTests.InsertColumn(1, "Available")
        self.OBDTests.InsertColumn(2, "Complete")
        self.nb.AddPage(self.OBDTests, "Tests")


        self.OBDTests.Append(["MISFIRE_MONITORING", "---", "---"])
        self.OBDTests.Append(["FUEL_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["COMPONENT_MONITORING", "---", "---"])
        self.OBDTests.Append(["CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["HEATED_CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["EVAPORATIVE_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["SECONDARY_AIR_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["OXYGEN_SENSOR_MONITORING", "---", "---"])
        self.OBDTests.Append(["OXYGEN_SENSOR_HEATER_MONITORING", "---", "---"])
        self.OBDTests.Append(["EGR_VVT_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["NMHC_CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["NOX_SCR_AFTERTREATMENT_MONITORING", "---", "---"])
        self.OBDTests.Append(["BOOST_PRESSURE_MONITORING", "---", "---"])
        self.OBDTests.Append(["EXHAUST_GAS_SENSOR_MONITORING", "---", "---"])
        self.OBDTests.Append(["PM_FILTER_MONITORING", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 1", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 2", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 3", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 4", "---", "---"])




        self.build_sensor_page()


        self.build_DTC_page()

        self.build_freezeframe_page()

        # MAF AND TPS ADDED BY J.P.
        self.tps = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.maf = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.graph = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.nb.AddPage(self.tps, "TPS Test")
        self.nb.AddPage(self.maf, "MAF Test")
        self.nb.AddPage(self.graph, "Graph")

        self.tps.InsertColumn(0, "PID", width=70)
        self.tps.InsertColumn(1, "Description", width=200)
        self.tps.InsertColumn(2, "Value")
        self.tps.InsertItem(0, "")





        self.graph.InsertColumn(0, "PID", width=70)
        self.graph.InsertColumn(1, "Description", width=200)
        self.graph.InsertColumn(2, "Value")
        self.graph.InsertItem(0, "")

        self.maf.InsertColumn(0, "PID", width=70)
        self.maf.InsertColumn(1, "Description", width=200)
        self.maf.InsertColumn(2, "Value")
        self.maf.InsertItem(0, "")


        # MAF AND TPS ADDED BY J.P.

        self.trace = self.MyListCtrl(self.nb, tID, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.trace.InsertColumn(0, "Level", width=40)
        self.trace.InsertColumn(1, "Message")
        self.nb.AddPage(self.trace, "Trace")
        self.TraceDebug(1, "Application started")

        # Setting up the menu.
        self.filemenu = wx.Menu()
        self.filemenu.Append(ID_EXIT, "E&xit", " Terminate the program")

        self.settingmenu = wx.Menu()
        self.settingmenu.Append(ID_CONFIG, "Configure", " Configure pyOBD")
        self.settingmenu.Append(ID_RESET, "Connect", " Reopen and connect to device")
        self.settingmenu.Append(ID_DISCONNECT, "Disconnect", "Close connection to device")

        self.dtcmenu = wx.Menu()
        # tady toto nastavi automaticky tab DTC a provede akci
        self.dtcmenu.Append(ID_GETC, "Get DTCs", " Get DTC Codes")
        self.dtcmenu.Append(ID_CLEAR, "Clear DTC", " Clear DTC Codes")
        self.dtcmenu.Append(ID_LOOK, "Code Lookup", " Lookup DTC Codes")

        self.helpmenu = wx.Menu()

        self.helpmenu.Append(ID_HELP_ABOUT, "About this program", " Get DTC Codes")
        self.helpmenu.Append(ID_HELP_VISIT, "Visit program homepage", " Lookup DTC Codes")
        self.helpmenu.Append(ID_HELP_ORDER, "Order OBD-II interface", " Clear DTC Codes")

        # Creating the menubar.
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.filemenu, "&File")  # Adding the "filemenu" to the MenuBar
        self.menuBar.Append(self.settingmenu, "&OBD-II")
        self.menuBar.Append(self.dtcmenu, "&Trouble codes")
        self.menuBar.Append(self.helpmenu, "&Help")

        frame.SetMenuBar(self.menuBar)  # Adding the MenuBar to the Frame content.

        frame.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)  # attach the menu-event ID_EXIT to the
        frame.Bind(wx.EVT_MENU, self.QueryClear, id=ID_CLEAR)
        frame.Bind(wx.EVT_MENU, self.Configure, id=ID_CONFIG)
        frame.Bind(wx.EVT_MENU, self.OpenPort, id=ID_RESET)
        frame.Bind(wx.EVT_MENU, self.OnDisconnect, id=ID_DISCONNECT)
        frame.Bind(wx.EVT_MENU, self.GetDTC, id=ID_GETC)
        frame.Bind(wx.EVT_MENU, self.CodeLookup, id=ID_LOOK)
        frame.Bind(wx.EVT_MENU, self.OnHelpAbout, id=ID_HELP_ABOUT)
        frame.Bind(wx.EVT_MENU, self.OnHelpVisit, id=ID_HELP_VISIT)
        frame.Bind(wx.EVT_MENU, self.OnHelpOrder, id=ID_HELP_ORDER)

        self.SetTopWindow(frame)

        frame.Show(True)
        frame.SetSize((520, 400))
        self.sensor_control_off() # ??? JURE POLJSAK


        return True

    def OnHelpVisit(self, event):
        webbrowser.open("https://github.com/barracuda-fsh/pyobd")

    def OnHelpOrder(self, event):
        webbrowser.open("https://www.google.com/search?q=elm327+obd2+scanner")

    def OnHelpAbout(self, event):  # todo about box
        Text = """  PyOBD is an automotive OBD2 diagnosting application using ELM237 cable.

(C) 2021 Jure Poljsak
(C) 2008-2009 SeCons Ltd.
(C) 2004 Charles Donour Sizemore

https://github.com/barracuda-fsh/pyobd
http://www.obdtester.com/
http://www.secons.com/

  PyOBD is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 2 of the License, or (at your option) any later version.

  PyOBD is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MEHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with PyOBD; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

        # HelpAboutDlg = wx.Dialog(self.frame, id, title="About")

        # box  = wx.BoxSizer(wx.HORIZONTAL)
        # box.Add(wx.StaticText(reconnectPanel,-1,Text,pos=(0,0),size=(200,200)))
        # box.Add(wx.Button(HelpAboutDlg,wx.ID_OK),0)
        # box.Add(wx.Button(HelpAboutDlg,wx.ID_CANCEL),1)

        # HelpAboutDlg.SetSizer(box)
        # HelpAboutDlg.SetAutoLayout(True)
        # sizer.Fit(HelpAboutDlg)
        # HelpAboutDlg.ShowModal()

        self.HelpAboutDlg = wx.MessageDialog(self.frame, Text, 'About', wx.OK | wx.ICON_INFORMATION)
        self.HelpAboutDlg.ShowModal()
        self.HelpAboutDlg.Destroy()

    def OnResult(self, event):
        self.sensors.SetItem(event.data[0], event.data[1], event.data[2])

    def OnFreezeframeResult(self, event):
        self.freezeframe.SetItem(event.data[0], event.data[1], event.data[2])

    def OnStatus(self, event):
        if event.data[0] == 666:  # signal, that connection falied
            self.sensor_control_off()
        else:
            self.status.SetItem(event.data[0], event.data[1], event.data[2])

    def OnTests(self, event):
        self.OBDTests.SetItem(event.data[0], event.data[1], event.data[2])

    def OnMAF(self, event):
        self.maf.SetItem(event.data[0], event.data[1], event.data[2])
    def OnTPS(self, event):
        self.tps.SetItem(event.data[0], event.data[1], event.data[2])
    def OnTPSGraph(self, event):
        try:
            self.fig_tps
        except:
            plt.style.use('fivethirtyeight')
            x_axis_start = 0
            x_axis_end = 100
            x_axis_start = 0
            x_axis_end = 100
            self.fig_tps = Figure(dpi=100)
            #self.fig_tps = Figure(figsize=(100,100))
            self.axes = self.fig_tps.add_subplot()
            self.tps_canvas = FigureCanvas(self.tps, -1, self.fig_tps)
            self.tps_canvas.SetPosition(wx.Point(0, 80))


        def animate():

            if self.senprod.tps_dirty:
                self.axes.clear()
                self.axes.set_xlim(self.senprod.tps_counter - 290, self.senprod.tps_counter + 10)
                #if not np.array_equal(self.senprod.tps_y_vals, np.array([])):
                self.axes.set_ylim((self.senprod.tps_min_y_val)-5, (self.senprod.tps_max_y_val)+5)
                self.axes.set_title(obd.commands[1][17].desc,fontdict={'fontsize': 20, 'fontweight': 'medium'})
                self.axes.plot(self.senprod.tps_x_vals,self.senprod.tps_y_vals, color="b", linewidth=1)
                self.tps_canvas.draw()
                self.senprod.tps_dirty = False
        animate()

    def OnMAFGraph(self, event):
        try:
            self.fig_maf
        except:
            plt.style.use('fivethirtyeight')
            x_axis_start = 0
            x_axis_end = 100


            self.fig_maf = Figure(dpi=100)

            self.maf_axes = self.fig_maf.add_subplot()
            self.maf_canvas = FigureCanvas(self.maf, -1, self.fig_maf)
            self.maf_canvas.SetPosition(wx.Point(0, 80))


        def animate():
            if self.senprod.maf_dirty:
                self.maf_axes.clear()
                self.maf_axes.set_xlim(self.senprod.maf_counter - 290, self.senprod.maf_counter + 10)
                #if not np.array_equal(self.senprod.maf_y_vals,np.array([])):
                self.maf_axes.set_ylim((self.senprod.maf_min_y_val)-5, (self.senprod.maf_max_y_val)+5)
                self.maf_axes.set_title(obd.commands[1][16].desc, fontdict={'fontsize': 20, 'fontweight': 'medium'})
                self.maf_axes.plot(self.senprod.maf_x_vals,self.senprod.maf_y_vals, color="b", linewidth=1)
                self.maf_canvas.draw()
                self.senprod.maf_dirty = False
        animate()

        ###########################
        """
        plt.style.use('fivethirtyeight')
        self.fig_maf = plt.figure()
        x_axis_start = 0
        x_axis_end = 100
        ax = plt.axes(xlim=(x_axis_start, x_axis_end), ylim=(0, 100))

        line, = ax.plot(0, 0)

        def animate(i):
            if self.senprod.maf_dirty:
                line.set_linewidth(1)
                line.set_linewidth(1)
                line.set_xdata(self.senprod.maf_x_vals)
                line.set_ydata(self.senprod.maf_y_vals)
                ax.set_xlim(self.senprod.maf_counter - 290, self.senprod.maf_counter + 10)
                if self.senprod.maf_y_vals != []:
                    ax.set_ylim(0, max(self.senprod.maf_y_vals)+5)
                ax.set_title('MAF grams per second', fontdict={'fontsize': 20, 'fontweight': 'medium'})
                self.senprod.maf_dirty = False
            #plt.pause(0.05)

            return line,

        ani = FuncAnimation(self.fig_maf, animate, blit=False) #, frames=None, interval=1, blit=True)
        ax.axhline(linewidth=1, color="b")
        plt.tight_layout()
        plt.show()
        """

    def OnCombo(self, event):
        self.senprod.curr_selection = self.combobox.GetSelection()

    def InsertSensorRow(self, event):
        counter = event.data
        self.sensors.InsertItem(counter, "")

    def InsertFreezeframeRow(self, event):
        counter = event.data
        self.freezeframe.InsertItem(counter, "")

    def BuildComboBox(self, event):
        self.combobox = wx.ComboBox(self.graph, choices=event.data, pos=(0, 60))

    def DestroyComboBox(self, event):
        try:
            self.combobox
            self.combobox.Destroy()
        except:
            pass

    def GetSelectionComboBox(self, event):
        self.combobox_selection = self.combobox.GetSelection()
        self.combobox_sel_finished = True

    def OnClose(self, event):

        try:
            del self.fig_tps
        except:
            pass
        try:
            del self.fig_maf
        except:
            pass
        try:
            del self.fig_graph
        except:
            pass

        self.sensors.DeleteAllItems()
        self.freezeframe.DeleteAllItems()
        self.OBDTests.DeleteAllItems()
        self.OBDTests.Append(["MISFIRE_MONITORING", "---", "---"])
        self.OBDTests.Append(["FUEL_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["COMPONENT_MONITORING", "---", "---"])
        self.OBDTests.Append(["CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["HEATED_CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["EVAPORATIVE_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["SECONDARY_AIR_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["OXYGEN_SENSOR_MONITORING", "---", "---"])
        self.OBDTests.Append(["OXYGEN_SENSOR_HEATER_MONITORING", "---", "---"])
        self.OBDTests.Append(["EGR_VVT_SYSTEM_MONITORING", "---", "---"])
        self.OBDTests.Append(["NMHC_CATALYST_MONITORING", "---", "---"])
        self.OBDTests.Append(["NOX_SCR_AFTERTREATMENT_MONITORING", "---", "---"])
        self.OBDTests.Append(["BOOST_PRESSURE_MONITORING", "---", "---"])
        self.OBDTests.Append(["EXHAUST_GAS_SENSOR_MONITORING", "---", "---"])
        self.OBDTests.Append(["PM_FILTER_MONITORING", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 1", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 2", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 3", "---", "---"])
        self.OBDTests.Append(["MISFIRE CYLINDER 4", "---", "---"])
        self.dtc.DeleteAllItems()

        self.tps.DeleteAllItems()
        self.maf.DeleteAllItems()
        self.graph.DeleteAllItems()

        #####################
        try:
            self.tps_canvas.Destroy()

        except:
            pass
        try:
            self.maf_canvas.Destroy()
        except:
            pass
        try:
            self.graph_canvas.Destroy()
        except:
            pass

        ############
        self.tps.InsertItem(0, "")
        self.graph.InsertItem(0, "")
        self.maf.InsertItem(0, "")
        try:
            self.combobox.Destroy()
        except:
            pass


    def OnGraph(self, event):
        try:
            self.fig_graph
        except:
            plt.style.use('fivethirtyeight')
            x_axis_start = 0
            x_axis_end = 100


            self.fig_graph = Figure(dpi=100)

            self.graph_axes = self.fig_graph.add_subplot()
            self.graph_canvas = FigureCanvas(self.graph, -1, self.fig_graph)
            self.graph_canvas.SetPosition(wx.Point(0, 120))

        def animate():
            #print (self.senprod.graph_dirty)
            if self.senprod.graph_dirty:
                self.senprod.graph_dirty = False
                self.graph_axes.clear()
                self.graph_axes.set_xlim(self.senprod.graph_counter - 290, self.senprod.graph_counter + 10)
                #if not np.array_equal(self.senprod.graph_y_vals, np.array([])):
                self.graph_axes.set_ylim((self.senprod.graph_min_y_val)-5, (self.senprod.graph_max_y_val)+5)
                try:
                    self.graph_axes.set_title(self.senprod.current_command.desc, fontdict={'fontsize': 20, 'fontweight': 'medium'})
                except:
                    pass
                self.graph_axes.plot(self.senprod.graph_x_vals,self.senprod.graph_y_vals, color="b", linewidth=1)
                self.graph_canvas.draw()
        animate()
        """
        plt.style.use('fivethirtyeight')
        self.fig_graph = plt.figure()
        x_axis_start = 0
        x_axis_end = 100
        ax = plt.axes(xlim=(x_axis_start, x_axis_end), ylim=(-5, 105))

        line, = ax.plot(0, 0)

        def animate(i):
            if self.senprod.graph_dirty:
                x_vals = self.senprod.graph_x_vals
                y_vals = self.senprod.graph_y_vals
                graph_counter = self.senprod.graph_counter
                line.set_linewidth(1)
                line.set_xdata(x_vals)
                line.set_ydata(y_vals)
                ax.set_xlim(graph_counter - 290, graph_counter + 10)
                if y_vals != []:
                    ax.set_ylim(-50, max(y_vals)+5)
                ax.set_title(event.data.desc, fontdict={'fontsize': 20, 'fontweight': 'medium'})
                self.senprod.graph_dirty = False
            #plt.pause(0.05)

            return line,

        ani = FuncAnimation(self.fig_graph, animate, blit=False)#, frames=None, interval=1, blit=False)
        #ax.axhline(linewidth=1, color="b")
        #plt.tight_layout()
        plt.show()
        """
    def OnGraphValue(self, event):
        self.graph.SetItem(event.data[0], event.data[1], event.data[2])

    def OnDebug(self, event):
        self.TraceDebug(event.data[0], event.data[1])

    def OnDtc(self, event):
        if event.data == 0:  # signal, that DTC was cleared
            self.dtc.DeleteAllItems()
        else:
            self.dtc.Append(event.data)

    def OnDisconnect(self, event):  # disconnect connection to ECU
        self.ThreadControl = 666
        self.sensor_control_off()

    def OpenPort(self, e):

        if self.senprod:  # signal current producers to finish
            self.senprod.stop()
        self.ThreadControl = 0
        self.senprod = self.sensorProducer(self, self.COMPORT, self.SERTIMEOUT, self.RECONNATTEMPTS, self.BAUDRATE, self.FAST, self.nb)
        self.senprod.process_active = True
        self.senprod.start()

        self.sensor_control_on()

    def GetDTC(self, e):
        self.nb.SetSelection(3)
        self.ThreadControl = 2

    def AddDTC(self, code):
        self.dtc.InsertStringItem(0, "")
        self.dtc.SetItem(0, 0, code[0])
        self.dtc.SetItem(0, 1, code[1])

    def CodeLookup(self, e=None):
        id = 0
        diag = wx.Frame(None, id, title="Diagnostic Trouble Codes")
        ico = wx.Icon('pyobd.gif', wx.BITMAP_TYPE_GIF)
        diag.SetIcon(ico)
        tree = wx.TreeCtrl(diag, id, style=wx.TR_HAS_BUTTONS)

        root = tree.AddRoot("Code Reference")
        proot = root;  # tree.AppendItem(root,"Powertrain (P) Codes")
        codes = pcodes.keys()
        codes = sorted(codes)
        group = ""
        for c in codes:
            if c[:3] != group:
                group_root = tree.AppendItem(proot, c[:3] + "XX")
                group = c[:3]
            leaf = tree.AppendItem(group_root, c)
            tree.AppendItem(leaf, pcodes[c])

        diag.SetSize((400, 500))
        diag.Show(True)

    def QueryClear(self, e):
        id = 0
        diag = wx.Dialog(self.frame, id, title="Clear DTC?")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(diag, -1, "Are you sure you wish to"), 0)
        sizer.Add(wx.StaticText(diag, -1, "clear all DTC codes and "), 0)
        sizer.Add(wx.StaticText(diag, -1, "freeze frame data?      "), 0)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.Button(diag, wx.ID_OK, "Ok"), 0)
        box.Add(wx.Button(diag, wx.ID_CANCEL, "Cancel"), 0)

        sizer.Add(box, 0)
        diag.SetSizer(sizer)
        diag.SetAutoLayout(True)
        sizer.Fit(diag)
        r = diag.ShowModal()
        if r == wx.ID_OK:
            self.ClearDTC()

    def ClearDTC(self):
        self.ThreadControl = 1
        self.nb.SetSelection(3)

    def try_port(self, portStr):
        """returns boolean for port availability"""
        try:
            s = serial.Serial(portStr)
            s.close()  # explicit close 'cause of delayed GC in java
            return True

        except serial.SerialException:
            pass
        except:
            traceback.print_exc()

        return False

    def scanSerial(self):  # NEW

        """scan for available ports. return a list of serial names"""
        available = []
        available = obd.scan_serial()

        return available

    def Configure(self, e=None):
        id = 0
        diag = wx.Dialog(self.frame, id, title="Configure")
        sizer = wx.BoxSizer(wx.VERTICAL)

        ports = obd.scan_serial()
        if ports == []:
            ports = ["AUTO"]
        else:
            ports.append("AUTO")

        # web open link button
        self.OpenLinkButton = wx.Button(diag, -1, "Click here to order ELM-USB interface", size=(260, 30))
        diag.Bind(wx.EVT_BUTTON, self.OnHelpOrder, self.OpenLinkButton)
        sizer.Add(self.OpenLinkButton)
        rb = wx.RadioBox(diag, id, "Choose Serial Port",
                         choices=ports, style=wx.RA_SPECIFY_COLS,
                         majorDimension=2)

        sizer.Add(rb, 0)
        baudrates = ['AUTO', '38400', '9600', '230400', '115200', '57600', '19200']
        brb = wx.RadioBox(diag, id, "Choose Baud Rate",
                         choices=baudrates, style=wx.RA_SPECIFY_COLS,
                         majorDimension=2)

        sizer.Add(brb, 0)
        fb = wx.RadioBox(diag, id, "FAST or NORMAL:",
                         choices=["FAST","NORMAL"], style=wx.RA_SPECIFY_COLS,
                         majorDimension=2)

        sizer.Add(fb, 0)
        # timeOut input control
        timeoutPanel = wx.Panel(diag, -1)
        timeoutCtrl = wx.TextCtrl(timeoutPanel, -1, '', pos=(140, 0), size=(40, 25))
        timeoutStatic = wx.StaticText(timeoutPanel, -1, 'Timeout:', pos=(3, 5), size=(140, 20))
        timeoutCtrl.SetValue(str(self.SERTIMEOUT))

        # reconnect attempt input control
        reconnectPanel = wx.Panel(diag, -1)
        reconnectCtrl = wx.TextCtrl(reconnectPanel, -1, '', pos=(140, 0), size=(40, 25))
        reconnectStatic = wx.StaticText(reconnectPanel, -1, 'Reconnect attempts:', pos=(3, 5), size=(140, 20))
        reconnectCtrl.SetValue(str(self.RECONNATTEMPTS))



        # set actual serial port choice
        if (self.COMPORT != 0) and (self.COMPORT in ports):
            rb.SetSelection(ports.index(self.COMPORT))
        baudrates = ['AUTO', '38400', '9600', '230400', '115200', '57600', '19200']
        if (self.BAUDRATE != 0) and (self.BAUDRATE in baudrates):
            brb.SetSelection(baudrates.index(self.BAUDRATE))
        if (self.FAST == "FAST") or (self.FAST == "NORMAL"):
            fb.SetSelection(["FAST","NORMAL"].index(self.FAST))


        sizer.Add(timeoutPanel, 0)
        sizer.Add(reconnectPanel, 0)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.Button(diag, wx.ID_OK), 0)
        box.Add(wx.Button(diag, wx.ID_CANCEL), 1)

        sizer.Add(box, 0)
        diag.SetSizer(sizer)
        diag.SetAutoLayout(True)
        sizer.Fit(diag)
        r = diag.ShowModal()
        if r == wx.ID_OK:

            # create section
            if self.config.sections() == []:
                self.config.add_section("pyOBD")
            # set and save COMPORT

            self.COMPORT = ports[rb.GetSelection()]
            self.config.set("pyOBD", "COMPORT", self.COMPORT)

            self.BAUDRATE = baudrates[brb.GetSelection()]
            self.config.set("pyOBD", "BAUDRATE", self.BAUDRATE)

            self.FAST = ["FAST","NORMAL"][fb.GetSelection()]
            self.config.set("pyOBD", "FAST", self.FAST)

            # set and save SERTIMEOUT
            self.SERTIMEOUT = timeoutCtrl.GetValue()
            self.config.set("pyOBD", "SERTIMEOUT", self.SERTIMEOUT)


            # set and save RECONNATTEMPTS
            self.RECONNATTEMPTS = int(reconnectCtrl.GetValue())
            self.config.set("pyOBD", "RECONNATTEMPTS", self.RECONNATTEMPTS)

            # write configuration to cfg file
            self.config.write(open(self.configfilepath, 'w'))

    def OnExit(self, e=None):
        import sys
        try:
            self.senprod._notify_window.ThreadControl = 666
            while self.senprod.process_active !=  False:
                time.sleep(0.1)
            #time.sleep(3)
        except:
            pass
        sys.exit(0)


app = MyApp(0)
app.MainLoop()
