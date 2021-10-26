/***************************************************
 *     Copyright Keysight Technologies 2011-2020
 **************************************************/
#include "stdafx.h"
#include <atlstr.h>
#include <atlsafe.h>
#import "GlobMgr.dll"			no_namespace // VISA-COM I/O funtionality
#import "IviDriverTypeLib.dll"	no_namespace // IVI inherent functionality
#import "AgB29xx.dll"		no_namespace // AgB29xx driver functionality

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
	printf("  Cpp_StaircaseSweep\n\n");

	try
	{
		// Create an instance of the driver.
		IAgB29xxPtr spDriver(__uuidof(AgB29xx));
	
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
					// Set voltage sweep outputs (-5V to 5V, 11 steps)
                    spDriver->Transients->GetItem(spDriver->Transients->GetName(i))->Voltage->Mode = AgB29xxTransientCurrentVoltageModeSweep;
                    spDriver->Transients->GetItem(spDriver->Transients->GetName(i))->Voltage->Start = -5.0;
                    spDriver->Transients->GetItem(spDriver->Transients->GetName(i))->Voltage->Stop = +5.0;
                    spDriver->Transients->GetItem(spDriver->Transients->GetName(i))->Voltage->SweepPoints = 11;

					spDriver->Outputs->GetItem(spDriver->Outputs->GetName(i))->Voltage->AutoRangeEnabled= false;
					spDriver->Outputs->GetItem(spDriver->Outputs->GetName(i))->Voltage->Range = 20.0;
					spDriver->Outputs->GetItem(spDriver->Outputs->GetName(i))->Voltage->Level= 2.0;
					
                    // Set auto-range current measurement				
					if (str == _T("B2901A") ||str == _T("B2902A") ||str == _T("B2911A") ||str == _T("B2912A") || str == _T("B2901B") ||str == _T("B2902B") ||str == _T("B2911B") ||str == _T("B2912B"))
					{
						spDriver->Measurements->GetItem(spDriver->Measurements->GetName(i))->Current->AutoRangeEnabled = true;//Supported Models for this property: B2901A|B, B2902A|B, B2911A|B, B2912A|B
					}					
					spDriver->Measurements->GetItem(spDriver->Measurements->GetName(i))->Current->NPLC = 0.1;

					// Set trigger condition

                    //trigger.TriggerCount = 11;
                    spDriver->Transients->GetItem(spDriver->Transients->GetName(i))->Trigger->Count = 11;
                    spDriver->Measurements->GetItem(spDriver->Measurements->GetName(i))->Trigger->Count = 11;


                    // Turn on output switch
					spDriver->Outputs->GetItem(spDriver->Outputs->GetName(i))->Enabled = true;

                }

                // Measure
                //
				bstr_t chanlist;
				if (iNumberOfChannels == 1)
					chanlist = "1";
				else
					chanlist = "1,2";

				spDriver->Trigger->Initiate(chanlist);

                //
                // Query Results
				
               SAFEARRAY* psaData = spDriver->Measurements->FetchArrayData(AgB29xxMeasurementFetchTypeCurrent, chanlist);
               CComSafeArray<double> saData;
			   saData.Attach(psaData);

			   printf("%s", "Staircase sweep data:");

				// Display results 
			
				for (int i = 0; i < (int)saData.GetCount(); i++)
				{
					printf("\n\n%le", saData.GetAt(i));
				}
				saData.Destroy();
                //
                // Turn off output switch
                //
                for (int i = 1; i <= iNumberOfChannels; i++)
                {
					spDriver->Outputs->GetItem(spDriver->Outputs->GetName(i))->Enabled = false;
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
