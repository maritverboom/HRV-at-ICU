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
    
    # Read .txt file containing patient IDs
    with open(pt_ids) as f:                                                     
        lines = [x.strip() for x in list(f) if x]

    # For every patient ID
    for line in lines:
        ecg = preproc.load_data(patient_id = line)
        ecg_df = preproc.ecg_dataframe(ecg, 'no')
        ecg_df, r_peaks, nni = preproc.ecg_rpeak(ecg_df, 'no')
        r_peaks = r_peaks/125
        nni = nni/125
        hrv_td, hrv_fd = hrvcalc.hrv_results(rpeaks=r_peaks, sampling_rate=125)
        
        batch_dataframes.append(ecg_df)
        batch_rpeaks.append(r_peaks)
        batch_nni.append(nni)
        batch_td.append(hrv_td)
        batch_fd.append(hrv_fd)
        
    # Exportfile
    tuplekeys = batch_td[0].keys()
    matrix_td = []
    
    for key in tuplekeys:
        matrix_td += [batch_td[0][key]]
        
    matrix_td = np.array(matrix_td)
    
    for i in range(1,len(batch_td)):
        stack = []
        
        for key in tuplekeys:
            stack += [batch_td[i][key]]
        
        stack = np.array(stack)
        matrix_td = np.vstack((matrix_td, stack))
            
    export_td = pd.DataFrame(matrix_td.T, index=tuplekeys, columns=lines)       # DataFrame containing all calculated HRV parameters for every patient
        
    return batch_dataframes, batch_rpeaks, batch_td, batch_fd, batch_nni, export_td
    

#%% Final calculations    
batch_df, batch_r, batch_td, batch_fd, batch_nni, export = workflow_batch('files_id.txt')



