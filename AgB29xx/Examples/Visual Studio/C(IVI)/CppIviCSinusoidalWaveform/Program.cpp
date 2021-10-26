/***************************************************
*     Copyright Keysight Technologies 2011-2020
**************************************************/
#include "stdafx.h"
#include "AgB29xx.h"
#include <string.h>
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
	ViChar MeasurementName[256];
	ViChar TransientName[256];
	ViChar OutputName[256];
	ViInt32 FunctionName[1];
	ViConstString ChanList;	
	ViInt32 ValBufferSize = 100;
	ViReal64 Val[100] = { 0 };
	ViInt32 ValActualSize = 100;

	int i;
	// Edit resource and options as needed.  resource is ignored if option Simulate=true
	//char resource[] = "GPIB0::23::INSTR";
	char resource[] = "GPIB0::23::INSTR";
	//char resource[] = "TCPIP0::<ip or host name>::INSTR";

	char options[]  = "QueryInstrStatus=true, Simulate=True, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut";

	ViBoolean idQuery = VI_TRUE;
	ViBoolean reset   = VI_TRUE;

	printf("  C_SinusoidalWaveform\n\n");

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


	//  Exercise driver methods and properties
	status = AgB29xx_GetAttributeViInt32(session, "", AGB29XX_ATTR_OUTPUT_CHANNEL_COUNT, &iNumberOfChannels);

	for (i = 1; i <= iNumberOfChannels; i++)
	{	
		//Set sinusoidal voltage waveform				
		AgB29xx_GetTransientName( session, i ,256, TransientName);
		AgB29xx_GetMeasurementName( session, i ,256, MeasurementName);
		AgB29xx_GetOutputChannelName( session, i ,256, OutputName);

		//Configure Function Mode: Voltage
		AgB29xx_SetAttributeViInt32(session,OutputName,AGB29XX_ATTR_OUTPUT_TYPE,AGB29XX_VAL_OUTPUT_TYPE_VOLTAGE);

		if((strstr(str,"B2961A")) || (strstr(str,"B2961B")) || (strstr(str,"B2962A")) || (strstr(str,"B2962B")))
		{
			//Configure Voltage Mode to Arbitrary Waveform  
			AgB29xx_ArbitraryWaveform_ConfigureMode(session,TransientName,AGB29XX_VAL_TRANSIENT_FUNCTION_TYPE_VOLTAGE); 

			//Set Arbitrary Waveform Shape to Sinusoidal
			AgB29xx_SetAttributeViInt32(session,TransientName,AGB29XX_ATTR_ARBITRARYWAVEFORM_SHAPE,AGB29XX_VAL_TRANSIENT_ARBITRARYWAVEFORM_SHAPE_SINUSOID);

			//Set Sinusoid Amplitude
			AgB29xx_SetAttributeViReal64(session,TransientName,AGB29XX_ATTR_ARBITRARYWAVEFORM_VOLTAGE_SINUSOID_AMPLITUDE,1.0);

			//Set Sinusoid Frequency
			AgB29xx_SetAttributeViReal64(session,TransientName,AGB29XX_ATTR_ARBITRARYWAVEFORM_VOLTAGE_SINUSOID_FREQUENCY,1.0);
		}

		//Set sampling voltage measurement		
		FunctionName[0] = AGB29XX_VAL_MEASURE_TYPE_VOLTAGE;

		//Set measurement function to Voltage
		AgB29xx_Function_SetEnabled(session,MeasurementName,1,FunctionName);

		//Set number of power line cycles (NPLC)
		AgB29xx_SetAttributeViReal64(session,MeasurementName,AGB29XX_ATTR_MEASUREMENT_CURRENT_NPLC,0.1);

		//Set the Compliance value (Current Protection)
		AgB29xx_SetAttributeViReal64(session,MeasurementName,AGB29XX_ATTR_MEASUREMENT_CURRENT_COMPLIANCE_VALUE,0.1);


		//Generate Triggers
		//Set Transient Trigger count: 1
		AgB29xx_SetAttributeViInt32(session,TransientName,AGB29XX_ATTR_TRANSIENT_TRIGGER_COUNT,1);

		//Set Trigger source
		AgB29xx_SetAttributeViInt32(session,TransientName,AGB29XX_ATTR_TRANSIENT_TRIGGER_SOURCE,AGB29XX_VAL_ARM_TRIGGER_SOURCE_AINT);

		//Set Measurement Trigger count: 100
		AgB29xx_SetAttributeViInt32(session,MeasurementName,AGB29XX_ATTR_MEASUREMENT_TRIGGER_COUNT,100);

		//Set Measurement Trigger source: Timer
		AgB29xx_SetAttributeViInt32(session,MeasurementName,AGB29XX_ATTR_MEASUREMENT_TRIGGER_SOURCE,AGB29XX_VAL_ARM_TRIGGER_SOURCE_TIMER);

		//Set Measurement interval - Timer Trigger source 
		AgB29xx_SetAttributeViReal64(session,MeasurementName,AGB29XX_ATTR_MEASUREMENT_TRIGGER_TIMER ,0.01);		

		//Turn on output switch		
		AgB29xx_SetAttributeViBoolean(session , OutputName, AGB29XX_ATTR_OUTPUT_ENABLED, VI_TRUE);		
	}
	//Initiate transition and acquire
	if (iNumberOfChannels == 1)
		ChanList = "1";
	else
		ChanList = "1,2";

	status = AgB29xx_Trigger_Initiate(session,128,ChanList);

	//Retrieve measurement result		
	status = AgB29xx_Measurement_FetchArrayData(session ,AGB29XX_VAL_MEASUREMENT_FETCH_TYPE_VOLTAGE,128,ChanList,ValBufferSize, Val, &ValActualSize);		
	printf("%s", "\n\nSinusoidal Waveform data (in Volts):\n\n");

	// Display results 	
	for (i = 0; i < ValActualSize; i++)
	{	
		printf("%4.2le\t", Val[i]);		
	}

	// Turn off output switch
	for (i = 1; i <= iNumberOfChannels; i++)
	{
		AgB29xx_GetOutputChannelName( session, i ,256, OutputName);
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
