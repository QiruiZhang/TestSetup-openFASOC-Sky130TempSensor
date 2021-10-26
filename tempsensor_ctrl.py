# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Multiple classes for controlling Sky130TempSensor I/Os through FT232H
"""

from pyftdi.gpio import GpioMpsseController

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

'''
Some useful functions
'''


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is