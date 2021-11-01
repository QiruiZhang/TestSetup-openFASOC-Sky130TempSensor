# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Multiple classes for controlling Sky130TempSensor I/Os through FT232H
"""

from pyftdi.gpio import GpioMpsseController
import time

# GPIO Board USB addresses
gpio_in_addr = "ftdi://ftdi:232h:00:fd/1" # {SEL_INST[1:0], SEL_GRP[2:0], SEL_DESIGN, SEL_CTR[3:0], RESET_REGn} = {C7:C0, D7:D5}
gpio_out1_addr = "ftdi://ftdi:232h:00:fe/1" # {C7:C0, D7:D4} = DOUT[23:12] 
gpio_out0_addr = "ftdi://ftdi:232h:00:ff/1" # {C7:C0, D7:D3} = {DOUT[11:0], DONE}

class tempsensorIO():
    def __init__(self, input_addr_url, out1_addr_url, out0_addr_url, freq):
        self.input_url = input_addr_url
        self.out1_url = out1_addr_url
        self.out0_url = out0_addr_url
        self.freq = freq
        self.direction_in = 0xffff
        self.direction_out1 = 0x0000
        self.direction_out0 = 0x0000

        '''
        Input Board Pinout:
            C7-C6:  SEL_INST[1:0]. Default 0b00. 
            C5-C3:  SEL_GRP[2:0]. Default 0b000. 
            C2:     SEL_DESIGN. Default 0b0. 
            C1-C0, 
            D7-D6:  SEL_CTR[3:0]. Default 0b0000. 
            D5:     RESET_REGn. Default 0b0. 
        '''
        self.gpio_in = GpioMpsseController()
        self.gpio_in.configure(self.input_url, direction=self.direction_in, frequency=self.freq)
        self.gpio_in.write(0x0000)
        
        '''
        Output Board1 Pinout:
            C7-C0,
            D7-D4:  DOUT[23:12]
        
        Output Board0 Pinout:
            C7-C0,
            D7-D4:  DOUT[11:0]
            D3:     DONE
        '''
        self.gpio_out1 = GpioMpsseController()
        self.gpio_out1.configure(self.out1_url, direction=self.direction_out1, frequency=self.freq)
        
        self.gpio_out0 = GpioMpsseController()
        self.gpio_out0.configure(self.out0_url, direction=self.direction_out0, frequency=self.freq)

    def reset(self):
        self.gpio_in.write(0x0000)

    def close(self):
        self.gpio_in.close()
        self.gpio_out1.close()
        self.gpio_out0.close()

    def update_freq(self, freq):
        self.freq = freq
        self.gpio_in.set_frequency(self.freq)
        self.gpio_out1.set_frequency(self.freq)
        self.gpio_out0.set_frequency(self.freq)

    def get_state(self):
        return [f'{self.gpio_in.read()[0]:016b}', f'{self.gpio_out1.read()[0]:016b}', f'{self.gpio_out0.read()[0]:016b}']

    # active low
    def chip_reset(self, rst_val):
        cur_state = self.gpio_in.read()[0]
        cur_state &= ~(0b1 << 5)
        self.gpio_in.write(cur_state | rst_val << 5)

    def set_sel_ctr(self, sel_ctr_val):
        cur_state = self.gpio_in.read()[0]
        cur_state &= ~(0b1111 << 6)
        self.gpio_in.write(cur_state | sel_ctr_val << 6)

    def set_sel_design(self, sel_design_val):
        cur_state = self.gpio_in.read()[0]
        cur_state &= ~(0b1 << 10)
        self.gpio_in.write(cur_state | sel_design_val << 10)

    def set_sel_grp(self, sel_grp_val):
        cur_state = self.gpio_in.read()[0]
        cur_state &= ~(0b111 << 11)
        self.gpio_in.write(cur_state | sel_grp_val << 11)

    def set_sel_inst(self, sel_inst_val):
        cur_state = self.gpio_in.read()[0]
        cur_state &= ~(0b11 << 14)
        self.gpio_in.write(cur_state | sel_inst_val << 14)

    def get_done(self):
        return (self.gpio_out0.read()[0] >> 3) & 0b1

    def get_dout(self):
        return ((self.gpio_out1.read()[0] >> 4) << 12) + (self.gpio_out0.read()[0] >> 4)

    # Test RO frequency of all 64 designs on a chip
    def test_all_freqs(self, ctr_design0, ctr_design1, repeat0, repeat1, temp, freq_ref):
        # initialize columns in the measurement results table
        list_temp = []
        list_design = []
        list_grp = []
        list_inst = []
        list_ctr = []
        list_ref = []
        list_dout = []
        list_freq = []
        
        # Start looping all the 64 designs in a chip under a given temperature
        for sel_design in range(2):
            # select input ctr configurations according to design type
            if sel_design == 0:
                sel_ctr = ctr_design0
                repeat = repeat0
            else:
                sel_ctr = ctr_design1
                repeat = repeat1
            
            for sel_grp in range(8):
                for sel_inst in range(4):
                    print("Testing temperature sensor node " + str(sel_design) + '.' + str(sel_grp) + '.' + str(sel_inst))
                    # Set CTR
                    self.set_sel_ctr(sel_ctr)
    
                    # Select design
                    self.set_sel_design(sel_design)
                    self.set_sel_grp(sel_grp)
                    self.set_sel_inst(sel_inst)
                    
                    freq_avg = 0
                    for i in range(repeat):
                        # reset chip
                        self.chip_reset(0)
                        time.sleep(1)
                        
                        # release reset
                        self.chip_reset(1)
                        
                        # Wait for done and read dout
                        while True:
                            done = self.get_done()
                            if done:
                                print("** DONE DETECTED **")
                                dout = self.get_dout()
                                print("DOUT result is " + str(dout))
                                break
                    
                        freq = (dout/(16.0*(2**sel_ctr)))*freq_ref/2
                        freq_avg += freq
                    
                    freq_avg /= repeat
                    print("Frequency result is " + str(freq_avg) + " kHz\n")
                        
                    list_temp.append(temp)
                    list_design.append(sel_design)
                    list_grp.append(sel_grp)
                    list_inst.append(sel_inst)
                    list_ctr.append(sel_ctr)
                    list_ref.append(freq_ref)
                    list_dout.append(dout)
                    list_freq.append(freq_avg) # kHz
                            
        dict_meas = {
            'temp':             list_temp, 
            'design':           list_design, 
            'group':            list_grp,
            'inst':             list_inst,
            'CTR':              list_ctr,
            'FreqRef (kHz)':    list_ref,
            'DOUT':             list_dout,
            'Freq (kHz)':       list_freq
        }  
       
        return dict_meas

    # Test chip current of all 64 designs on a chip
    def test_all_powers(self, ctr_design0, ctr_design1, meas_step, pmeas, temp, freq_ref, SMU):
        # initialize columns in the measurement results table        
        list_Ivdd = []
        list_Ivdd1v8 = []
        
        # Start looping all the 64 designs in a chip under a given temperature
        for sel_design in range(2):
            # select input ctr configurations according to design type
            if sel_design == 0:
                sel_ctr = ctr_design0
            else:
                sel_ctr = ctr_design1
            
            for sel_grp in range(8):
                for sel_inst in range(4):
                    print("Testing temperature sensor node " + str(sel_design) + '.' + str(sel_grp) + '.' + str(sel_inst))
                    # Set CTR
                    self.set_sel_ctr(sel_ctr)
    
                    # Select design
                    self.set_sel_design(sel_design)
                    self.set_sel_grp(sel_grp)
                    self.set_sel_inst(sel_inst)
                    
                    # reset chip
                    self.chip_reset(0)
                    time.sleep(1)
                    
                    # Initialize averaged Voltage, Current and Power
                    Ivdd_rec = []
                    Ivdd_avg = 0
                    Ivdd1v8_rec = []
                    Ivdd1v8_avg = 0
                    
                    # release reset
                    self.chip_reset(1)
                    time.sleep(1)

                    # Wait for done and measure power
                    while True:
                        I_values = SMU.query_ascii_values(':MEASure:CURRent:DC? (%s)' % ('@1,2'))
                        done = self.get_done()
                        if done:
                            print("** DONE DETECTED **")
                            break
                        else:
                            Ivdd_rec.append(I_values[0])
                            Ivdd1v8_rec.append(I_values[1])
                            time.sleep(meas_step)
                    
                    # Calculate average powers
                    win_meas_len = len(Ivdd_rec)
                    win_stable_len = int(len(Ivdd_rec)*pmeas)
                    Ivdd_avg = sum(Ivdd_rec[(win_meas_len-win_stable_len):win_meas_len])/win_stable_len
                    Ivdd1v8_avg = sum(Ivdd1v8_rec[(win_meas_len-win_stable_len):win_meas_len])/win_stable_len
                    print("VDD1v8 current is " + str(Ivdd1v8_avg*1e6) + " uA\n")

                    list_Ivdd.append(Ivdd_avg)
                    list_Ivdd1v8.append(Ivdd1v8_avg)

        dict_meas = {
            'Ivdd (A)':     list_Ivdd, 
            'Ivdd1v8 (A)':  list_Ivdd1v8
        }  
       
        return dict_meas

'''
Some useful functions
'''

def convert_temp_read(temp):
    temp_bin = f'{temp:016b}'
    if temp_bin[0] == '1': # T < 0C
        temp = - (2**16 - temp)/10.0
    else:
        temp = temp/10.0
    return temp

def convert_temp_write(temp):
    if temp < 0: # T < 0C
        temp_set = 2**16 + temp * 10
    else:
        temp_set = temp * 10
    return temp_set

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is