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

def workflow_batch(patient_ids, sampfreq):
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
    batch_nni = list()
    batch_all = list()

    sampling_rate = sampfreq
    
    # Read .txt file containing patient IDs
    with open(pt_ids) as f:                                                     
        lines = [x.strip() for x in list(f) if x]

    # For every patient ID
    for line in lines:
        ecg = preproc.load_data(line, sampling_rate, 0, 3600, 'II')
        ecg_df = preproc.ecg_dataframe(ecg)
        ecg_df, r_peaks, nni = preproc.ecg_rpeak(ecg_df, sampling_rate)
        r_peaks, nni = preproc.ecg_ectopic_removal(r_peaks, nni)
        hrv_td, hrv_fd, hrv_nl = hrvcalc.hrv_results(nni=nni, sampling_rate=125)
        hrv_all = pyhrv.utils.join_tuples(hrv_td, hrv_fd, hrv_nl)
        
        batch_dataframes.append(ecg_df)
        batch_rpeaks.append(r_peaks)
        batch_nni.append(nni)
        batch_all.append(hrv_all)
        
    # Exportfile
    tuplekeys_all = batch_all[0].keys()
    matrix_all = []
            
    for key in tuplekeys_all:
        matrix_all += [batch_all[0][key]]    
         
    matrix_all = np.array(matrix_all)
    
    for i in range(1,len(batch_all)):
        stack = []
        
        for key in tuplekeys_all:
            stack += [batch_all[i][key]]
            
        stack = np.array(stack)
        matrix_all = np.vstack((matrix_all, stack))
            
    export_all = pd.DataFrame(matrix_all, index=lines, columns=tuplekeys_all)
    
    # Write calculated parameters to .csv file
    export_all.to_csv('HRVparameters.csv')
        
    return batch_dataframes, batch_rpeaks, batch_nni, batch_all, export_all
    

#%% Final calculations    
batch_df, batch_r, batch_nni, batch_all, export_all = workflow_batch('files_id_test.txt',
                                                                     sampfreq=125)

#%% Evaluation of R-peak detection after ectopic beat removal

def visual_evaluation():
    for i in np.arange(0, len(batch_df), 1):
        dataset = batch_df[i]
        data = dataset.ecg_signal
        time = dataset.Time
        time = [x-time.iloc[0] for x in time]
        rpiek = batch_r[i]
    
        plt.figure()
        plt.plot(time, data)
        for i in np.arange(0, len(rpiek), 1):
            plt.axvline(rpiek[i], color = 'm')
            plt.xlabel('Time [s]', fontsize = 15)
            plt.ylabel('Amplitude [mV]', fontsize = 15) 
    
#visual_evaluation()                                                            # Uncommend and run cell in case of visual evaluation of R-peak detection
    
#%% Spreiding data
#histtd = pd.read_csv('timedomain.csv')
#hist = histtd.hist()
#histfd = pd.read_csv('frequencydomain.csv')
#hist = histfd.hist()




    




