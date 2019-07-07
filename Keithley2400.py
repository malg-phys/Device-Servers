# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:32:33 2018

@author: Kaifei Kang
"""

import visa
rm=visa.ResourceManager()
import time
import numpy as np
class Keithley2400():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
        
    def set_volt(self,value):
#        self.inst.write(":SOUR:FUNC 'VOLT'")
        self.inst.write(":SOUR:VOLT:LEV "+str(value))

    def set_curr(self,value):
#        self.inst.write(":SOUR:FUNC 'CURR'")
        self.inst.write(":SOUR:CURR:LEV "+str(value))
        
    def get_volt(self):
        self.x=self.inst.query(":MEAS:VOLT?")
        return (self.x.split(',')[0])
    
    def get_curr(self):
        self.x=self.inst.query(":MEAS:CURR?")
        self.x=self.x.strip('\n').split(',')[0]
        return (self.x)
    
    def ramp_gate(self,start,end):
        self.list=np.linspace(start,end,101)
        for i in range(len(self.list)):
            self.set_volt(self.list[i])
            time.sleep(0.3)

    def ramp_curr(self,start,end):
        self.list=np.linspace(start,end,51)
        for i in range(len(self.list)):
            self.set_curr(self.list[i])
            self.get_volt()
            time.sleep(0.3)
            
    def closeall(self):
        self.inst.close()
    
    
        