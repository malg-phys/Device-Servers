# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:28:23 2018

@author: Mak & Shan group
"""

import numpy as np
import visa
rm=visa.ResourceManager()

class ITC503():
    
    def __init__(self):
        
        self.inst=rm.open_resource('GPIB0::24::INSTR')
        self.inst.write_termination='\r'
        self.inst.read_termination='\r'

    def R0(self):
        while True:
            self.r1=self.inst.query('R1')
            self.r2=list(self.r1)
            if (self.r2)[0]=='R':
                break
        self.r1=self.r1.strip('R')
        return float(self.r1)
    def R1(self):
        while True:
            self.r1=self.inst.query('R1')
            self.r2=list(self.r1)
            if (self.r2)[0]=='R':
                break
        self.r1=self.r1.strip('R')
        return float(self.r1)

    def R2(self):
        while True:
            self.r1=self.inst.query('R2')
            self.r2=list(self.r1)
            if (self.r2)[0]=='R':
                break
        self.r1=self.r1.strip('R')
        return float(self.r1)
    
    def R3(self):
        self.r3=self.inst.query('R3')
        self.r3=self.r1.strip('R')
        return self.r3   

    def R4(self):
        self.r1=self.inst.query('R4')
        self.r1=self.r1.strip('R')
        return self.r1

    def R5(self):
        self.r2=self.inst.query('R5')
        self.r2=self.r2.strip('R')
        return self.r2

    def R6(self):
        self.r3=self.inst.query('R6')
        self.r3=self.r3.strip('R')
        return self.r3
    
    def R7(self):
        self.r3=self.inst.query('R7')
        self.r3=self.r3.strip('R')
        return self.r3
#setting the ITC503
        
    def set_temp(self,setp):
#        self.inst.write('A1')
#        print(self.inst.read())
        self.inst.write('T'+str(setp))
        print(self.inst.read())
    
    def set_ned(self,setp):
#        self.inst.write('A3')
#        print(self.inst.read())
        self.inst.write('G'+str(setp))
        print(self.inst.read())

    def FN(self,n):
        self.inst.write('F'+str(n))
        
    
    
    
    
    
    
#itc=ITC503()
#
#for i in range(100000):
#    
##itc.set_ned(10.0)
#print(itc.inst.write('G15'))
##print(itc.inst.query('V'))
##itc.inst.write('C3')
###itc.inst.write('O0.1')
#print(itc.R2())
##print(itc.R4())
#itc.set_temp(70.00)
#print(itc.R7())