# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 08:49:37 2021

@author: marit
"""

# HRV toolbox
import pyhrv
import pyhrv.time_domain as td
import pyhrv.frequency_domain as fd


#%% Created functions

def hrv_results(nni, sampling_rate):
    """
    Function that uses pyHRV toolbox to calculate HRV values
    """
    
    # Time domain parameters
    nnpar = td.nni_parameters(nni=nni)                                           # n of intervals, mean, min and max nn interval
    nndif = td.nni_differences_parameters(nni=nni)                               # n of interval differences, mean, min and max of nn interval differences
    hr = td.hr_parameters(nni=nni)                                               # mean, min, max std of HR
    sdnn = td.sdnn(nni=nni)                                                      # standard deviation of NN interval series
    sdnni = td.sdnn_index(nni=nni, full=False, duration=300, warn=True)          # mean of std of all NN intervals within 5 minute intervals [ms]
    sdann = td.sdann(nni=nni, full=False, overlap=False, duration=300,           # std of the mean nni value of each segment    
                     warn=True)
    rmssd = td.rmssd(nni=nni)                                                    # root mean of square differences of successive NN intervals
    sdsd = td.sdsd(nni=nni)                                                      # std of differences of successive NN intervals
    nn50 = td.nn50(nni=nni)                                                      # NN differences > 50 ms                                              
    triang = td.triangular_index(nni=nni, binsize=7.8125)                        # triangular index bas on NN interval histogram
    results_td = pyhrv.utils.join_tuples(nnpar, nndif, hr, sdnn, sdnni, sdann, 
                                         rmssd, sdsd, nn50, triang)
       
         
    # Frequency domain
    #settings_welch = {'nfft': 2 ** 12, 'detrend': True, 'window': 'hanning'}
    #settings_lomb = {'nfft': 2 ** 8, 'ma_size': 5}
    #settings_ar = {'nfft': 2**12, 'order': 32}
    fbands={'ulf': (0.00, 0.003), 'vlf': (0.003, 0.04), 'lf': (0.04, 0.15), 'hf': (0.15, 0.4)}
    
    #results_fd = fd.frequency_domain(nni=nni, sampling_rate=sampling_rate, 
                                     #fbands=fbands, show=False)
    
    results_fd = fd.welch_psd(nni=nni, fbands=fbands)
    print(results_fd)
    
    return results_td, results_fd