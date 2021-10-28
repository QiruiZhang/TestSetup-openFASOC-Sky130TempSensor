# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Sky130TempSensor Chip Testing Sanity Check for a single node
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
import pandas as pd
import time

'''
Functions
'''

def test_all_freqs(chip, ctr_design0, ctr_design1, temp, freq_ref):
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
        else:
            sel_ctr = ctr_design1
            
        for sel_grp in range(8):
            for sel_inst in range(4):
                print("Testing temperature sensor node " + str(sel_design) + '.' + str(sel_grp) + '.' + str(sel_inst))
                # Set CTR
                chip.set_sel_ctr(sel_ctr)
    
                # Select design
                chip.set_sel_design(sel_design)
                chip.set_sel_grp(sel_grp)
                chip.set_sel_inst(sel_inst)
    
                # reset chip
                chip.chip_reset(0)
                time.sleep(0.5)
                
                # release reset
                chip.chip_reset(1)
        
                # Wait for done and read dout
                while True:
                    done = chip.get_done()
                    if done:
                        print("** DONE DETECTED **")
                        dout = chip.get_dout()
                        print("DOUT result is " + str(dout))
                        break
                
                list_temp.append(temp)
                list_design.append(sel_design)
                list_grp.append(sel_grp)
                list_inst.append(sel_inst)
                list_ctr.append(sel_ctr)
                list_ref.append(freq_ref)
                list_dout.append(dout)
                freq = (dout/(16.0*(2**sel_ctr)))*freq_ref/2
                print("Frequency result is " + str(freq) + " kHz\n")
                list_freq.append(freq) # kHz
    
    dict_meas = {'temp':     list_temp, 
            'design':   list_design, 
            'group':    list_grp,
            'inst':     list_inst,
            'CTR':      list_ctr,
            'FreqRef':  list_ref,
            'DOUT':     list_dout,
            'Freq':     list_freq}  
       
    df = pd.DataFrame(dict_meas) 
    return df

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
Test Frequency for all nodes under a given temperature
'''
ChipNo = 2
temp = -20 # degree C
freq_ref = 32.768 # kHz
ctr_design0 = 14 # 16 * (2^ctr_design0) CLK_REF cycles
ctr_design1 = 7  # 16 * (2^ctr_design1) CLK_REF cycles

df_meas = test_all_freqs(gpio_ts, ctr_design0, ctr_design1, temp, freq_ref)

# Save to csv
meas_res_path = 'C:/Files/Research/FASoC/TempSensorTesting/MeasResults/'
res_csv_name = meas_res_path + 'Freqs_ChipNo' + str(ChipNo) + '_' + str(temp) + 'C.csv'
df_meas.to_csv(res_csv_name)

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