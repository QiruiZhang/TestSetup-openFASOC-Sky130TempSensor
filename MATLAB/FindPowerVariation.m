clc; clear all;
TZiK = 273.15; scale = 1;
% Load and pre-process power and resolution data
LoadPowerRes;
% Load Tested Frequency Data
LoadFreqData;
    % How good we want the performance to be
inacc_th    = 2.5;
Nc_B        = 8;
    % Polynomial SEC Order
order_sec = 3;

% Explore temp range
tstart_ind  = 5; % 0C
twin_len    = 12; % 0C + 120C = 120C
pcalib      = 1; % +/- 10C calibration
    % Explore the best designs out of 64
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

% Calculate FoMs
freq_arr_20C = freq_data_array(7, :, :);
    % Calculate resolution type-1
freq_pres1_arr_20C = freq_arr_20C + res_data_array(1, :, :);
freq_nres1_arr_20C = freq_arr_20C - res_data_array(1, :, :);
T_pres1_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_pres1_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_pres1_arr_20C)));
T_nres1_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_nres1_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_nres1_arr_20C)));
T_res1_arr_20C = (T_pres1_arr_20C - T_nres1_arr_20C) / 2;
    % Calculate resolution type-2
freq_pres2_arr_20C = freq_arr_20C + res_data_array(2, :, :);
freq_nres2_arr_20C = freq_arr_20C - res_data_array(2, :, :);
T_pres2_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_pres2_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_pres2_arr_20C)));
T_nres2_arr_20C = abs((scale .* TZiK .* params_arr(1, :, :) .* log(freq_nres2_arr_20C) + params_arr(2, :, :)) ./ (1 - scale .* params_arr(1, :, :) .* log(freq_nres2_arr_20C)));
T_res2_arr_20C = (T_pres2_arr_20C - T_nres2_arr_20C) / 2;
    % Calculate type-1 FoM for all
FoM_data_array = EnC_data_array(1, :, :) .* (T_res1_arr_20C .^ 2) * 1e3; % pJ * K^2
FoM2_data_array = EnC_data_array(2, :, :) .* (T_res2_arr_20C .^ 2); % nJ * K^2
FoM_B_arr = zeros(1, Nc_B, 64); FoM2_B_arr = zeros(1, Nc_B, 64); power_B_arr = zeros(1, Nc_B, 64);
T_res1_B_arr = zeros(1, Nc_B); T_res2_B_arr = zeros(1, Nc_B, 64); EnC_B_arr = zeros(1, Nc_B, 64);
for d = 1:64
    FoM_B_arr(1, :, d) = FoM_data_array(1, indlist_B_arr(1, :, d), d);
    FoM2_B_arr(1, :, d) = FoM2_data_array(1, indlist_B_arr(1, :, d), d);
    power_B_arr(1, :, d) = power_data_array(1, indlist_B_arr(1, :, d), d);
    T_res1_B_arr(1, :, d) = T_res1_arr_20C(1, indlist_B_arr(1, :, d), d);
    T_res2_B_arr(1, :, d) = T_res2_arr_20C(1, indlist_B_arr(1, :, d), d);
    EnC_B_arr(1, :, d) = EnC_data_array(1, indlist_B_arr(1, :, d), d);
end

err_th = 5.0;
SelectedInst_A = [];
for d = 1:32
    % Only plot designs with a reasonable inaccuracy
    if (inacc_B_arr(1, d) < err_th)
        power_list = [];
        [~, sorted_ind] = sort(power_B_arr(1, :, d));
        for i = 1:Nc_B
            if (FoM2_B_arr(1, sorted_ind(i), d) > 0)
                power_list = [power_list, power_B_arr(1, sorted_ind(i), d)];
            end
        end
        % Remove the min and max powers
        %power_list = power_list(2:(length(power_list)-1));
        mean_power = mean(power_list);
        max_power_var = (max(power_list) - mean_power)/mean_power;
        min_power_var = abs(min(power_list) - mean_power)/mean_power;
        SelectedInst_A = [SelectedInst_A, [d; max_power_var; min_power_var]];
    end
end
AvgPowerVar_A = max(mean(SelectedInst_A(2, :)), mean(SelectedInst_A(3, :)));

err_th = 5.0;
SelectedInst_B = [];
for d = 33:64
    if (inacc_B_arr(1, d) < err_th)
        power_list = [];
        [~, sorted_ind] = sort(power_B_arr(1, :, d));
        for i = 1:Nc_B
            if (FoM2_B_arr(1, sorted_ind(i), d) > 0)
                power_list = [power_list, power_B_arr(1, sorted_ind(i), d)];
            end
        end
        % Remove the min and max powers
        %power_list = power_list(2:(length(power_list)-1));
        length(power_list)
        mean_power = mean(power_list);
        max_power_var = (max(power_list) - mean_power)/mean_power;
        min_power_var = abs(min(power_list) - mean_power)/mean_power;
        SelectedInst_B = [SelectedInst_B, [d; max_power_var; min_power_var]];
    end
end
AvgPowerVar_B = max(mean(SelectedInst_B(2, :)), mean(SelectedInst_B(3, :)));