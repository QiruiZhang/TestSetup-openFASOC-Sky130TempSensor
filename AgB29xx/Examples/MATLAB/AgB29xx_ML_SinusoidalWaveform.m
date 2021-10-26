	% Agilent IVI-COM Driver Example Program
	% 
	% Creates a driver object, reads a few Identity interface
	% properties, and checks the instrument error queue.
	% May include additional instrument specific functionality.
	% 
	% See driver help topic "Programming with the IVI-COM Driver in Various Development Environments"
	% for additional programming information.
	%
	% Runs in simulation mode without an instrument.

disp(blanks(1)');
disp('  ML_SinusoidalWaveform');
try
    
    % Create driver instance
    driver = instrument.driver.AgB29xx();

    % Edit resource and options as needed.  Resource is ignored if option Simulate=true
    resourceDesc = 'GPIB0::23::INSTR';    
    % resourceDesc = 'TCPIP0::<host_name or IP addr>::INSTR';

    initOptions = 'QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false';			
    idquery = true;
    reset   = true;

    driver.Initialize(resourceDesc, idquery, reset, initOptions);
    disp('Driver Initialized');

    % Print a few IIviDriver.Identity properties
    disp(['Identifier:      ', driver.Identity.Identifier]);
    disp(['Revision:        ', driver.Identity.Revision]);
    disp(['Vendor:          ', driver.Identity.Vendor]);
    disp(['Description:     ', driver.Identity.Description]);
    disp(['InstrumentModel: ', driver.Identity.InstrumentModel]);
    disp(['FirmwareRev:     ', driver.Identity.InstrumentFirmwareRevision]);
    disp(['Serial #:        ', driver.DeviceSpecific.System.SerialNumber]);
    simulate = driver.DriverOperation.Simulate;
    if simulate == true
		disp(blanks(1));
        disp('Simulate:        True');
    else
        disp('Simulate:        False');
    end
    disp(blanks(1));
        
    iNumberOfChannels = driver.DeviceSpecific.Outputs2.Count;  
    strModel = driver.Identity.InstrumentModel;
         
    for i = 1:iNumberOfChannels
        
         %Set sinusoidal voltage waveform
         %Configure Function Mode: Voltage
         driver.DeviceSpecific.Outputs2.Item2(driver.DeviceSpecific.Outputs2.Name(i)).Type = 1;
        
         if(strcmp(strModel,'B2961A') ||strcmp(strModel,'B2961B')||strcmp(strModel,'B2962A') ||strcmp(strModel,'B2962B'))
         %Configure Voltage Mode to Arbitrary Waveform
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).ArbitraryWaveform.ConfigureMode(1);
         
         %Set Arbitrary Waveform Shape to Sinusoidal
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).ArbitraryWaveform.Shape = 2;
         
         %Set Sinusoid Amplitude
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Amplitude = 1.0;
         
         %Set Sinusoid Frequency
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).ArbitraryWaveform.Voltage.Sinusoid.Frequency = 1.0;         
         end
         %Set sampling voltage measurement
         %Set measurement function to Voltage         
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Function.SetEnabled(1)
         
         %Set number of power line cycles (NPLC)
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Current2.NPLC = 0.1;
         
         %Set the Compliance value (Current Protection)
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Current2.ComplianceValue = 0.1;
         
         %Generate triggers
         %Set Transient Trigger count: 1
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).Trigger.Count = 1;
         
         %Set Trigger source
         driver.DeviceSpecific.Transients2.Item2(driver.DeviceSpecific.Transients2.Name(i)).Trigger.Source = 17;
         
         %Set Measurement Trigger count: 100
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Trigger.Count = 100;
         
         %Set Measurement Trigger source: Timer
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Trigger.Source = 19;
         
         %Set Measurement interval - Timer Trigger source
         driver.DeviceSpecific.Measurements2.Item2(driver.DeviceSpecific.Measurements2.Name(i)).Trigger.Timer = 0.01;
                          
        % Turn on output switch
        driver.DeviceSpecific.Outputs2.Item2(driver.DeviceSpecific.Outputs2.Name(i)).Enabled = true;
    end

    % Measure  
    if iNumberOfChannels == 1
        chanlist = '1';
    else
        chanlist = '1,2';
    end
    driver.DeviceSpecific.Trigger.Initiate(chanlist);    
   
    %Sleep 2 secs
    pause (2);
    
    % Query Results    
    dResult = driver.DeviceSpecific.Measurements.FetchArrayData(5, chanlist);
    disp('Sinusoidal Waveform data (in Volts):');
    
    for i = 1:length(dResult)
        %str = sprintf('%2.2e\t',dResult(i));
        %disp(str);
        disp(dResult(i));
    end    
   
    % Turn off output switch  
     for i = 1:iNumberOfChannels
        driver.DeviceSpecific.Outputs2.Item2(driver.DeviceSpecific.Outputs2.Name(i)).Enabled = false;       
    end
    
    %Sleep 1 secs
    pause (1);
				
    % Check instrument for errors
    errorNum = -1;
    errorMsg = ('');
    disp(blanks(1)');
    while (errorNum ~= 0)
    	[errorNum, errorMsg] = driver.Utility.ErrorQuery();
    	disp(['ErrorQuery: ', num2str(errorNum), ', ', errorMsg]);
    end

catch exception
    disp(getReport(exception));
end

if driver.Initialized
    driver.Close();
    disp('Driver Closed');
end

disp('Done');
disp(blanks(1)');

