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


'''
Import Libraries
'''
import tempsensor_ctrl as tsc
from tempsensor_ctrl import tempsensorIO as ts_ctrl
import pyvisa as pvisa
import time

'''
Connect to the B2902A
'''
rm = pvisa.ResourceManager()
B2902A = rm.open_resource('USB0::0x0957::0x8C18::MY51140630::0::INSTR')

# Set Modes to be VOLTS
B2902A.write(':SOURce1:VOLTage:MODE %s' % ('FIXed'))
B2902A.write(':SOURce2:VOLTage:MODE %s' % ('FIXed'))

# Set Voltage Levels
VDD = 3.0 # V
VDD1v8 = 1.8 # V
B2902A.write(':SOURce1:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD))
B2902A.write(':SOURce2:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD1v8))

# Set Current Limits
I_VDD_limit = 0.1 # A
I_VDD1v8_limit = 0.01 #A
B2902A.write(':SENSe1:CURRent:DC:PROTection:LEVel %G' % (I_VDD_limit))
B2902A.write(':SENSe2:CURRent:DC:PROTection:LEVel %G' % (I_VDD1v8_limit))

# Initiate the two channels
B2902A.write(':INITiate:IMMediate:ALL (%s)' % ('@1,2'))

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

# Set CTR
sel_ctr_list = [str(i) for i in range(16)]
while True:
    sel_ctr = input("Please set the length of measurement time window: enter n = 0 ~ 15, 16*(2^n) CLK_REF cycles.\n")
    if sel_ctr not in sel_ctr_list:
        print('Please enter a number from 0 ~ 15!\n')
    else:
        break
sel_ctr = int(sel_ctr)
gpio_ts.set_sel_ctr(sel_ctr)

print('')

'''
Design Selection
'''
# Set Design Selections
sel_design_list = [str(i) for i in range(2)]
while True:
    sel_design = input("Please select between different NMOS header designs: enter 0 (gate connected to ground) or 1 (gate connected to source).\n")
    if sel_design not in sel_design_list:
        print('Please enter a number from 0 ~ 1!\n')
    else:
        break
sel_design = int(sel_design)
gpio_ts.set_sel_design(sel_design)

# Set GRP Selections
sel_grp_list = [str(i) for i in range(8)]
while True:
    sel_grp = input("Please select between different supply current: enter 0 ~ 7.\n")
    if sel_grp not in sel_grp_list:
        print('Please enter a number from 0 ~ 7!\n')
    else:
        break    
sel_grp = int(sel_grp)
gpio_ts.set_sel_grp(sel_grp)

# Set INST Selections
sel_inst_list = [str(i) for i in range(4)]
while True:
    sel_inst = input("Please select between different RingOsc inverter-chain length: enter 0 ~ 3.\n")
    if sel_inst not in sel_inst_list:
        print('Please enter a number from 0 ~ 3!\n')
    else:
        break   
sel_inst = int(sel_inst)
gpio_ts.set_sel_inst(sel_inst)

''' For checking if every node works
sel_design = 1
sel_grp = 7
sel_inst = 3
gpio_ts.set_sel_design(sel_design)
gpio_ts.set_sel_grp(sel_grp)
gpio_ts.set_sel_inst(sel_inst)
'''

'''
Reset Release
'''
# Testing Parameters
freq_ref = 32.768 # kHz
meas_step = 0.00 # Sec

# reset chip
gpio_ts.chip_reset(0)
time.sleep(1)

# Initialize averaged Voltage, Current and Power
VDD_avg = 0
Ivdd_avg = 0
Pvdd_avg = 0
VDD1v8_avg = 0
Ivdd1v8_avg = 0
Pvdd1v8_avg = 0
cnt = 0

# Release Chip Reset
release = 'no'
while release != 'yes':
    release = input("Do you want to release chip reset?: enter yes/no.\n")
print('Chip Reset Released!')
print('')
gpio_ts.chip_reset(1)
time.sleep(1)

'''
Wait for DONE and report DOUT
'''
#print('Waiting for test result......')
Ivdd_rec = []
Ivdd1v8_rec = []

# Try to settle measurement first
#for i in range(120):
#    I_values = B2902A.query_ascii_values(':MEASure:CURRent:DC? (%s)' % ('@1,2'))

while True:
    I_values = B2902A.query_ascii_values(':MEASure:CURRent:DC? (%s)' % ('@1,2'))
    #V_values = B2902A.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % ('@1,2'))
    done = gpio_ts.get_done()
    if done:
        print("** DONE DETECTED **")
        dout = gpio_ts.get_dout()
        print("DOUT result is " + str(dout))
        break
    else:
        #if (cnt >= 10):
        #VDD_avg += V_values[0]
        Ivdd_rec.append(I_values[0])
        #Pvdd_avg += V_values[0] * I_values[0]
        #VDD1v8_avg += V_values[1]
        Ivdd1v8_rec.append(I_values[1])
        #Pvdd1v8_avg += V_values[1] * I_values[1]
        #cnt += 1
        time.sleep(meas_step)

#print('Count is ' + str(cnt))

freq = (dout/(16.0*(2**sel_ctr)))*freq_ref/2
print("Frequency result is " + str(freq) + " kHz\n")

# Calculate average powers
#cnt -= 10
win_meas_len = len(Ivdd_rec)
win_stable_len = int(len(Ivdd_rec)/3)
Ivdd_avg = sum(Ivdd_rec[(win_meas_len-win_stable_len):win_meas_len])/win_stable_len
#Pvdd_avg /= cnt
Ivdd1v8_avg = sum(Ivdd1v8_rec[(win_meas_len-win_stable_len):win_meas_len])/win_stable_len
#Pvdd1v8_avg /= cnt
print("VDD1v8 current is " + str(Ivdd1v8_avg*1e6) + " uA\n")

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

B2902A.close()
rm.close()