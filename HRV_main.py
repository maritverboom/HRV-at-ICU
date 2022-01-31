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
import pyhrv.time_domain as td

# Visuals
import matplotlib.pyplot as plt


# import the WFDB(WaveFormDataBase) package
import wfdb
 
import HRV_preprocessing as preproc
import HRV_calculations as hrvcalc


#%% Workflow Batch mode

def workflow_batch(patient_ids):
    """
    Function in the case of batch processing.
    
    INPUT:
        patient_ids: .txt file of patient ID from MIMIC-III database
    
    OUTPUT:
        batch_dataframes: list containing dataframes with raw ecg,
                          filtered ecg and time of all patients
        batch_rpeaks: list containing all locations of r-peaks for all patients
    
    """
    pt_ids = patient_ids
    
    # Create empty lists for storage of dataframes
    batch_dataframes = list()                                                   
    batch_rpeaks = list()
    batch_td = list()
    batch_fd = list()
    batch_nni = list()
   
    
    sampling_rate = 125
    
    # Read .txt file containing patient IDs
    with open(pt_ids) as f:                                                     
        lines = [x.strip() for x in list(f) if x]

    # For every patient ID
    for line in lines:
        ecg = preproc.load_data(patient_id = line)
        ecg_df = preproc.ecg_dataframe(ecg)
        ecg_df, r_peaks, nni = preproc.ecg_rpeak(ecg_df, sampling_rate)
        r_peaks, nni = preproc.ecg_ectopic_removal(r_peaks, nni)
        hrv_td, hrv_fd = hrvcalc.hrv_results(nni=nni, sampling_rate=125)
        
        batch_dataframes.append(ecg_df)
        batch_rpeaks.append(r_peaks)
        batch_nni.append(nni)
        batch_td.append(hrv_td)
        batch_fd.append(hrv_fd)
        
    # Exportfile
    tuplekeys_td = batch_td[0].keys()
    tuplekeys_fd = batch_fd[0].keys()
    matrix_td = []
    matrix_fd = []
    
    for key in tuplekeys_td:
        matrix_td += [batch_td[0][key]]
    
    for key in tuplekeys_fd:
        matrix_fd += [batch_fd[0][key]]
        
    matrix_td = np.array(matrix_td)
    matrix_fd = np.array(matrix_fd)
    
    for i in range(1,len(batch_td)):
        stack = []
        
        for key in tuplekeys_td:
            stack += [batch_td[i][key]]
        
        stack = np.array(stack)
        matrix_td = np.vstack((matrix_td, stack))
    
    for i in range(1,len(batch_fd)):
        stack = []
        
        for key in tuplekeys_fd:
            stack += [batch_fd[i][key]]
        
        stack = np.array(stack)
        matrix_fd = np.vstack((matrix_fd, stack))
            
    export_td = pd.DataFrame(matrix_td.T, index=tuplekeys_td, columns=lines)       # DataFrame containing all calculated HRV parameters for every patient
    export_fd = pd.DataFrame(matrix_fd.T, index=tuplekeys_fd, columns=lines)       # DataFrame containing all calculated HRV parameters for every patient   
    
    # Write calculated parameters to .csv file
    export_td.to_csv('timedomain.csv')
    export_fd.to_csv('frequencydomain.csv')
        
    return batch_dataframes, batch_rpeaks, batch_td, batch_nni, export_td, hrv_td
    

#%% Final calculations    
batch_df, batch_r, batch_td, batch_nni, export_td, hrv_td = workflow_batch('files_id_test.txt')

#%% Evaluation of R-peak detection after ectopic beat removal
for i in np.arange(0, len(batch_df), 1):
    dataset = batch_df[i]
    data = dataset.ecg_signal
    time = dataset.Time
    time = [x-time.iloc[0] for x in time]
    rpiek = batch_r[i]
    
    plt.figure()
    plt.plot(time, data)
    for i in np.arange(0, len(rpiek), 1):
        plt.axvline(rpiek[i], color = 'r')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude [mV]') 
    plt.title('Visual evaluation of R-peak detection')



    




