# openFASOC Temperature Sensors in SkyWater 130nm: Test Setup

This repository provides a fully open-source test setup solution for a temperature sensor chip taped-out in SkyWater 130nm with 64 openFASOC-generated temperature sensor instances. The setup is highly automated with Python and open-source libraries, where the chip is controled through low-cost commercially-available USB devices, and control of testing equipments like temperature chambers and source meters is also seamlessly embedded in the test flow using Python. 

**Author:** [Qirui Zhang](https://www.linkedin.com/in/cary-qirui-zhang/) from the [University of Michigan, Ann Arbor](https://micl.engin.umich.edu/)

## 1. Prerequisites
### 1.1 **Host Computer**
A host computer with Windows 10 operating system is required. Either a desktop or laptop should work.

### 1.2 **Python**
Please install the latest version of [Anaconda](https://www.anaconda.com/products/individual) (Python3) and use Spyder for running the test scripts.

## 2. Test Setup
### 2.1 **Daughter Board for the Chip**
The daughter board could be as simple as one that directly connects all the chip I/Os to headers and power supplies to SMA or banana connectors. No level conversion should be needed as the chip uses 3.3V I/O voltage. It is suggested to use 64-pin ceramic PGA packages for packaging the dice and a Zero-Insertion-Force (ZIF) socket for holding the chip. The daughter board designed for validating this setup is shown below as a reference:

<img src="PCBtop.png" width="600">
Fig. 1. Top view of the daughter board
<br /> <br /> <br />
<img src="PCBbot.png" width="600">
Fig. 2. Bottom view of the daughter board

### 2.2 **FT232H USB-GPIO Bridge**
Three FT232H USB-GPIO bridge boards from AdaFruit are needed in this setup for controlling the chip. Please purchase them online from Adafruit. After getting the boards, follow this [page](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows) to install driver for the boards using Zadig. Note: you only need to follow the "Plug in FT232H & Fix Driver with Zadig" part on this page, as we do not use the boards in the same way as they suggest.

After the driver is installed, open an Anaconda prompt, install pyftdi and pyusb libraries:
```
    pip install pyftdi
    pip install pyusb
```

### 2.3 **Temperature Chamber**
Please make sure you use a TestEquity temperature chamber with the [F4 controller](https://www.testequity.com/RS-232-F4-resources) from Watlow Electric. Any other temperature chambers are not guaranteed to work with this setup. 

### 2.4 **Source and Measurement Unit**

### 2.5 **Other Equipments**

## 3. Running the Scripts for Automated Testing

## 4. Acknowledgements
The author would like to thank Google and SkyWater for fabrication of the test chip.

## 5. License
The source code is released under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

For any technical issues, please contact Qirui Zhang <qiruizhATumich.com>.
