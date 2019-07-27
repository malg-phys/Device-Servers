# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:53:10 2019

@author: Mak & Shan group
"""

"""
Created on The day before yesterday
@author: Mak & Shan group
"""
import re
import numpy as np
import visa
rm = visa.ResourceManager()

class PSGE8257():    
    def __init__(self, address):  
        self.address = address
        
    def connectInst(self):
        try:
            self.inst=rm.open_resource(self.address)
            self.inst.baud_rate = 9600
            self.inst.write_termination='\r'
            #self.inst.read_termination='\r'
        except:
            print( 'Could not connect PSGE8257')
    
    def disconnectInst(self):
        rm.close()
        
    def formatFreq(self, freq):
        if isinstance(freq, float) or isinstance(freq, int):
            return freq
        units = {'MHz' : 1e6, 'MHZ': 1e6, 'GHZ': 1e9, 'GHz': 1e9, 'KHZ': 1e3, 'kHz':1e3}
        frqNum, frqUnit = freq[:-3], freq[-3:]
        print (frqNum, frqUnit)
        if (frqUnit in units.keys()):
            try:
                frqNum = float(frqNum)
                print(frqNum * units[frqUnit])
                return frqNum * units[frqUnit]
            except:
                return 'invalid'
        else:
            return 'invalid'
            
        
    def id(self):
        ''' 
        Queries the id of the device
        '''
        ans = self.inst.query('*IDN?')
        return ans
        
    def auto_blank(self, auto = None):
        ''' 
        Sets/get the auto blank setting for nower noise frequency sweeps. 1 - ON, 0 - OFF
        '''
        if auto is None:
            ans = self.inst.query(':OUTP:BLAN:AUTO?')
            return ans
        else:
            self.inst.write(':OUTP:BLAN:AUTO {:d}'.format(auto))
            
    def blank(self, state = None):
        '''
        Sets/gets the blanking state. 1 - ON, 0 - OFF
        '''
        if state is None:
            ans = self.inst.query(':OUTP:BLAN:STAT?')
            return ans
        else:
            self.inst.write(':OUTP:BLAN:STAT {:d}'.format(state))
            
    def mod_state(self, state = None):
        '''
        Sets/gets the modulation state for all of AM, FM and PM. 1 - ON, 0 - OFF
        '''
        if state is None:
            ans = self.inst.query(':OUTP:MOD:STAT?')
            return ans
        else:
            self.inst.write(':OUTP:MOD:STAT {:d}'.format(state))
            
    def rf_out(self, state = None):
        '''
        Sets/gets the state of the RF output. 1 - ON, 0 - OFF
        '''
        if state is None:
            ans = self.inst.query(':OUTP:STAT?')
            return ans
        else:
            self.inst.write(':OUTP:STAT {:d}'.format(state))
            
    def trig_source(self, sour = None):
        '''
        Sets/gets the trigger source. Input 'BUS' for GPIB trigger, 'IMM' for immediate trigger, 'EXT' for external trigger, or 'KEY' for hard key trigger
        '''
        sources = ['IMM', 'KEY', 'EXT', 'BUS']
        if sour is None:
            ans = self.inst.query(':TRIG:SEQ:SOUR?')
            return ans
        elif sour in sources:
            self.inst.write(':TRIG:SEQ:SOUR {}'.format(sour))
        else:
            return 'Source must be either BUS, EXT, KEY, or IMM'
            
    def arm_trig(self):
        '''
        Arms the trigger if in KEY, BUS, or EXT trigger mode and arms and triggers the output if in IMM trigger mode
        '''
        self.inst.write(':INIT:IMM:ALL')
        
    def bus_trig(self):
        '''
        Trigger the output when in BUS trigger mode
        '''
        self.inst.write('*TRG')
    
    def imm_trig(self):
        '''
        Causes a trigger event for any trigger mode
        '''
        self.inst.write(':TRIG:SEQ:IMM')
    
    def power_unit(self, unit = None):
        '''
        Sets/gets the units in which the output power is set. Permissible units are 'DBM', 'DBUV', 'DBUVEMF', 'V', 'VEMF', 'DB'
        '''
        units = ['DBM', 'DBUV', 'DBUVEMF', 'V', 'VEMF', 'DB']
        if unit is None:
            ans = self.inst.write(':UNIT:POW?')
            return ans
        elif unit in units:
            self.inst.write(':UNIT:POW {}'.format(unit))
        else:
            return "Unit must be either 'DBM', 'DBUV', 'DBUVEMF', 'V', 'VEMF', 'DB'"
            
    def fix_freq(self, freq = None):
        '''
        Sets/gets the fixed frequency of the RF output. Frequency can be specified as either a floating point without units (interpretted as Hz), or a string consisting of floating point plus 'kHz', 'MHz', or 'GHz'. Frequency cannot exceed 40GHz or be lower than 250kHz
        '''
        if freq is None:
            ans = self.inst.query(':SOUR:FREQ:FIX?')
            return ans
        elif isinstance(freq, int) or isinstance(freq, float):
            self.inst.write(':SOUR:FREQ:FIX {}'.format(freq))
        elif isinstance(freq, str):
            setFrq = self.formatFreq(freq)
            if setFrq != 'invalid' :
                self.inst.write(':SOUR:FREQ:FIX {}'.format(setFrq))
            else:
                return 'Invalid frequency'
                
    def freq(self, freq = None):
        '''
        Sets/gets the frequency of the RF output. Frequency can be specified as either a floating point without units (interpretted as Hz), or a string consisting of floating point plus 'kHz', 'MHz', or 'GHz'. Frequency cannot exceed 40GHz or be lower than 250kHz
        
        Can also increase/decrease the output frequency by a set incrememnt - see freq_inc command - by inputting 'UP' or 'DOWN'
        '''
        options = ['UP', 'DOWN']
        if freq is None:
            ans = self.inst.query(':FREQ?')
            return ans
        elif freq in options:
            self.inst.write(':FREQ {}'.format(freq))
        else:
            setFrq = self.formatFreq(freq)
            if setFrq != 'invalid' :
                self.inst.write(':FREQ {}'.format(setFrq))
            else:
                return 'Invalid frequency'
            
    def freq_inc(self, inc = None):
        '''
        Sets/gets the frequency increment when stepping UP or DOWN in frequency.
        
        Increment frequency can be specified as either a floating point without units (interpretted as Hz), or a string consisting of floating point plus 'kHz', 'MHz', or 'GHz'. Frequency cannot exceed 40GHz or be lower than 250kHz
        '''
        if inc is None:
            ans = self.inst.query(':SOUR:FREQ:CW:STEP:INC?')
            return ans
        else:
            incFrq = self.formatFreq(inc)
            if incFrq != 'invalid':
                self.inst.write(':SOUR:FREQ:CW:STEP:INC {}'.format(incFrq))
            else:
                return 'Invalid increment'
                
    def freq_mode(self, mode = None):
        '''
        Gets/sets the frequency output mode. Can be continuous wave - 'CW', fixed - 'FIX', sweep - 'SWE', or list - 'LIST'
        '''
        modes = ['CW', 'FIX', 'SWE', 'LIST']
        if mode is None:
            ans = self.inst.query(':SOUR:FREQ:MODE?')
            return ans
        elif mode in modes:
            self.inst.write(':SOUR:FREQ:MODE {}'.format(mode))
        else:
            return "Mode must be 'CW', 'FIX', 'SWE', or 'LIST'"
            
    def power_mode(self, mode = None):
        '''
        Sets/gets the power output mode. Can be either fixed - 'FIX', sweep - 'SWE', or list - 'LIST'
        '''
        modes = ['FIX', 'SWE', 'LIST']
        if mode is None:
            ans = self.inst.query(':SOUR:POW:MODE?')
            return ans
        elif mode in modes:
            self.inst.write(':SOUR:POW:MODE {}'.format(mode))
        else:
            return "Power mode must be 'FIX', 'SWE', or 'LIST'"
    
    def power(self, pow = None):
        '''
        Sets/gets the RF power output in dBm. Input a float or integer value without units.
        '''
        if pow is None:
            ans = self.inst.query(':POW?')
            return ans
        elif isinstance(pow, int) or isinstance(pow, float):
            self.inst.write(':POW {}DBM'.format(pow))
        else:
            return 'Power must be a float or integer'
        
            
    def am_state(self, stat = None):
        '''
        Gets/sets the amplitude modulation state. 1 - ON, 0 - OFF
        '''
        if stat is None:
            ans = self.inst.query(':AM:STAT?')
            return ans
        elif (stat == 1) or (stat == 0):
            self.inst.write(':AM:STAT {}'.format(stat))
        else:
            return 'AM state must be 1 or 0'
            
    def am_source(self, sour = None):
        '''
        Gets/sets the source for the amplitude modulation. Options are 'INT', 'INT1', 'INT2', 'EXT', 'EXT1', 'EXT2' for internal/external sources 1 and 2 (default without channel is 1)
        '''
        sources = ['INT', 'INT1', 'INT2', 'EXT', 'EXT1', 'EXT2']
        if sour is None:
            ans = self.inst.query(':AM:SOUR?')
            return ans
        elif sour in sources:
            self.inst.wirte(':AM:SOUR {}'.format(sour))
        else:
            return "Source must be 'INT', 'INT1', 'INT2', 'EXT', 'EXT1', or 'EXT2'"
        
    def am_shape(self, shap = None):
        '''
        Sets/gets the shape of the AM. Options are 'SINE', 'TRI', 'SQU', 'RAMP', 'NOIS', 'DUAL', 'SWEP'
        '''
        shapes = ['SINE', 'TRI', 'SQU', 'RAMP', 'NOIS', 'DUAL', 'SWEP']
        if shap is None:
            ans = self.inst.query(':AM:INT:FUNC:SHAP?')
            return ans
        elif shap in shapes:
            self.inst.write(':AM:INT:FUNC:SHAP {}'.format(shap))
        else:
            return "Shape must be 'SINE', 'TRI', 'SQU', 'RAMP', 'NOIS', 'DUAL', or 'SWEP'"
            
            
    def am_pct(self, pct = None):
        '''
        Sets/gets the modulation amplitude in percent/voltage
        units. Input is a float or integer in percent
        '''
        if pct is None:
            ans = self.inst.query(':AM?')
            return ans
        elif isinstance(pct, float) or isinstance(pct, int):
            self.inst.write(':AM {}PCT'.format(pct))   
        else:
            return 'Modulation must a float or integer'

    def am_freq(self, freq = None):
        '''
        Sets/gets the amplitude modulation frequency. Accepts
        a float or integer assuming Hz, or add units of kHz, 
        MHz, or GHz
        '''
        if freq is None:
            ans = self.inst.query(':AM:INT:FREQ?')
            return ans
        else:                                                            
            frmFrq = self.formatFreq(freq)
            if frmFrq != 'invalid':
                self.inst.write(':AM:INT:FREQ {}'.format(frmFrq))
            else:
                return 'Invalid frequency'

    def zero_alt_am(self):
        '''
        Zeros any contribution from the dual amplitude modulation
        tone
        '''
        self.inst.write(':AM:INT:FREQ:ALT:AMPL:PERC 0')
        
    def alt_am_pct(self, pct = None):
        '''
        Sets/gets the dual amplitude modulation
        percent modulation
        '''
        if pct is None:
            ans = self.inst.query(':AM:INT:FREQ:ALT:AMPL:PERC?')
            return ans
        elif isinstance(pct, float) or isinstance(pct, int):
           self.inst.write(':AM:INT:FREQ:ALT:AMPL:PERC {}'.format(pct))
        else:
            return 'Percent of alt AM must be float or int'

    def fm_state(self, stat = None):
        '''
        Sets/gets the state of the frequency modulation
        0 - OFF, 1 - ON
        '''
        states = [0, 1, 'ON', 'OFF']
        if stat is None:
            ans = self.inst.query(':FM:STAT?')
            return ans
        elif stat in states:
            self.inst.write(':FM:STAT {}'.format(stat))
        else:
            return 'FM state must me 0/1 or ON/OFF'
        
    def pm_state(self, stat = None):
        '''
        Sets/gets the state of the phase modulation
        0 - OFF, 1 - ON
        '''
        states = [0, 1, 'ON', 'OFF']
        if stat is None:
            ans = self.inst.query('PM:STAT?')
            return ans
        elif stat in states:
            self.inst.write(':PM:STAT {}'.format(stat))
        else:
            return 'PM state must me 0/1 or ON/OFF'