# openFASOC Temperature Sensor Chip in SkyWater 130nm: Test Setup

This repository provides a fully open-source test setup solution for a temperature sensor chip taped-out in SkyWater 130nm with 64 openFASOC-generated temperature sensor instances. The setup is highly automated with Python and open-source libraries, where the chip is controled through low-cost commercially-available USB devices, and control of testing equipments like temperature chambers and source meters is also seamlessly embedded in the test flow using Python. 

**Author:** [Qirui Zhang](https://www.linkedin.com/in/cary-qirui-zhang/) from the [University of Michigan, Ann Arbor](https://micl.engin.umich.edu/)

## 1. Prerequisites
### 1.1 **Host Computer**
A host computer with Windows 10 operating system is required. Either desktop or laptop should work.

### 1.2 **Python**
Please install the latest version of [Anaconda](https://www.anaconda.com/products/individual) (Python3) and use Spyder for running the test scripts.

### 1.3 **Daughter Board for the Chip**
The daughter board could be as simple as one that directly connects all the chip I/Os to headers and power supplies to SMA or banana connectors. No level conversion should be needed as the chip uses 3.3V I/O voltage. It is suggested to use 64-pin ceramic PGA packages for packaging the dice and a Zero-Insertion-Force (ZIF) socket for holding the chip. The daughter board designed for validating this setup is shown below as a reference:

![Top view of daughter board](PCBtop.png)


### 1.4 **FT232H USB-GPIO Bridge**
Three FT232H USB-GPIO bridge boards from AdaFruit are needed in this setup for controlling the chip. Please purchase them online from Adafruit. After getting the boards, follow this [page](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows) to install driver for the boards using Zadig. Note: you only need to follow the "Plug in FT232H & Fix Driver with Zadig" part on this page, as we do not use the boards in the same way as they suggest.

After the driver is installed, open an Anaconda prompt, install pyftdi and pyusb libraries:
```
    pip install pyftdi
    pip install pyusb
```



## 2. Build Explicit VINS-Fusion
Clone the repository and catkin_make:
```
    mkdir /home/username/VINS_Fusion
    mkdir /home/username/VINS_Fusion/src
    mkdir /home/username/VINS_Fusion/result
    cd /home/username/VINS_Fusion/src
    git clone https://github.com/QiruiZhang/Explicit-VINS-Fusion.git
    cd ../
    catkin_make
    source /home/username/VINS_Fusion/devel/setup.bash
```
(if you fail in this step, try to find another computer with clean system or reinstall Ubuntu and ROS)

## 3. EuRoC Example
Download [EuRoC MAV Dataset](http://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets) and extract the '.bag' files to YOUR_DATASET_FOLDER. Take MH_01 for example, you can run Explicit VINS-Fusion with two sensor types (monocular camera + IMU and stereo cameras + IMU). 
Open three terminals, launch rviz, run vins node and play the bag file respectively. Green path in the rviz GUI is the VIO odometry.

### 3.1 Monocualr camera + IMU

```
    In terminal 1:
    source ~/VINS_Fusion/devel/setup.bash (only need to do this after openning a new terminal)
    roslaunch vins vins_rviz.launch
    
    In terminal 2: 
    source ~/VINS_Fusion/devel/setup.bash (only need to do this after openning a new terminal)
    rosrun vins vins_node ~/VINS_Fusion/src/Explicit-VINS-Fusion/config/euroc/euroc_mono_imu_config_Allwork.yaml MH_01 /home/username/VINS_Fusion/result
    
    In terminal 3:
    rosbag play YOUR_DATASET_FOLDER/MH_01_easy.bag
```

The output 6-DoF pose trajectory file will be ~/VINS_Fusion/result/MH01_mono.csv.

### 3.2 Stereo cameras + IMU

```
    In terminal 1:
    source ~/VINS_Fusion/devel/setup.bash (only need to do this after openning a new terminal)
    roslaunch vins vins_rviz.launch
    
    In terminal 2: 
    source ~/VINS_Fusion/devel/setup.bash (only need to do this after openning a new terminal)
    rosrun vins vins_node ~/VINS_Fusion/src/Explicit-VINS-Fusion/config/euroc/euroc_stereo_imu_config_Allwork.yaml MH_01 /home/username/VINS_Fusion/result
    
    In terminal 3:
    rosbag play YOUR_DATASET_FOLDER/MH_01_easy.bag
```

The output 6-DoF pose trajectory file will be ~/VINS_Fusion/result/MH01_stereo.csv.

## 4. Acknowledgements
The author would like to thank of the original authors of VINS-Fusion from HKUST.

## 5. License
The source code is released under [GPLv3](http://www.gnu.org/licenses/) license.

For any technical issues, please contact Qirui Zhang <qiruizhATumich.com>.
