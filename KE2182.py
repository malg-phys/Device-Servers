# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang
"""
import visa
import numpy as np
rm=visa.ResourceManager()

class KE2182():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def write(self, value):
        print(self.inst.query(value))
     

    def set_range(self, value):
        self.inst.write(":SENS:VOLT:RANG {}".format(value))
    
    def get_range(self):
        self.x = self.inst.query(":SENS:VOLT:RANG?")
        self.x = float(self.x.split('\n')[0])
        return self.x

    def get_voltage(self):
        self.x = self.inst.query(":MEAS:VOLT?")
        self.x = float(self.x.split('\n')[0])
        return self.x

        
    def closeall(self):
        self.inst.close()
    
