# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:28:23 2018

@author: Mak & Shan group
"""
import re
import numpy as np
import visa
rm = visa.ResourceManager()

class ITC503():    
    def __init__(self, address):  
        self.address = address
        
    def connectInst(self):
        try:
            self.inst=rm.open_resource(self.address)
            self.inst.baud_rate = 9600
            self.inst.write_termination='\r'
            self.inst.read_termination='\r'
        except:
            print 'Could not connect ITC503'
    
    def disconnectInst(self):
        rm.close()
        
    def remote(self, unlocked = True):
        '''
        Sets the device to remote mode, either locked or unlocked (default unlocked)
        '''
        if unlocked:
            self.inst.query('C3')
        else:
            self.inst.query('C1')
    
    def local(self, unlocked = True):
        '''
        Sets the device to local mode, either locked or unlocked (default unlocked)
        '''
        if unlocked:
            self.inst.query('C2')
        else:
            self.inst.query('C0')
            
    def com_protocol(self, prot):
        '''
        Sets the communication protocol. Takes either 'NORM' to specify normal communication, or 'LF' to return <LF> after each <CR>
        '''
        if prot == 'NORM':
            self.inst.query('Q0')
        elif prot == 'LF':
            self.inst.query('Q2')
        else:
            print "Protocol must be either 'NORM' or 'LF'"
            
    def get_temp(self, sensor):
        '''
        Read the temperature on the specified sensor (1, 2, or 3)
        '''
        if int(sensor) in [1, 2, 3]:
            ans = self.inst.query('R{:d}'.format(sensor))
            return float(ans.strip('R').strip('+'))
        else:
            print 'Seonsor must be either 1, 2, or 3'
            
    def get_set_temp(self):
        '''
        Returns the temperature setpoint
        '''
        ans = self.inst.query('R0')
        return float(ans.strip('R').strip('+'))
            
    def set_heat_gas(self, heat, gas):
        '''
        Set the heater and gas to manual or auto. Accepts the setting for (heater, gas) has either AUTO or MAN: eg. query set_heat_gas('AUTO', 'MAN') to set the heat to auto and gas to manual mode
        '''
        setting = {'AUTO' : 1, 'MAN' : 0}
        if (heat in setting.keys()) and (gas in setting.keys()):
            num = setting[heat] * 2 + setting[gas]
            self.inst.query('A{:d}'.format(num))
        else:
            print 'Heat and gas must be set to AUTO or MAN'
        
    def set_temp(self,setp):
        '''
        Sets the tempature to the specified setpoint
        '''
        self.inst.query('T{:f}'.format(setp))
        
    def get_needle(self):
        '''
        Gets the gas flow in percent
        '''
        ans = self.inst.query('R7')
        return float(ans.strip('R'))
        
    
    def set_needle(self,setp):
        '''
        Sets the needle valve to the specified setpoint
        '''
        self.inst.query('G{:f}'.format(setp))
