# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 08:49:37 2021

@author: marit
"""

import numpy as np
import pandas as pd

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
    nndif = td.nni_differences_parameters(nni=nni)                                # n of interval differences, mean, min and max of nn interval differences
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
    results_fd = fd.frequency_domain(nni=nni, sampling_rate=sampling_rate, 
                                     show=False)
    
    return results_td, results_fd