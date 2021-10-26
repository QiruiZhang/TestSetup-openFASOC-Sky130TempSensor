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
disp('  ML_StairCaseSweep');
try
    
    % Create driver instance
    driver = instrument.driver.AgB29xx();

    % Edit resource and options as needed.  Resource is ignored if option Simulate=true
    resourceDesc = 'GPIB0::23::INSTR';
    % resourceDesc = 'TCPIP0::<host_name or IP addr>::INSTR';

    initOptions = 'QueryInstrStatus=true, Simulate=true, DriverSetup= Model=, Trace=false';			
    idquery = true;
    reset   = true;

    driver.DeviceSpecific.Initialize(resourceDesc, idquery, reset, initOptions);
    disp('Driver Initialized');

    % Print a few IIvidriver.DeviceSpecific.DeviceSpecific.Identity properties
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

    iNumberOfChannels = driver.DeviceSpecific.Outputs.Count;   
    
    for i = 1:iNumberOfChannels
        
        % Set voltage sweep outputs (-5V to 5V, 11 steps)
        driver.DeviceSpecific.Transients.Item(driver.DeviceSpecific.Transients.Name(i)).Voltage.Mode = 2;
        driver.DeviceSpecific.Transients.Item(driver.DeviceSpecific.Transients.Name(i)).Voltage.Start = -5.0;
        driver.DeviceSpecific.Transients.Item(driver.DeviceSpecific.Transients.Name(i)).Voltage.Stop = +5.0;
        driver.DeviceSpecific.Transients.Item(driver.DeviceSpecific.Transients.Name(i)).Voltage.SweepPoints = 11;
        
        driver.DeviceSpecific.Outputs.Item(driver.DeviceSpecific.Outputs.Name(i)).Voltage.AutoRangeEnabled = false;
        driver.DeviceSpecific.Outputs.Item(driver.DeviceSpecific.Outputs.Name(i)).Voltage.Range = 20.0;
        driver.DeviceSpecific.Outputs.Item(driver.DeviceSpecific.Outputs.Name(i)).Voltage.Level = 0.0;
        
        % Set auto-range current measurement
        strModel = driver.Identity.InstrumentModel;
        if(strcmp(strModel,'B2901A') ||strcmp(strModel,'B2902A')||strcmp(strModel,'B2911A') ||strcmp(strModel,'B2912A') || strcmp(strModel,'B2901B') ||strcmp(strModel,'B2902B')||strcmp(strModel,'B2911B') ||strcmp(strModel,'B2912B'))
            driver.DeviceSpecific.Measurements.Item(driver.DeviceSpecific.Measurements.Name(i)).Current.AutoRangeEnabled = true;
        end
        driver.DeviceSpecific.Measurements.Item(driver.DeviceSpecific.Measurements.Name(i)).Current.NPLC = 0.1;
        
        % Set trigger condition
        
        %trigger.TriggerCount = 11;
        driver.DeviceSpecific.Transients.Item(driver.DeviceSpecific.Transients.Name(i)).Trigger.Count = 11;
        driver.DeviceSpecific.Measurements.Item(driver.DeviceSpecific.Measurements.Name(i)).Trigger.Count = 11;
        
        % Turn on output switch
        driver.DeviceSpecific.Outputs.Item(driver.DeviceSpecific.Outputs.Name(i)).Enabled = true;
    end
    
    % Measure
    %
    if iNumberOfChannels == 1
        chanlist = '1';
    else
        chanlist = '1,2';
    end
    driver.DeviceSpecific.Trigger.Initiate(chanlist);
    
    %
    % Query Results
    
    dResult = driver.DeviceSpecific.Measurements.FetchArrayData(0, '(@1,2)');
    disp('Staircase sweep data:');
    for i = 1:length(dResult)
        str = sprintf('Item[%d] = %d',i,dResult(i));
        disp(str);
    end
    
    %
    % Turn off output switch
    %
    for i = 1:iNumberOfChannels
        
        driver.DeviceSpecific.Outputs.Item(driver.DeviceSpecific.Outputs.Name(i)).Enabled = false;
    end 

				
    % Check instrument for errors
    errorNum = -1;
    errorMsg = ('');
    disp(blanks(1)');
    while (errorNum ~= 0)
    	[errorNum, errorMsg] = driver.DeviceSpecific.Utility.ErrorQuery();
    	disp(['ErrorQuery: ', num2str(errorNum), ', ', errorMsg]);
    end

catch exception
    disp(getReport(exception));
end

if driver.DeviceSpecific.Initialized
    driver.DeviceSpecific.Close();
    disp('Driver Closed');
end

disp('Done');
disp(blanks(1)');

