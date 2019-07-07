# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:04:59 2019

@author: lenovo
"""
import visa
rm=visa.ResourceManager()

class Agilent_E5061A():
    
    def __init__(self, address):
        self.E5061A = rm.open_resource(address)

    def set_freq_star(self, frequency):
        self.E5061A.write(':SENS1:FREQ:STAR {}'.format(frequency))
        
    def set_freq_stop(self, frequency):
        self.E5061A.write(':SENS1:FREQ:STOP {}'.format(frequency))
        
    def set_freq_cent(self, frequency):
        self.E5061A.write(':SENS1:FREQ:CENT {}'.format(frequency))
    
    def set_power(self, power):
        self.E5061A.write(':SOUR1:POW {}'.format(power))
    
    def set_powerrange(self, prange):
        if prange == 0 or prange == 10 or prange == 20 or prange == 30 or prange == 40:
            self.E5061A.write(':SOUR1:POW:ATT {}'.format(prange))
        else:
            print('Enter 0, 10, 20, 30 or 40')
    
    def get_power(self):
        self.a = self.E5061A.query(':CALC1:MARK1:Y?')
        self.a = self.a.split(',')[0]
        return float(self.a)
    
    