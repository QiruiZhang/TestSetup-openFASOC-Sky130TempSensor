			***********************
			**** Read Me First ****
			***********************

Version: 2.2.2.0		Oct 2020

Introducing the AgB29xx IVI Driver for the Keysight B29xx family of instruments
---------------------------------------------------------------------------
  This instrument driver provides access to the functionality of the 
   B2901A, B2902A, B2911A, B2912A, B2961A  and B2962A through a COM server or ANSI C API which also complies
  with the IVI specifications. This driver works in any development environment
  which supports COM or C programming including Microsoft Visual C++, Microsoft
  .NET, Keysight VEE Pro, National Instruments LabView, LabWindows CVI, MATLAB(32
  bit only) and others.


Supported Instruments
---------------------
B2901A
B2902A
B2911A
B2912A
B2961A
B2962A
B2901B
B2901BL 
B2902B
B2910BL
B2911B
B2912B
B2961B
B2962B
 
 
Installation
-------------
  System Requirements: The driver installation will check for the following 
  requirements.  If not found, the installer will either abort, warn, or 
  install the required component as appropriate.

  Supported Operating Systems:
    Windows 7 32-bit, 64-bit
    Windows 8 32-bit, 64-bit
    Windows 10 32-bit, 64-bit

  Shared Components
    Before this driver can be installed, your computer must already have:
	  IVI Shared Components Version: 2.6.1 or newer installed

    The IVI Shared Components installers are available from: 
    http://www.ivifoundation.org/shared_components/Default.aspx

  VISA-COM
    Any compliant implementation is acceptable. Typically, VISA-COM is installed
	with VISA and other I/O library modules.  The latest version of Keysight's IO
	Libraries is recommended and includes VISA-COM.
    You can download the latest version from:
      http://www.keysight.com/find/iosuite 

	
Uninstall
---------
  This driver can be uninstalled like any other software from the Control Panel 
  using "Add or Remove Programs" or "Programs and Features" dialog.

  The IVI Shared Components may also be uninstalled like any other software from
  the Control Panel using the "Add or Remove Programs" or "Program & 
  Features" dialog.

  Note: All IVI-COM/C drivers require the IVI Shared Components to function. To 
  completely remove IVI components from your computer, uninstall all drivers and
  then uninstall the IVI Shared Components.

  
Source Code
-----------
  Driver source code is available by enabling the "Source Code" option in the
  "Custom Setup" dialog when installing the driver.  This code is provided as
  is for informational purposes only.  Modification of this code is not 
  supported.  Code is a Visual Studio 2010 C++ project and may be updated to new
  versions of Visual Studio.

  Caution: Once you have installed version 2.x of the IVI Shared Components, 
  you will not be able to build IVI drivers and applications developed with 
  earlier versions. You will need to upgrade those drivers/applications to the 
  new IVI Shared Components and to build on Visual Studio 2010 or higher or you 
  will need to build those drivers/applications on a different machine that does
  not have version 2.x of the IVI Shared Components.
  
Start Menu Help File 
--------------------
  A shortcut to the driver help file is added to the Start Menu, All Programs, 
  Keysight Instrument Drivers, IVI-COM-C Drivers, KtIviComDrvr group.  It contains
  "Getting Started"   information on using the driver in a variety of programming 
  environments as   well as documentation on IVI and instrument specific  methods and
  properties.

  You will also see shortcuts to the Readme and Introduction files and 
  programming examples for this driver.


Additional Setup
----------------
  .NET Framework
  The .NET Framework itself is not required by this driver. If you plan to use 
  the driver with .NET, the minimal .NET framework version is: 2.0

  The .NET Framework requires an interop assembly for a COM server. A Primary
  Interop Assembly, along with an XML file for IntelliSense is installed with
  the driver. The driver's PIA along with IVI PIAs are installed by default in:
  drive:\<Program Files>\IVI Foundation\IVI\Bin\Primary Interop Assemblies

  The PIA is also installed into the Global Assembly Cache (GAC) if you have the
  .NET framework installed.


Using a New Version of the Driver
---------------------------------
  New versions of this Keysight IVI-COM/C driver may have a new ProgId.

  If you use the version dependent ProgId in CoCreateInstance, you will need to 
  modify and recompile your code to use the new ProgID once you upgrade to the 
  next version of the driver.  Doing a side-by-side installation of the driver 
  to use multiple versions of the driver is not supported.  If you need to go 
  back to an older version of the driver, you need to uninstall the later
  version and install the older version.

  If you use the version independent ProgId in CoCreateInstance, you will not 
  need to modify and recompile your code.  The new version of the driver has 
  been tested to be backwards compatible with previous versions.

  To access the new functionality in a new version of the driver you will need 
  to use the latest numbered IKtIviComDrvr[n] interface rather than the IKtIviComDrvr 
  interface.  The IKtIviComDrvr[n].<interface> property will return a pointer
  to the new IKtIviComDrvr<interface>[n] interface.  The IKtIviComDrvr<interface>[n] 
  interface contains the methods and properties for the new functionality and 
  inherits all prior interface functionality.  The new interfaces were 
  introduced rather than modifying the existing interfaces for backwards 
  compatibility.  The interfaces that were previously shipped have not been 
  changed.
  
  Pre-existing .NET client applications must be re-build before using the new 
  version of the driver.

  
