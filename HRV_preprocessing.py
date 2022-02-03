# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 08:46:15 2021

@author: marit
"""

# Basic import
import pandas as pd
import numpy as np


# Signals toolbox
import biosppy
import pyhrv.tools as tools


# Visuals
import matplotlib.pyplot as plt


# import the WFDB(WaveFormDataBase) package
import wfdb


def load_data(patient_id, sampling_rate, sampfrom, sampto, lead='II'):
    """
    Function to load data from MIMIC-III database.
    
    INPUT:
        analysistype: 'single' or 'batch'
            single: analaysis of single ECG file
            batch: analysis of all ECG files in folder
        sampling_rate:
        sampfrom: starting sample [seconds]
        sampto: last sample [seconds]
        lead: 'I', 'II', 'V'
            default = 'II'
        
    OUTPUT:
        ECG = DataFrame containing all ECG records (single or multiple)
            Rows: ECG trace
            Colums: Datapoints
    """
    pt_id = patient_id
    sampling_rate = sampling_rate
    Sampfrom = sampling_rate * sampfrom                                         # The starting sample number to read for all channels
    Sampto = sampling_rate * sampto                                             # The sample number at which to stop reading for all channels
    LeadWanted = [lead]                                                         # Lead that is used for the analysis
    record = wfdb.rdrecord(pt_id[-7:], sampfrom = Sampfrom, sampto = Sampto, 
                           pn_dir=('mimic3wdb/'+pt_id), channel_names =
                           LeadWanted)
    return record

def ecg_dataframe(record):
    """
    INPUT:
        record
    OUTPUT:
        time axis
        plot
    """   
    t = np.linspace(0, record.sig_len, record.sig_len)                          # Length of signal                      
    time = pd.DataFrame(t)                                                      # Create dataframe for plotting
    time.columns = ['Time']                                                     # Change name of column to 'Time'
    ecg_df = time.assign(ecg_signal = pd.DataFrame(record.p_signal))            # Add ECG signal to dataframe
    
    #NaN removal
    index = np.arange(0, ecg_df.ecg_signal.first_valid_index(), 1)
    ecg_df=ecg_df.drop(labels=index, axis=0)        
    ecg_df = ecg_df.fillna(0)
    ecg_df.Time = ecg_df.Time/125                                               # Time axis in seconds (125 Hz)
        
    return ecg_df
           

def ecg_rpeak(ecg_df, sampling_rate):
    """
    Function that uses bioSPPY toolbox in order to filter the ECG signal and
    detect R-peaks
    """
    dataframe = ecg_df
    ecg_filtered, r_peaks = biosppy.signals.ecg.ecg(dataframe.ecg_signal, 125, 
                                                    show=False)[1:3]             # [1:3] To get filtered signal and R-peaks
    dataframe = dataframe.assign(ecg_filtered = ecg_filtered)                   # Add filtered ECG signal to dataframe
    r_peaks =  r_peaks * 1/sampling_rate                                        # Convert from index to time in seconds
    nni = tools.nn_intervals(r_peaks)
                
    return dataframe, r_peaks, nni

def ecg_ectopic_removal(r_peaks, nni):
    "Function for the removal of outliers and ectopic beats"
    nni_new = np.delete(nni, [np.where(nni < 300)])     # HR > 200 bpm
    nni_new = np.delete(nni, [np.where(nni > 6000)])    # HR < 30 bpm

    # Ectopic beat removal 
    # If an ectopic beat occurs, two values of the NNI series will be ~half of the
    # 'mean' NN interval. 
    n = np.arange(1, len(nni), 1)[10:-5]
    nni_true = nni_new.copy()
    rrn = r_peaks[:-1]
    rrn_true = rrn.copy()
    index = []

    for i in n:
        if nni[i] < 0.75*(np.mean(nni[i-11:i-1])):
            if nni[i+1] < 0.75*(np.mean(nni[i-11:i-1])):
                if nni[i+2] > 0.75*(np.mean(nni[i-11:i-1])):
                    nni_true[i] = np.median(nni[i-11:i-1])
                    #rrn_true[i] = rrn_true[i-1] + nni_true[i]/1000
                    index = index + [i+1]
        #if nni[i] > 1.15*(np.mean(nni[i-11:i-1])):
        #    if nni[i+1] < 0.85*(np.mean(nni[i-11:i-1])):
        #        if nni[i+2] > 0.75 * (np.mean(nni[i-11:i-1])):
        #            nni_true[i] = np.median(nni[i-11:i-1])
        #            rrn_true[i] = rrn_true[i-1] + nni_true[i]/1000
        #            index = index + [i+1]
        if nni[i] < 0.85*(np.mean(nni[i-11:i-1])):
            if nni[i+1] > 1.15*(np.mean(nni[i-11:i-1])):
                if nni[i+2] > 0.75 * (np.mean(nni[i-11:i-1])):
                    nni_true[i] = np.median(nni[i-11:i-1])
                    rrn_true[i] = rrn_true[i-1] + nni_true[i]/1000
                    index = index + [i+1]            
        if nni[i] > 1.20*(np.mean(nni[i-11:i-1])) or nni[i] < 0.8*(np.mean(nni[i-11:i-1])):
            nni_true[i] = np.median(nni[i-11:i-1])

    nni_true = np.delete(nni_true, index)
    rrn_true = np.delete(rrn_true, index)
    
    return rrn_true, nni_true