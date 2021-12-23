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

def hrv_results(rpeaks, sampling_rate):
    """
    Function that uses pyHRV toolbox to calculate HRV values
    """
    
    # Time domain parameters
    # results_td = list()
    # nnpar = td.nn_parameters(nni)                                               # n of intervals, mean, min and max nn interval
    # nndif = td.nn_differences_parameter()
    # hr = td.hr_parameters()
    # sdnn = td.sdnn()
    # sdnni = td.sdnn_index()
    # rmssd = td.rmssd()
    # sdsd = td.sdsd()
    # nnxx = td.nnXX()
    # triang = td.triangular_index()
    # geom = td.geometrical_parameters()
    # results_td.append(nnpar, nndif, hr, sdnn, sdnni, rmssd, sdsd, nnxx, triang, geom)
    results_td = td.time_domain(rpeaks=rpeaks, sampling_rate=sampling_rate, plot=True)
    
        
    # Frequency domain
    results_fd = fd.frequency_domain(rpeaks=rpeaks, sampling_rate=sampling_rate, show=False)
    
    return results_td, results_fd