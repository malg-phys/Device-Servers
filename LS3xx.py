# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang
"""
import visa
import numpy as np
rm=visa.ResourceManager()

class LS3xx():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def set_ramprate(self, value):
        self.inst.write('RAMP 1, 1, {}'.format(value))
    
    def set_rampoff(self):
        self.inst.write('RAMP 1, 0, 0')
    
    def set_heater(self, value):
        if value == 'low':
            self.inst.write('RANGE 1')
        elif value == 'med':                ### For LS325, change this to high.
            self.inst.write('RANGE 2')   
        elif value == 'high':               
            self.inst.write('RANGE 3')      ### For LS325, there is no 3 for range
        elif value == 'off':
            self.inst.write('RANGE 0')
        else:
            print('Invalid value. (off/low/high)')
    
    def set_temp(self, value):
        self.inst.write('SETP 1, {}'.format(value))
    
    def get_temp(self):
        self.x = float(self.inst.query('KRDG? A').strip('\r\n'))
        return self.x
    
################################################################################################
        
    def set_curve_header(self, num, name, SN, dataformat, limit, coefficient):
        self.inst.write("CRVHDR {},{},{},{},{},{}".format(num, name, SN, dataformat, limit, coefficient))
    
    def set_curve_point(self, curvenum, index, sensorvalue, tempvalue):
        self.sv = str(sensorvalue)
        self.tv = str(tempvalue)
        self.inst.write("CRVPT {},{},{:.7},{:.7}".format(curvenum, index, self.sv, self.tv))
        
    def get_curve_header(self, num):
        self.x = self.inst.query("CRVHDR? {}".format(num))
        return self.x
    
    def get_curve_point(self, curvenum, index):
        self.x = self.inst.query("CRVPT? {}, {}".format(curvenum, index))
        self.x=self.x.strip('\r\n')
        return self.x
    
    
    def closeall(self):
        self.inst.close()
    
