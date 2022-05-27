# -*- coding: utf-8 -*-
"""
Created on Tue May 24 2022

@author: Qirui Zhang

Sky130TempSensor chip testing: RO frequency for one instance under one given temperature
"""

'''
Check if FT232H devices are connected. Should list 3 devices.
'''
from pyftdi.usbtools import UsbTools
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
for i in FT232H_list:
    print(i)
print('')

'''
Import Libraries
'''
import tempsensor_ctrl as tsc
from tempsensor_ctrl import tempsensorIO as ts_ctrl
import time

'''
Initialize GPIO bridge boards
'''
print('Initializing GPIO Boards......')
freq = 1e6
gpio_ts = ts_ctrl(tsc.gpio_in_addr, tsc.gpio_out1_addr, tsc.gpio_out0_addr, freq)
gpio_ts.get_state()
print('')

'''
Chip Bring-Up Sequence
'''
print('Start chip bringing-up!')
# Open VDD
opened = 'no'
while opened != 'yes':
    opened = input("Please set VDD (Typ. 3.0V): enter yes/no to finish.\n")

# Open VDD1v8
opened = 'no'
while opened != 'yes':
    opened = input("Please set VDD1v8 (Typ. 1.8V): enter yes/no to finish.\n")

# Turn on CLK ref
opened = 'no'
while opened != 'yes':
    opened = input("Please turn on reference clock (Typ. 32.768kHz): enter yes/no to finish.\n")

print('')

'''
Test Frequency for one selected instance under given temp and supply 
'''
# Specify Chip No.
ChipNo = 18 # QP Tech. Ones starts from 10

# Select Design
sel_ctr = 0
sel_design = 1
sel_grp = 4
sel_inst = 3

# Specify other parameters
freq_ref = 32.768 # kHz 
temp = 20 # degree C
Supply = 1.8
repeat = 16

# Set Input Control
gpio_ts.set_sel_ctr(sel_ctr)
gpio_ts.set_sel_design(sel_design)
gpio_ts.set_sel_grp(sel_grp)
gpio_ts.set_sel_inst(sel_inst)

# Begin Testing
time.sleep(2)
dout_avg = 0
for i in range(repeat):
    # reset chip
    gpio_ts.chip_reset(0)
    time.sleep(0.5)
    
    # release reset
    gpio_ts.chip_reset(1)
    
    # Wait for done and read dout
    while True:
        done = gpio_ts.get_done()
        if done:
            print("** DONE DETECTED **")
            dout = gpio_ts.get_dout()
            print("DOUT result is " + str(dout))
            break
    
    dout_avg += dout

dout_avg /= repeat
freq = (dout_avg/(32.0*(2**sel_ctr)))*freq_ref
print("Frequency result is " + str(freq) + " kHz\n")


'''
Test Finished. Reset Chip and Close GPIO Ports
'''
finish = 'no'
while finish != 'yes':
    finish = input("Do you want to end the test?: enter yes/no.\n")
print('End of Test!')
print('')

gpio_ts.reset()
gpio_ts.close()