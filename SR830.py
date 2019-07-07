# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang
"""
import visa
import numpy as np
rm=visa.ResourceManager()

class SR830():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def write(self, value):
        print(self.inst.query(value))
        
    def get_X(self):
        self.x=self.inst.query("OUTP?1")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_Y(self):
        self.x=self.inst.query("OUTP?2")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_R(self):
        self.x=self.inst.query("OUTP?3")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_Theta(self):
        self.x=self.inst.query("OUTP?4")
        self.x = self.x.strip("\n")
        return self.x
    
    def set_AC_Volt(self,value):
        self.inst.write("SLVL"+str(value))
        
    def scan_bias(self,low,high,num):
        self.x=np.linspace(float(low),float(high),int(num)+1)
        for i in range(int(num)+1):
            self.set_AC_Volt(self.x[i])
            self.get_X()
            self.get_Y()
        
    def closeall(self):
        self.inst.close()
    
