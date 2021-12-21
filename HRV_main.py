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


#%% Workflow Single mode

def workflow_single(patient_id):
    """
    Function in the case of single patient processing.
    
    INPUT:
        patient_id: ID number of patient from MIMIC-III database
    """
    pt_id = patient_id
    ecg = preproc.load_data(patient_id = pt_id)
    ecg_df = preproc.ecg_dataframe(ecg, 'no')
    ecg_df, r_peaks = preproc.ecg_rpeak(ecg_df, 'no')
    
    return ecg_df, r_peaks


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
        hrv_td, hrv_fd = hrvcalc.hrv_results(r_peaks=r_peaks, sampling_rate=125)
        
        batch_dataframes.append(ecg_df)
        batch_rpeaks.append(r_peaks)
        batch_nni.append(nni)
        batch_td.append(hrv_td)
        batch_fd.append(hrv_fd)
        
    return batch_dataframes, batch_rpeaks, batch_td, batch_fd, batch_nni
    

#%% Final calculations    
batch_df, batch_r, batch_td, batch_fd, batch_nni = workflow_batch('files_id.txt')


#%% HANDIG om inhoud te checken
for key in batch_td[1].keys(): print(key, batch_td[1][key])
for key in batch_fd[1].keys(): print(key, batch_fd[1][key])



        