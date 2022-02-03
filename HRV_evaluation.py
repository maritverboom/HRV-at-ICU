# -*- coding: utf-8 -*-
"""
HRV analysis
Created: 10/2021 - 02/2022
Python v3.8
Author: M. Verboom
"""

#%% Required modules
import numpy as np
import matplotlib.pyplot as plt

#%% Visual evaluation of R peaks
def visual_evaluation_rpeaks(batch_df, batch_rpeaks):
    """
    Function that creates a plot for the visual evaluation of R-peak detection.
    The plot that is created shows the raw ECG signal with all detected R-peaks
    by the algorithm. 
    
    INPUT:
        batch_df: list containing dataframes with raw ecg,
                          filtered ecg and time of all patients
        batch_rpeaks: list containing all locations of r-peaks for all 
                      patients [s]   
    
    OUTPUT:
        plot with raw ECG signal and detected R-peaks
    """
    
    
    for i in np.arange(0, len(batch_df), 1):
        dataset = batch_df[i]
        data = dataset.ecg_signal
        time = dataset.Time
        time = [x-time.iloc[0] for x in time]
        rpiek = batch_rpeaks[i]
    
        plt.figure()
        plt.plot(time, data, 'c', label='Raw ECG signal')
        plt.axvline(rpiek[1], color='m', label='Detected R-peaks')
        plt.xlabel('Time [s]', fontsize = 15)
        plt.ylabel('Amplitude [mV]', fontsize = 15) 
        plt.legend(loc=2, prop={'size': 20})
        for i in np.arange(0, len(rpiek), 1):
            plt.axvline(rpiek[i], color = 'm')
        
#%% Visual evalation of NNI series

def visual_evaluation_nni(batch_nni, batch_rpeaks, batch_nni_first, batch_rpeaks_first):
    """
    Function that creates a plot for the visual evaluation of NNI correction.
    The plot that is created shows the NNI series before and after removal of
    ectopic beats and outliers. 
    
    INPUT:
        batch_nni: list containing arrays with nni per included patient [ms]
        batch_nni_first: list containing arrays with nni per included patient 
                         [ms], before ectopic beat- and outlier removal
        batch_rpeaks: list containing arrays with rpeak locations [s]
        batch_rpeaks_first: list containing array with rpeak locations [s]-
                            before ectopic beat- and outlier removal
    
    OUTPUT:
        plot with NNI series before and after ectopic beat- and outlier removal
    """
    
    for i in np.arange(0, len(batch_nni), 1):
        rpeak = batch_rpeaks[i]
        rpeak_first = batch_rpeaks_first[i]
        nni = batch_nni[i]
        nni_first = batch_nni_first[i]
        plt.figure()
        plt.plot(rpeak_first[:-1], nni_first, 'm-o', label='Before ectopic beat removal')
        plt.plot(rpeak, nni, 'c-o', label='After ectopic beat removal')
        plt.xlabel('Time of R-peak [s]', fontsize=20)
        plt.ylabel('NNI [ms]', fontsize=20)
        plt.legend(loc=2, prop={'size': 20})
