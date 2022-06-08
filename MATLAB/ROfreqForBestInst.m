InstanceNo = 27;
freq_8 = freq_arr_20C(:,:, InstanceNo);
freq_8 = freq_8(indlist_B_arr(1, :, InstanceNo));
freq_avg_20C = mean(freq_8)