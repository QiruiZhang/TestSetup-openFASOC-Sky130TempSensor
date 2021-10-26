Keysight IVI Driver Programming Examples
---------------------------------------

Examples installed with the driver demonstrate basic use 
of the driver in a variety of application development environments and 
programming languages.  All the Example programs do the following:

1. Create an instance of the driver.
2. Initialize the driver in simulation mode (no instrument required).
3. Read several IVI Identity properties.
4. Check the instrument error queue.
5. Close the driver.

Notes:
-----
Examples may perform additional instrument driver specific tasks.

Examples are coded to initialize the driver in simulation mode and should 
compile and run as is, without an instrument.

Example Visual Studio projects were created with VS2010.  They may be updated 
to newer versions or, if you are using an older version of Visual Studio, 
you may cut and paste code from the example project source into a similar 
project created in your older version of Visual Studio.

C# and VB.NET examples compiled in AnyCPU configuration on 64-bit machines will 
use the 64-bit version of the driver.  Only x86 or AnyCPU configurations are 
supported.  Compiling in x64 configuration is not supported. 

Keysight VEE Pro example requires VEE 9.0 or newer.
LabVIEW example requires LV 2010 or newer.
MATLAB examples require MATLAB R2015b (32-bit). R2015b was the last MATLAB release with Windows 
32 support.

You may use these examples as a starting point for creating programs for
this instrument driver. For additional info on using IVI drivers in a variety 
of development environments, see the driver Help file topics:

  Programming with the IVI-COM Driver in Various Development Environments 
	Using C#
	Using Visual Basic.NET
	Using Visual C++
	Using LabVIEW
	Using LabWindows CVI
	Using MATLAB

  Programming with the IVI-C Driver in Various Development Environments 
	Using LabVIEW
	Using Visual C++
	Using .NET
