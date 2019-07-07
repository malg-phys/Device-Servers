# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang
"""
import visa
import numpy as np
rm=visa.ResourceManager()

class KE6221():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def ask(self, value):
        print(self.inst.query(value))
    
    def write(self, value):
        self.inst.write(value)
      

    def output_on(self):
        self.inst.write("OUTP ON")
    
    def output_off(self):
        self.inst.write("OUTP OFF")
        
    def set_current(self, value):
        self.inst.write("SOUR:CURR {}".format(value))
        
    def set_current_range(self, value):
        self.inst.write("SOUR:CURR:RANG {}".format(value))
    
        
    def closeall(self):
        self.inst.close()
    
