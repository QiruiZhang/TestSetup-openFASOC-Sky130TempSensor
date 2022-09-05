clc; clear all;
TZiK = 273.15; scale = 1;

% Load Tested Frequency Data
LoadFreqData;

% Set the temperature range here
% Temperature starts from -40C with a step of 10C
% [0C, 120C] in this example. 
tstart_ind  = 5; % 0C
twin_len    = 12; % 0C + 120C = 120C
pcalib      = 1; % +/- 10C calibration. Trim points are 10C and 110C.

% For each of the 64 designs, you may want to get an average inaccuracy out
% of the 15 tested chips. But not all the 15 chips are good - many of them
% can be not working for a particular design. Thus you want to select the
% chips that have sane inaccuracy and then use them to calculate the
% average inaccuracy of a design for the model file. Here two methods are
% provided for reference. You are more than welcome to come up with other
% methods that may better serve this purpose.

% Chip-selection method A: Tolerable upper limit for raw/pre-SEC Maximum Absolute Error (MAE). 
% If using this method for selection of chips:
% For each sensor design, only the chips with MAE lower than this limit
% are selected. The chip indices and corresponding MAEs are stored in 
% "indlist_A_arr". Indices ranges from 1 to 15 (10 ~ 24 in the MeasResults folder).
inacc_th    = 5; % Tolerable upper limit for MAE is 5C.

% Chip-selection method B: Number of best chips wanted
% If using this metric for selection of chips:
% For each sensor design, the MAEs of chips are sorted, then the chips with
% the smallest MAEs are selected. E.g., for Nc_B = 5, the first five chips
% in the sorted list are selected. The chip indices and corresponding MAEs
% are stored in "indlist_B_arr".
Nc_B        = 5; % Only use the five chips with smallest MAEs.

% Polynomial SEC Order
order_sec = 3;

% Calculate inaccuracies
% Raw/Pre-SEC inaccuracies are stored in "inacc_arr".
% Post-SEC inaccuracies are stored in "inacc_arr_sec".
% For now, EvalDesignGivenRange() already implemented chip selection 
% method A and B for the raw inaccuracies. 
% You may also try applying the above two chip selection methods to the
% post-SEC inaccuracies, through modifying EvalDesignGivenRange().
fprintf("Generate metrics for the given range......\n");
params_arr = zeros(2, Nchip, 64);
inacc_arr  = zeros(Ntemp, Nchip, 64);
params_sec_arr = zeros(order_sec + 1, 64);
inacc_arr_sec = zeros(Ntemp, Nchip, 64);
Nc_A_arr = zeros(1, 64);
indlist_A_arr = zeros(2, Nchip, 64);
inacc_B_arr = zeros(1, 64);
indlist_B_arr = zeros(2, Nc_B, 64);
for design = 1:64
    freq_arr = freq_data_array(:, :, design);
    [params, inacc, params_sec, inacc_sec, Nc_A, indlist_A, inacc_B, indlist_B] = ...
        EvalDesignGivenRange(freq_arr, tlist, tstart_ind, twin_len, pcalib, inacc_th, Nc_B, order_sec);    
    params_arr(:, :, design) = params;
    inacc_arr(:, :, design) = inacc;
    params_sec_arr(:, design) = params_sec;
    inacc_arr_sec(:, :, design) = inacc_sec;
    Nc_A_arr(:, design) = Nc_A;
    indlist_A_arr(:, :, design) = indlist_A;
    inacc_B_arr(:, design) = inacc_B;
    indlist_B_arr(:, :, design) = indlist_B;
end



