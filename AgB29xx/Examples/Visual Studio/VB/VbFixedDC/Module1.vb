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

        Console.WriteLine("  VB_FixedDC")
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
            Dim str As String
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


            ' driver specific tasks...
            Dim iNumberOfChannels As Integer
            iNumberOfChannels = driver.Outputs.Count

            Str = driver.Identity.InstrumentModel

            Dim i As Integer
            For i = 1 To iNumberOfChannels

                ' Set voltage output to 2.0V
                driver.Outputs.Item(driver.Outputs.Name(i)).Voltage.AutoRangeEnabled = False
                driver.Outputs.Item(driver.Outputs.Name(i)).Voltage.Range = 20.0
                driver.Outputs.Item(driver.Outputs.Name(i)).Voltage.Level = 2.0
                driver.Outputs.Item(driver.Outputs.Name(i)).Voltage.TriggeredLevel = 2.0

                ' Set auto-range current measurement
                If (String.Equals(str, "B2901A") Or String.Equals(str, "B2902A") Or String.Equals(str, "B2911A") Or String.Equals(str, "B2912A") Or String.Equals(str, "B2901B") Or String.Equals(str, "B2902B") Or String.Equals(str, "B2911B") Or String.Equals(str, "B2912B")) Then
                    driver.Measurements.Item(driver.Measurements.Name(i)).Current.AutoRangeEnabled = True 'Supported Models for this property: B2901A|B, B2902A|B, B2911A|B, B2912A|B
                End If

                driver.Measurements.Item(driver.Measurements.Name(i)).Current.NPLC = 0.1

                ' Turn on output switch

                driver.Outputs.Item(driver.Outputs.Name(i)).Enabled = True

            Next


            ' Measure

            Dim chanlist As String

            If (iNumberOfChannels = 1) Then
                chanlist = "1"
            Else
                chanlist = "1,2"
            End If

            driver.Trigger.Initiate(chanlist)


            ' Query Results

            Dim dResult As Double()
            dResult = driver.Measurements.FetchArrayData(Agilent.AgB29xx.Interop.AgB29xxMeasurementFetchTypeEnum.AgB29xxMeasurementFetchTypeCurrent, chanlist)

            Console.WriteLine("Fixed DC data:")

            For i = 0 To dResult.Length - 1
                Console.WriteLine("Item [{0}]: {1}", i, dResult(i))
            Next


            ' Turn off output switch
            For i = 1 To iNumberOfChannels
                driver.Outputs.Item(driver.Outputs.Name(i)).Enabled = False
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
