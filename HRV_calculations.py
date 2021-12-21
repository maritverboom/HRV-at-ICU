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

def hrv_results(r_peaks, sampling_rate):
    """
    Function that uses pyHRV toolbox to calculate HRV values
    """
    
    # Time domain
    results_td = td.time_domain(rpeaks=r_peaks, sampling_rate=sampling_rate, plot=True)
    
    # Frequency domain
    results_fd = fd.frequency_domain(rpeaks=r_peaks, sampling_rate=sampling_rate, show=False)
    
    return results_td, results_fd