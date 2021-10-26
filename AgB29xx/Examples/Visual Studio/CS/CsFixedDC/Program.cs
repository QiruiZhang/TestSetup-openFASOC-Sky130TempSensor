/***************************************************
 *     Copyright Keysight Technologies 2011-2020
 **************************************************/
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using Agilent.AgB29xx.Interop;

namespace AgB29xx_CS_FixedDC
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
            Console.WriteLine("  CS_FixedDC");
            Console.WriteLine();
            AgB29xx driver = null;

            try
            {
                // Create driver instance
                driver = new AgB29xx();

                // Edit resource and options as needed.  Resource is ignored if option Simulate=true
                string resourceDesc = "GPIB0::23::INSTR";
                //resourceDesc = "TCPIP0::<ip or hostname>::INSTR";

                string initOptions = "QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut";

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

                int iNumberOfChannels = driver.Outputs.Count;
                string str = driver.Identity.InstrumentModel;

                for (int i = 1; i <= iNumberOfChannels; i++)
                {
                    // Set voltage output to 2.0V
                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Voltage.AutoRangeEnabled = false;
                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Voltage.Range = 20.0;
                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Voltage.Level = 2.0;
                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Voltage.TriggeredLevel = 2.0;

                    // Set auto-range current measurement
                    if (str == "B2901A" || str == "B2902A" || str == "B2911A" || str == "B2912A" || str == "B2901B" || str == "B2902B" || str == "B2911B" || str == "B2912B")
                        driver.Measurements.get_Item(driver.Measurements.get_Name(i)).Current.AutoRangeEnabled = true;//Supported Models for this property: B2901A|B, B2902A|B, B2911A|B, B2912A|B 

                    driver.Measurements.get_Item(driver.Measurements.get_Name(i)).Current.NPLC = 0.1;

                    // Turn on output switch

                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Enabled = true;

                }

                // Measure
                //
                string chanlist;
                if (iNumberOfChannels == 1)
                    chanlist = "1";
                else
                    chanlist = "1,2";

                driver.Trigger.Initiate(chanlist);

                //
                // Query Results

                double[] dResult = driver.Measurements.FetchArrayData(Agilent.AgB29xx.Interop.AgB29xxMeasurementFetchTypeEnum.AgB29xxMeasurementFetchTypeCurrent, "(@1,2)");

                Console.WriteLine("Fixed DC data:");

                for (int i = 0; i < dResult.Length; i++)
                {
                    System.Console.WriteLine("Item[" + i + "]: " + dResult[i].ToString());
                }

                //
                // Turn off output switch
                //
                for (int i = 1; i <= iNumberOfChannels; i++)
                {
                    driver.Outputs.get_Item(driver.Outputs.get_Name(i)).Enabled = false;
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
