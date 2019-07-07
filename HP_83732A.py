# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:57:33 2019

@author: lenovo
"""

import visa
rm=visa.ResourceManager()

class HP_83732A():
    
    def __init__(self, address):
        self.HP = rm.open_resource(address)

    def set_frequency(self, frequency):
        self.HP.write('SOUR:FREQ {}'.format(frequency))
    
    def set_power(self, power):
        self.HP.write('SOUR:POW {}'.format(power))
    
    