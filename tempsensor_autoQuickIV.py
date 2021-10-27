# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 21:54:53 2021

@author: 95864
"""
import time
import mouse

# Move mouse to measure
mouse.move('200', '100')
time.sleep(0.5)

# Start measurement
mouse.click()
time.sleep(10)

# Move mouse to data table
mouse.move('200', '300')
time.sleep(0.5)

# Right click on data table
mouse.right_click()
time.sleep(0.5)

# Click on 'Export csv'
mouse.move('250', '370')
time.sleep(0.5)
mouse.click()
time.sleep(0.5)

# Select 'test.csv' to fill in file name
mouse.move('200', '140')
time.sleep(0.5)
mouse.click()
time.sleep(0.5)

'C:\Files\Research\FASoC\TempSensorTesting\MeasResults\testMouse.csv'

# Click 'save'
mouse.move('450', '450')
time.sleep(0.5)
mouse.click()
time.sleep(0.5)

# Click 'yes' to overwrite
mouse.move('700', '420')
time.sleep(0.5)
mouse.click()
time.sleep(0.5)
