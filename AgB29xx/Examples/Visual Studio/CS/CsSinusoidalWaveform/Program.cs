/***************************************************
 *     CCopyright Keysight Technologies 2011-2020
 **************************************************/
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using Agilent.AgB29xx.Interop;

namespace AgB29xx_CS_SinusoidalWaveform
{
    /// <summary>
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
    /// Requires a reference to the driver's interop or COM type library.
    /// 
    /// </summary>
    class Program
    {
        [STAThread]
        public static void Main(string[] args)
        {
            Console.WriteLine("  CS_SinusoidalWaveform");
            Console.WriteLine();
            AgB29xx driver = null;

            try
            {
                // Create driver instance
                driver = new AgB29xx();

                // Edit resource and options as needed.  Resource is ignored if option Simulate=true
                string resourceDesc = "GPIB0::23::INSTR";
                //resourceDesc = "TCPIP0::<ip or hostname>::INSTR";

                string initOptions = "QueryInstrStatus=false, Simulate=true, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut";

                bool idquery = true;
                bool reset = true;

                // Initialize the driver.  See driver help topic "Initializing the IVI-COM Driver" for additional information
                driver.Initialize(resourceDesc, idquery, reset, initOptions);
                Console.WriteLine("Driver Initialized");

                // Print a few IIviDriverIdentity properties
                Console.WriteLine("Identifier:  {0}", driver.Identity.Identifier);
                Console.WriteLine("Revision:    {0}", driver.Identity.Revision);
                Console.WriteLine("Vendor:      {0}", driver.Identity.Vendor);
                Console.WriteLine("Description: {0}", driver.Identity.Description);
                Console.WriteLine("Model:       {0}", driver.Identity.InstrumentModel);
                Console.WriteLine("FirmwareRev: {0}", driver.Identity.InstrumentFirmwareRevision);
                Console.WriteLine("Serial #:    {0}", driver.System.SerialNumber);
                Console.WriteLine("\nSimulate:    {0}\n", driver.DriverOperation.Simulate);


                //  Exercise driver methods and properties
                int iNumberOfChannels = driver.Outputs2.Count;

                for (int i = 1; i <= iNumberOfChannels; i++)
                {
                    //Set sinusoidal voltage waveform
                    //Configure Function Mode: Voltage
                    driver.Outputs2.get_Item2(driver.Outputs2.get_Name(i)).Type = AgB29xxOutputTypeEnum.AgB29xxOutputTypeVoltage;

                    if ((driver.Identity.InstrumentModel == "B2961A") || (driver.Identity.InstrumentModel == "B2961B") || (driver.Identity.InstrumentModel == "B2962A") || (driver.Identity.InstrumentModel == "B2962B"))
                    {
                        //Configure Voltage Mode to Arbitrary Waveform  
                        driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).ArbitraryWaveform.ConfigureMode(AgB29xxTransientFunctionTypeEnum.AgB29xxTransientFunctionTypeVoltage);

                        //Set Arbitrary Waveform Shape to Sinusoidal
                        driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).ArbitraryWaveform.Shape = AgB29xxTransientArbitraryWaveformShapeEnum.AgB29xxTransientArbitraryWaveformShapeSinusoid;

                        //Set Sinusoid Amplitude
                        driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Amplitude = 1.0;

                        //Set Sinusoid Frequency
                        driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Frequency = 1.0;
                    }
                    //Set sampling voltage measurement
                    //Set measurement function to Voltage
                    AgB29xxMeasurementTypeEnum[] FunctionName = { AgB29xxMeasurementTypeEnum.AgB29xxMeasurementTypeVoltage };
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Function.SetEnabled(ref FunctionName);

                    //Set number of power line cycles (NPLC)
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Current2.NPLC = 0.1;

                    //Set the Compliance value (Current Protection)
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Current2.ComplianceValue = 0.1;

                    //Generate Triggers    
                    //Set Transient Trigger count: 1
                    driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).Trigger.Count = 1;

                    //Set Trigger source
                    driver.Transients2.get_Item2(driver.Transients2.get_Name(i)).Trigger.Source = AgB29xxArmTriggerSourceEnum.AgB29xxArmTriggerSourceAint;

                    //Set Measurement Trigger count: 100
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Trigger.Count = 100;

                    //Set Measurement Trigger source: Timer
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Trigger.Source = AgB29xxArmTriggerSourceEnum.AgB29xxArmTriggerSourceTimer;

                    //Set Measurement interval - Timer Trigger source 
                    driver.Measurements2.get_Item2(driver.Measurements2.get_Name(i)).Trigger.Timer = 0.01;

                    //Turn on Output switch	                    
                    driver.Outputs2.get_Item2(driver.Outputs2.get_Name(i)).Enabled = true;
                }

                //Initiate transition and acquire
                string chanlist;
                if (iNumberOfChannels == 1)
                    chanlist = "1";
                else
                    chanlist = "1,2";

                driver.Trigger.Initiate(chanlist);

                //Retrieve measurement result			
                double[] dResult = driver.Measurements2.FetchArrayData(Agilent.AgB29xx.Interop.AgB29xxMeasurementFetchTypeEnum.AgB29xxMeasurementFetchTypeVoltage, chanlist);
                Console.WriteLine("Sinusoidal Waveform data (in Volts):");

                // Display results 
                for (int i = 0; i < dResult.Length; i++)
                {
                    //System.Console.WriteLine("Item[" + i + "]: " + dResult[i].ToString());
                    Console.Write("{0:E2}\t", dResult[i]);
                }

                // Turn off output switch   
                for (int i = 1; i <= iNumberOfChannels; i++)
                {
                    driver.Outputs2.get_Item2(driver.Outputs2.get_Name(i)).Enabled = false;
                }


                // Check instrument for errors
                int errorNum = -1;
                string errorMsg = null;
                Console.WriteLine();
                while (errorNum != 0)
                {
                    driver.Utility.ErrorQuery(ref errorNum, ref errorMsg);
                    Console.WriteLine("ErrorQuery: {0}, {1}", errorNum, errorMsg);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                if (driver != null && driver.Initialized)
                {
                    // Close the driver
                    driver.Close();
                    Console.WriteLine("Driver Closed");
                }
            }

            Console.WriteLine("Done - Press Enter to Exit");
            Console.ReadLine();
        }
    }
}
