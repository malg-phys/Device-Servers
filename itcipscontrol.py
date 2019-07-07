# -*- coding: utf-8 -*-
"""
Created on Sat May 25 20:54:28 2019

@author: paulv
"""
#
import visa
import numpy as np

rm = visa.ResourceManager()
print(rm.list_resources())
##
#ips = rm.open_resource('ASRL7::INSTR')
#ips.baud_rate = 9600
#ips.write_termination = '\r'
#ips.read_termination = '\r'
#ips.query('C3')
#ips.query('H0')         ## heater off
#ips.query('H1')         ## heater on

itc = rm.open_resource('GPIB0::24::INSTR')
itc.baud_rate = 9600
itc.write_termination = '\r'
itc.read_termination = '\r'


itc.query('C3')     #turning on remote
itc.query('A1')     #turn heater into auto
#
itc.query('T1')
itc.query('G20')
#
print(itc.query('R1'))