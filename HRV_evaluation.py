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
