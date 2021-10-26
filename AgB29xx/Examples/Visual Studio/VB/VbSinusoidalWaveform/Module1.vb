'/***************************************************
'*     Copyright Keysight Technologies 2011-2020
'**************************************************/
Imports Ivi.Driver
Imports Agilent.AgB29xx.Interop

Module Module1

    ' AgB29xx IVI-COM Driver VB7 Example Program
    ' 
    ' Creates a driver object, reads a few Identity interface properties and checks the instrument error queue.
    ' May include additional instrument specific functionality.
    '
    ' See driver help topic "Programming with the IVI-COM Driver in Various Development Environments"
    ' for additional programming information.
    '
    ' Requires a reference to the driver's interop or COM type library.

    Sub Main()

        Console.WriteLine("  VB_SinusoidalWaveform")
        Console.WriteLine()

        ' Create an instance of the driver
        Dim driver As New AgB29xx()

        Try
            ' Edit resource and options as needed.  Resource is ignored if option Simulate=true
            Dim resourceDesc As String = "GPIB0::23::INSTR"
            ' resourceDesc = "TCPIP0::<ip or hostname>::INSTR"

            Dim initOptions As String = "QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false, TraceName=c:\\temp\\traceOut"

            Dim idquery As Boolean = True
            Dim reset As Boolean = True

            ' Initialize the driver.  See driver help topic "Initializing the IVI-COM Driver" for additional information
            driver.Initialize(resourceDesc, idquery, reset, initOptions)
            Console.WriteLine("Driver Initialized")

            ' Get driver Identity properties.
            Console.WriteLine("Identifier:  {0}", driver.Identity.Identifier)
            Console.WriteLine("Revision:    {0}", driver.Identity.Revision)
            Console.WriteLine("Vendor:      {0}", driver.Identity.Vendor)
            Console.WriteLine("Description: {0}", driver.Identity.Description)
            Console.WriteLine("Model:       {0}", driver.Identity.InstrumentModel)
            Console.WriteLine("FirmwareRev: {0}", driver.Identity.InstrumentFirmwareRevision)
            Console.WriteLine("Serial #:    {0}", driver.System.SerialNumber)
            Console.WriteLine()
            Console.WriteLine("Simulate:    {0}", driver.DriverOperation.Simulate)
            Console.WriteLine()


            '  driver specific tasks...

            Dim iNumberOfChannels As Integer
            iNumberOfChannels = driver.Outputs2.Count
            Dim i As Integer
            For i = 1 To iNumberOfChannels
                Dim str As String
                str = driver.Identity.InstrumentModel

                'Set sinusoidal voltage waveform
                'Configure Function Mode: Voltage
                driver.Outputs2.Item2(driver.Outputs2.Name(i)).Type = Agilent.AgB29xx.Interop.AgB29xxOutputTypeEnum.AgB29xxOutputTypeVoltage
              
                If (String.Equals(str, "B2961A") Or String.Equals(str, "B2961B") Or String.Equals(str, "B2962A") Or String.Equals(str, "B2962B")) Then

                    'Configure Voltage Mode to Arbitrary Waveform  
                    driver.Transients2.Item2(driver.Transients2.Name(i)).ArbitraryWaveform.ConfigureMode(Agilent.AgB29xx.Interop.AgB29xxTransientFunctionTypeEnum.AgB29xxTransientFunctionTypeVoltage)

                    'Set Arbitrary Waveform Shape to Sinusoidal
                    driver.Transients2.Item2(driver.Transients2.Name(i)).ArbitraryWaveform.Shape = Agilent.AgB29xx.Interop.AgB29xxTransientArbitraryWaveformShapeEnum.AgB29xxTransientArbitraryWaveformShapeSinusoid

                    'Set Sinusoid Amplitude
                    driver.Transients2.Item2(driver.Transients2.Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Amplitude = 1

                    'Set Sinusoid Frequency
                    driver.Transients2.Item2(driver.Transients2.Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Frequency = 1
                End If

                'Set sampling voltage measurement
                'Set measurement function to Voltage
                Dim FunctionName() As Agilent.AgB29xx.Interop.AgB29xxMeasurementTypeEnum = {Agilent.AgB29xx.Interop.AgB29xxMeasurementTypeEnum.AgB29xxMeasurementTypeVoltage}

                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Function.SetEnabled(FunctionName)

                'Set number of power line cycles (NPLC)
                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Current2.NPLC = 0.1

                'Set the Compliance value (Current Protection)
                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Current2.ComplianceValue = 0.1

                'Generate triggers
                'Set Transient Trigger count: 1
                driver.Transients2.Item2(driver.Transients2.Name(i)).Trigger.Count = 1

                'Set Trigger source
                driver.Transients2.Item2(driver.Transients2.Name(i)).Trigger.Source = Agilent.AgB29xx.Interop.AgB29xxArmTriggerSourceEnum.AgB29xxArmTriggerSourceAint

                'Set Measurement Trigger count: 100
                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Trigger.Count = 100

                'Set Measurement Trigger source: Timer
                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Trigger.Source = Agilent.AgB29xx.Interop.AgB29xxArmTriggerSourceEnum.AgB29xxArmTriggerSourceTimer

                'Set Measurement interval - Timer Trigger source 
                driver.Measurements2.Item2(driver.Measurements2.Name(i)).Trigger.Timer = 0.01

                'Turn on output switch
                driver.Outputs2.Item2(driver.Outputs2.Name(i)).Enabled = True
            Next i

            ' Initiate transition and acquire
            Dim chanlist As String

            If (iNumberOfChannels = 1) Then
                chanlist = "1"
            Else
                chanlist = "1,2"
            End If

            driver.Trigger.Initiate(chanlist)

            'Retrieve measurement result	
            Dim dResult As Double()
            dResult = driver.Measurements.FetchArrayData(Agilent.AgB29xx.Interop.AgB29xxMeasurementFetchTypeEnum.AgB29xxMeasurementFetchTypeVoltage, chanlist)

            Console.WriteLine("Sinusoidal Waveform data (in Volts):")

            'Display results
            For i = 0 To dResult.Length - 1
                Console.Write("{0:E2}" & vbTab, dResult(i))
            Next


            ' Turn off output switch
            For i = 1 To iNumberOfChannels
                driver.Outputs2.Item2(driver.Outputs2.Name(i)).Enabled = False
            Next

            ' Check instrument for errors.
            Dim errorCode As Integer = -1
            Dim errorMsg As String = String.Empty
            Console.WriteLine()

            Do
                driver.Utility.ErrorQuery(errorCode, errorMsg)
                Console.WriteLine("ErrorQuery: {0}, {1}", errorCode, errorMsg)
            Loop While errorCode <> 0

        Catch err As System.Exception
            Console.WriteLine()
            Console.WriteLine("Exception Error:")
            Console.WriteLine("  " + err.Message())
        End Try

        ' Close driver if initialized.
        If (driver.Initialized) Then
            driver.Close()
            Console.WriteLine("Driver Closed")
        End If

        Console.WriteLine()
        Console.Write("Done - Press Enter to Exit ")
        Console.ReadLine()

    End Sub

End Module
