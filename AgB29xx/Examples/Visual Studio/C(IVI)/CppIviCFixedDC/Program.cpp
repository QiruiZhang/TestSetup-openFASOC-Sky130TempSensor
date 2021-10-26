/***************************************************
 *     Copyright Keysight Technologies 2011-2020
 **************************************************/

#include "stdafx.h"
#include "AgB29xx.h"
// Link to: <Program Files>\IVI Foundation\IVI\Lib\msc\AgB29xx.lib

///
/// AgB29xx IVI-C Driver Example Program
/// 
/// Initializes the driver, reads a few Identity interface properties, and checks the instrument error queue.
/// May include additional instrument specific functionality.
/// 
/// See driver help topic "Programming with the IVI-C Driver in Various Development Environments"
/// for additional programming information.
///
/// Runs in simulation mode without an instrument.
/// 

int _tmain(int argc, _TCHAR* argv[])
{
	ViStatus status;
	ViSession session;
	ViChar str[128];
	ViInt32 ErrorCode;
	ViChar ErrorMessage[256];
	ViBoolean simulate;
	ViInt32 iNumberOfChannels;
	ViChar OutputName[256];
	ViChar MeasurementName[256];
	int i;
	ViReal64 Val[2];
	ViInt32 ValActualSize;
	ViConstString ChanList;
	// Edit resource and options as needed.  resource is ignored if option Simulate=true
	char resource[] = "GPIB0::23::INSTR";
	//char resource[] = "TCPIP0::<ip or host name>::INSTR";

	char options[]  = "QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut";

	ViBoolean idQuery = VI_TRUE;
	ViBoolean reset   = VI_TRUE;

	printf("  C_FixedDC\n\n");

	// Initialize the driver.  See driver help topic "Initializing the IVI-C Driver" for additional information
	status = AgB29xx_InitWithOptions(resource, idQuery, reset, options, &session);
	if(status)
	{
		// Initialization failed
		AgB29xx_GetError(session, &ErrorCode, 255, ErrorMessage);
		printf("** InitWithOptions() Error: %d, %s\n", ErrorCode, ErrorMessage);
		printf("\nDone - Press Enter to Exit");
		getchar();  
		return ErrorCode;
	}
	assert(session != VI_NULL);
	printf("Driver Initialized \n");

	// Read and output a few attributes
	// Return status checking omitted for example clarity
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_SPECIFIC_DRIVER_PREFIX, 127, str);
	assert(status == VI_SUCCESS);
	printf("DRIVER_PREFIX:      %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_SPECIFIC_DRIVER_REVISION, 127, str);
	assert(status == VI_SUCCESS);
	printf("DRIVER_REVISION:    %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_SPECIFIC_DRIVER_VENDOR, 127, str);
	assert(status == VI_SUCCESS);
	printf("DRIVER_VENDOR:      %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_SPECIFIC_DRIVER_DESCRIPTION, 127, str);
	assert(status == VI_SUCCESS);
	printf("DRIVER_DESCRIPTION: %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_INSTRUMENT_MODEL, 127, str);
	assert(status == VI_SUCCESS);
	printf("INSTRUMENT_MODEL:   %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_INSTRUMENT_FIRMWARE_REVISION, 127, str);
	assert(status == VI_SUCCESS);
	printf("FIRMWARE_REVISION:  %s\n", str);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_SYSTEM_SERIAL_NUMBER, 127, str);
	assert(status == VI_SUCCESS);
	printf("SERIAL_NUMBER:      %s\n", str);
	status = AgB29xx_GetAttributeViBoolean(session, "", AGB29XX_ATTR_SIMULATE, &simulate);
	assert(status == VI_SUCCESS);
	if (simulate == VI_TRUE)
		printf("\nSIMULATE:           True\n\n");
	else
		printf("SIMULATE:           False\n\n");


	// Exercise driver methods and properties
	status = AgB29xx_GetAttributeViInt32(session, "", AGB29XX_ATTR_OUTPUT_CHANNEL_COUNT, &iNumberOfChannels);
	status = AgB29xx_GetAttributeViString(session, "", AGB29XX_ATTR_INSTRUMENT_MODEL, 127, str);

	for (i = 1; i <= iNumberOfChannels; i++)
    {
        // Set voltage output to 2.0V
		AgB29xx_GetOutputChannelName( session, 1 ,256, OutputName);
		AgB29xx_SetAttributeViBoolean(session , OutputName, AGB29XX_ATTR_OUTPUT_VOLTAGE_AUTO_RANGE_ENABLED, VI_FALSE);
		AgB29xx_SetAttributeViReal64(session , OutputName, AGB29XX_ATTR_OUTPUT_VOLTAGE_RANGE, 20.0);
		AgB29xx_SetAttributeViReal64(session , OutputName, AGB29XX_ATTR_OUTPUT_VOLTAGE_LEVEL, 2.0);
		AgB29xx_SetAttributeViReal64(session , OutputName, AGB29XX_ATTR_OUTPUT_VOLTAGE_TRIGGERED_LEVEL, 2.0);

		// Set auto-range current measurement		
		AgB29xx_GetMeasurementName( session, 1 ,256, MeasurementName);
		if (str == "B2901A" ||str == "B2902A" ||str == "B2911A" ||str == "B2912A" || str == "B2901B" ||str == "B2902B" ||str == "B2911B" ||str == "B2912B")
			AgB29xx_SetAttributeViBoolean(session , MeasurementName, AGB29XX_ATTR_MEASUREMENT_CURRENT_AUTO_RANGE_ENABLED, VI_TRUE);//Supported Models for this property: B2901A|B, B2902A|B, B2911A|B, B2912A|B 

		AgB29xx_SetAttributeViReal64(session , MeasurementName, AGB29XX_ATTR_MEASUREMENT_CURRENT_NPLC, 0.1);

        // Turn on output switch
		AgB29xx_SetAttributeViBoolean(session , OutputName, AGB29XX_ATTR_OUTPUT_ENABLED, VI_TRUE);

    }

	 // Measure
        //
		if (iNumberOfChannels == 1)
			ChanList = "1";
		else
			ChanList = "1,2";

		status = AgB29xx_Trigger_Initiate(session,128,ChanList);
		
        //
        // Query Results
		
		status = AgB29xx_Measurement_FetchArrayData(session ,AGB29XX_VAL_MEASUREMENT_FETCH_TYPE_CURRENT,128,ChanList,512,Val, &ValActualSize);

		printf("%s", "Fixed DC data:");

		// Display results 
	
		for (i = 0; i < ValActualSize; i++)
		{
			printf("\n\n%le", Val[i]);
		}
		
        // Turn off output switch
        //
        for (i = 1; i <= iNumberOfChannels; i++)
        {
			AgB29xx_SetAttributeViBoolean(session , OutputName, AGB29XX_ATTR_OUTPUT_ENABLED, VI_FALSE);
        }


	// Check instrument for errors
	ErrorCode = -1;
	printf("\n");
	while(ErrorCode!=0)
	{
		status = AgB29xx_error_query( session, &ErrorCode, ErrorMessage);
		assert(status == VI_SUCCESS);
		printf("error_query: %d, %s\n", ErrorCode, ErrorMessage);
	}

	// Close the driver
	status = AgB29xx_close(session);
	assert(status == VI_SUCCESS);
	session = VI_NULL;
	printf("Driver Closed \n");

	printf("\nDone - Press Enter to Exit");
	getchar();

	return 0;
}
