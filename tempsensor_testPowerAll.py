# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Sky130TempSensor Chip Testing Powers of all 64 designs on a chip given one temperature and supply voltages
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
import pyvisa as pvisa

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
I_VDD1v8_limit = 0.0001 # 100uA
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

print('')

'''
Test Power for all nodes under a given temperature
'''
ChipNo = 10
temp = 20 # degree C
freq_ref = 32.768 # kHz
ctr = 13 # 8s conversion time
meas_step = 0.00 # s
pmeas = 0.3 # only use tail-30% samples

dict_meas = gpio_ts.test_all_powers(ctr, meas_step, pmeas, temp, freq_ref, B2902A)
df_meas = pd.DataFrame(dict_meas) 

# Save to csv
meas_res_path = './MeasResults/Power/'
res_csv_name = meas_res_path + 'Meas_ChipNo' + str(ChipNo) + '_Vdio' + str(VDD) + 'Vdd' + str(VDD1v8) + '_' + str(temp) + 'C.csv'
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

'''
Close SMU Connection
'''
B2902A.close()
rm.close()