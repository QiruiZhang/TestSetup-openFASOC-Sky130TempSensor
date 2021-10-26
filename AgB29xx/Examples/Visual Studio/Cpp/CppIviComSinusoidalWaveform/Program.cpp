/***************************************************
*     Copyright Keysight Technologies 2011-2020
**************************************************/
#include "stdafx.h"
#include <atlstr.h>
#include <atlsafe.h>
#import "GlobMgr.dll"			no_namespace // VISA-COM I/O funtionality
#import "IviDriverTypeLib.dll"	no_namespace // IVI inherent functionality
#import "AgB29xx.dll"		no_namespace // AgB29xx driver functionality
#include <string.h>
///
/// AgB29xx IVI-COM Driver Example Program
/// 
/// Creates a driver object, reads a few Identity interface properties, and checks the instrument error queue.
/// May include additional instrument specific functionality.
/// 
/// See driver help topic "Programming with the IVI-COM Driver in Various Development Environments"
/// for additional programming information.
///
/// Runs in simulation mode without an instrument.
/// 

int _tmain(int argc, _TCHAR* argv[])
{
	::CoInitialize(NULL);
	printf("  Cpp_SinusoidalWaveform\n\n");

	try
	{
		// Create an instance of the driver.
		IAgB29xx2Ptr spDriver(__uuidof(AgB29xx));

		try
		{
			// Edit resource and options as needed.  Resource is ignored if option Simulate=true
			CString strResourceDesc = "GPIB0::23::INSTR";
			//strResourceDesc = "TCPIP0::<ip or hostname>::INSTR";

			CString strInitOptions = "QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut";

			VARIANT_BOOL idQuery = VARIANT_TRUE;
			VARIANT_BOOL reset   = VARIANT_TRUE;

			// Initialize the driver.  See driver help topic "Initializing the IVI-COM Driver" for additional information
			spDriver->Initialize(LPCTSTR(strResourceDesc), idQuery, reset, LPCTSTR(strInitOptions));	
			printf("Driver Initialized\n");

			// Print a few IIviDriverIdentity properties
			wprintf(L"Identifier:  %s\n", spDriver->Identity->Identifier.GetBSTR());
			wprintf(L"Revision:    %s\n", spDriver->Identity->Revision.GetBSTR());
			wprintf(L"Vendor:      %s\n", spDriver->Identity->Vendor.GetBSTR());
			wprintf(L"Description: %s\n", spDriver->Identity->Description.GetBSTR());
			wprintf(L"Model:       %s\n", spDriver->Identity->InstrumentModel.GetBSTR());
			wprintf(L"FirmwareRev: %s\n", spDriver->Identity->InstrumentFirmwareRevision.GetBSTR());
			wprintf(L"Serial #:    %s\n", spDriver->System->SerialNumber.GetBSTR());
			VARIANT_BOOL boolSimulate = spDriver->DriverOperation->Simulate;
			if (boolSimulate == VARIANT_TRUE)
				wprintf(L"\nSimulate:    True\n\n");
			else
				wprintf(L"Simulate:    False\n\n");


			//  Exercise driver methods and properties
			int iNumberOfChannels = spDriver->Outputs->Count;
			CString str = _T("");
			str = spDriver->Identity->InstrumentModel.GetBSTR();
			for (int i = 1; i <= iNumberOfChannels; i++)
			{
				//Set sinusoidal voltage waveform
				//Configure Function Mode: Voltage
				spDriver->Outputs2->GetItem2(spDriver->Outputs2->GetName(i))->Type = AgB29xxOutputTypeVoltage;				
				if (str == _T("B2961A") ||str == _T("B2961B") ||str == _T("B2962A") ||str == _T("B2962B"))
				{
					//Configure Voltage Mode to Arbitrary Waveform  
					spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->ArbitraryWaveform->ConfigureMode(AgB29xxTransientFunctionTypeVoltage);

					//Set Arbitrary Waveform Shape to Sinusoidal
					spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->ArbitraryWaveform->Shape = AgB29xxTransientArbitraryWaveformShapeSinusoid;

					//Set Sinusoid Amplitude
					spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->ArbitraryWaveform->Voltage->Sinusoid->Amplitude = 1.0;

					//Set Sinusoid Frequency
					spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->ArbitraryWaveform->Voltage->Sinusoid->Frequency = 1.0;
				}

				//Set sampling voltage measurement
				//Set measurement function to Voltage
				CComSafeArray<int> cArr;
				cArr.Create(1);
				cArr[0] = 1;
				LPSAFEARRAY psa;
				psa = cArr.Detach();
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Function->SetEnabled(&psa);
				cArr.Destroy();
				::SafeArrayDestroy(psa);

				//Set number of power line cycles (NPLC)
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Current2->NPLC = 0.1;

				//Set the Compliance value (Current Protection)
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Current2->ComplianceValue = 0.1;

				//Generate Triggers    
				//Set Transient Trigger count: 1
				spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->Trigger->Count = 1;

				//Set Trigger source
				spDriver->Transients2->GetItem2(spDriver->Transients2->GetName(i))->Trigger->Source = AgB29xxArmTriggerSourceAint;

				//Set Measurement Trigger count: 100
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Trigger->Count = 100;

				//Set Measurement Trigger source: Timer
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Trigger->Source = AgB29xxArmTriggerSourceTimer;

				//Set Measurement interval - Timer Trigger source 
				spDriver->Measurements2->GetItem2(spDriver->Measurements2->GetName(i))->Trigger->Timer = 0.01;

				//Turn on Output switch	
				spDriver->Outputs2->GetItem2(spDriver->Outputs2->GetName(i))->Enabled = true;

			}
			//Initiate transition and acquire
			bstr_t chanlist;
			if (iNumberOfChannels == 1)
				chanlist = "1";
			else
				chanlist = "1,2";

			spDriver->Trigger->Initiate(chanlist);

			//Retrieve measurement result			
			SAFEARRAY* psaData = spDriver->Measurements2->FetchArrayData(AgB29xxMeasurementFetchTypeVoltage, chanlist);
			CComSafeArray<double> saData;
			saData.Attach(psaData);

			printf("%s", "\nSinusoidal Waveform data (in Volts):\n\n");

			// Display results 		
			for (int i = 0; i < (int)saData.GetCount(); i++)
			{	
				printf("%4.2le\t", saData.GetAt(i));
			}
			saData.Destroy();

			// Turn off output switch           
			for (int i = 1; i <= iNumberOfChannels; i++)
			{
				spDriver->Outputs2->GetItem2(spDriver->Outputs2->GetName(i))->Enabled = false;
			}


			// Check instrument for errors
			long lErrorNum = -1;
			_bstr_t bstrErrorMsg;
			wprintf(L"\n");
			while (lErrorNum != 0)
			{
				spDriver->Utility->ErrorQuery(&lErrorNum, bstrErrorMsg.GetAddress());
				wprintf(L"ErrorQuery: %d, %s\n", lErrorNum, bstrErrorMsg.GetBSTR());
			}
		}
		catch (_com_error& e)
		{
			wprintf(e.Description(), e.ErrorMessage(), MB_ICONERROR);
		}

		if (spDriver != NULL && spDriver->Initialized)
		{
			// Close the driver
			spDriver->Close();
			printf("Driver Closed\n");
		}
	}
	catch (_com_error& e)
	{
		wprintf(e.Description(), e.ErrorMessage(), MB_ICONERROR);
	}

	::CoUninitialize();

	printf("\nDone - Press Enter to Exit");
	getchar();

	return 0;
}
