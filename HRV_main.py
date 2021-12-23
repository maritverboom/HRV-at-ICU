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
   
    # Write calculated parameters to excel sheet
    writer = pd.ExcelWriter('HRV parameters.xlsx', engine = 'xlsxwriter')
    export_td.to_excel(writer, sheet_name='Time Domain')
    export_fd.to_excel(writer, sheet_name='Frequency Domain')
    #export_nl.to_excel(writer, sheet_name='Non Linear')
    #export_temp.to_excel(writer, sheet_name='Temp')
    writer.save()
    
    return batch_dataframes, batch_rpeaks, batch_td, batch_nni, export_td
    

#%% Final calculations    
batch_df, batch_r, batch_td, batch_nni, export_td = workflow_batch('files_id.txt')

                         


