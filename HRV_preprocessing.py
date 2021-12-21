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
    nni = tools.nn_intervals(r_peaks)
    r_peaks_plot = [x+31158 for x in r_peaks]                                   # 31158 is a random number now, needs to be adjusted to the starting index of the ECG after NaN removal
    
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
        plt.title("Data loaded from MIMIC III Database")
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage [mV]')
        plt.legend()
        
    return dataframe, r_peaks, nni