Revision History
----------------
  Version     Date      Notes
  -------   --------    -----
  2.2.2.0   Sep 2020    Added model support for B2901B,B2901BL,B2902B,B2910BL,B2911B,B2912B,B2961B,B2962B.
  2.1.1.0   Jun 2018    Fixed customer reported defect.
  2.1.0.0   Mar 2015    Updated help file, added IVI-2014 Compliance, Rebranded Keysight Technologies
  2.0.5.0   Nov 2012	Enhanced driver to support B296x family of instruments 
  1.0.7.0   June 2011	IviDCPwr class support added for IVI C driver also
  1.0.6.0   June 2011	Initial release

IVI Compliance 
--------------
IVI-COM/IVI-C IviDCPwr Specific Instrument Driver 


IVI Generation: IVI-2014
IVI Instrument Class: IviDCPwr
IviDCPwr Spec: IVI-4.4              Revision: 3.0 
Group Capabilities Supported:
  IviDCPwrBase                      Yes  
  IviDCPwrTrigger                   Yes  
  IviDCPwrSoftwareTrigger           Yes  
  IviDCPwrMeasurement               Yes  

Optional Features: 
  Interchangeability Checking       No
  State Caching	                    No
  Coercion Recording                No

Driver Identification: 
  Vendor:                         Keysight Technologies 
  Description:                    AgB29xx Arbitrary Waveform Generator
  Revision:                       2.2.2.0
  Component Identifier:           AgB29xx.AgB29xx

Hardware Information: 
  Instrument Manufacturer:        Keysight Technologies
  Supported Instrument Models:    B2901A, B2902A, B2911A, B2912A, B2961A, B2962A
  Supported Bus Interfaces:       TCPIP, GPIB

32-bit Software Information:
  Supported Operating Systems:    Windows 7 32-bit, Windows 8 32-bit, Windows 10 32-bit
  Unsupported Operating System:   Windows 2000
  Support Software Required:      VISA-COM
  Source Code Availability:       Source code included with driver via custom installation option.

64-bit Software Information:
  Supported Operating Systems: 	  Windows 7 64-bit, Windows 8 64-bit, Windows 10 64-bit 
  Support Software Required:      VISA-COM
  Source Code Availability:       Source code included with driver via custom installation option.


Unit Testing
------------
Test Setup Instrument:
  Instrument Models (FW Revision):      B2912B (5.0.2029.1911)
  Bus Interface:                        TCPIP
  Operating System (Service Pack):      Windows 10
  OS Bitness/Application Bitness:       64-bit/32-bit
  VISA Vendor and Version:              Keysight VISA-COM (IO Libraries 18.1)
  IVI Shared Components Version:        2.6.1

Test Setup Simulation: 
  Instrument Models: (FW Rev N/A)       B2912B
  Bus Interface:                        N/A
  Operating System (Service Pack):      Windows 7 (SP1)
  OS Bitness/Application Bitness:       64-bit/32-bit, 64-bit/64-bit
  VISA Vendor and Version:              N/A
  IVI Shared Components Version:        2.6.1

Driver Installation Testing:
  Operating System (Service Pack):  Windows 7 (SP1), Windows 8, Windows 10
  OS Bitness:                       32-bit, 64-bit

Driver Buildability:
  Operating System (Service Pack):  Windows 7 (SP1), Windows 8, Windows 10
  OS Bitness:                       32-bit, 64-bit
  Visual Studio Version:            VS2010

Driver Test Failures - Known Issues:
  None - This driver does not have any known defects. 

Keysight Technologies has evaluated and tested this driver to verify that it meets all applicable 
requirements of the IVI specifications at the time this compliance document was submitted to the 
IVI Foundation and agrees to abide by the dispute arbitration provisions in Section 7 of IVI-1.2: 
Operating Procedures, if the IVI Foundation finds this driver to be non-conformant.

More Information
----------------
  For more information about this driver and other instrument drivers and 
  software available from Keysight Technologies visit:
    http://www.keysight.com/find/drivers

  A list of contact information is available from:
    http://www.keysight.com/find/contactus

  Microsoft, Windows, MS Windows, and Windows NT are U.S. 
  registered trademarks of Microsoft Corporation.

Copyright Keysight Technologies 2020

