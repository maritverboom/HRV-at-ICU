# -*- coding: utf-8 -*-
"""
Created on 12-10-2021
Python 3.8
Author: M. Verboom

Basic algorithm for heart rate variability (HRV) analysis
- Hier komt nog meer uitleg, waar je files opgeslagen moeten zijn etc.
"""

# Basic import
import pandas as pd
import numpy as np


# HRV toolbox
import pyhrv
import biosppy

# Visuals
import matplotlib.pyplot as plt


# import the WFDB(WaveFormDataBase) package
import wfdb


#%% Created functions

def load_data(patient_id, lead='II'):
    """
    Function to load data from MIMIC-III database.
    
    INPUT:
        analysistype: 'single' or 'batch'
            single: analaysis of single ECG file
            batch: analysis of all ECG files in folder
        lead: 'I', 'II', 'V'
            default = 'II'
    OUTPUT:
        ECG = DataFrame containing all ECG records (single or multiple)
            Rows: ECG trace
            Colums: Datapoints
    """
    pt_id = patient_id
    x = 0 
    y = 3600
    Sampfrom = 125*x                                                            # The starting sample number to read for all channels
    Sampto = 125*y                                                              # The sample number at which to stop reading for all channels
    LeadWanted = [lead]                                                         # Lead that is used for the analysis
    record = wfdb.rdrecord(pt_id[-7:], sampfrom = Sampfrom, sampto = Sampto, 
                           pn_dir=('mimic3wdb/'+pt_id), channel_names =
                           LeadWanted)
    return record

def ecg_dataframe(record, plot='no'):
    """
    INPUT:
        record
        plot: 'yes', 'no'
            default = 'no'
    OUTPUT:
        time axis
        plot
    """
        
    t = np.linspace(0, record.sig_len, record.sig_len)                          # Length of signal                      
    time = pd.DataFrame(t)                                                      # Create dataframe for plotting
    time.columns = ['Time']                                                     # Change name of column to 'Time'
    ecg_df = time.assign(ecg_signal = pd.DataFrame(record.p_signal))            # Add ECG signal to dataframe
    ecg_df = ecg_df.dropna()                                                    # Drop all rows of NaN values
    ecg_df.Time = ecg_df.Time/125                                               # Time axis in seconds (125 Hz)

    if plot == 'yes':
        plt.figure()
        plt.plot(ecg_df.Time, ecg_df.ecg_signal, label="Raw ECG signal")
        plt.title("Data loaded from MIMIC III Database")
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage [mV]')
        #plt.xlim([3000, 3010])                                                    # Set limit on x-axis
        plt.legend()
              
        plt.show()
        
    return ecg_df
           

def ecg_rpeak(ecg_df, plot='no'):
    """
    Function that uses bioSPPY toolbox in order to filter the ECG signal and
    detect R-peaks
    """
    dataframe = ecg_df
    ecg_filtered, r_peaks = biosppy.signals.ecg.ecg(dataframe.ecg_signal, 125, 
                                                    show=True)[1:3]             # [1:3] To get filtered signal and R-peaks
    dataframe = dataframe.assign(ecg_filtered = ecg_filtered)                   # Add filtered ECG signal to dataframe
    r_peaks_plot = [x+31158 for x in r_peaks]
    
    if plot == 'yes':                                                           # Plot showing raw ECG, filtered ECG and detected R-peaks
        Plot, Axis = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        
        plt.plot(dataframe.Time, dataframe.ecg_filtered, 
                 label="Filtered ECG-signal", color = 'tab:orange')
        plt.plot(dataframe.Time, dataframe.ecg_signal,
                 label="Raw ECG-signal", color = 'tab:blue')
        plt.plot(dataframe.Time[r_peaks_plot], dataframe.ecg_filtered[r_peaks_plot],
                 "x", color = 'g', label="Detected R-peaks") 
        plt.plot(dataframe.Time[r_peaks_plot], dataframe.ecg_signal[r_peaks_plot],
                 "x", color = 'g', label="Detected R-peaks")                       
        #plt.xlim([70, 80]) 
        plt.title("Data loaded from MIMIC III Database")
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage [mV]')
        plt.legend()
        
    return dataframe, r_peaks

def hrv_results(dataframe):
    """
    Function that uses pyHRV toolbox to calculate HRV values
    """
    signal = dataframe.ecg_signal
    results = pyhrv.hrv(signal=signal, show=True, sampling_rate=125)
    return results

#%% Workflow Single mode

def workflow_single(patient_id):
    """
    Function in the case of single patient processing.
    
    INPUT:
        patient_id: ID number of patient from MIMIC-III database
    """
    pt_id = patient_id
    ecg = load_data(patient_id = pt_id)
    ecg_df = ecg_dataframe(ecg, 'yes')
    ecg_df, r_peaks = ecg_rpeak(ecg_df, 'yes')
    
    return ecg_df, r_peaks


#%% Workflow Batch mode

def workflow_batch(patient_ids):
    """
    Function in the case of batch processing.
    """
    batch_dataframes = list()
    batch_rpeaks = list()
    
    pt_ids = patient_ids
    with open(pt_ids) as f:
        lines = [x.strip() for x in list(f) if x]

    for line in lines:
        ecg = load_data(patient_id = line)
        ecg_df = ecg_dataframe(ecg, 'no')
        ecg_df, r_peaks = ecg_rpeak(ecg_df, 'no')
        
        batch_dataframes.append(ecg_df)
        batch_rpeaks.append(r_peaks)
    
    return batch_dataframes, batch_rpeaks


#%% Final calculations    
batch_df, batch_r = workflow_batch('files_id.txt')

    




        