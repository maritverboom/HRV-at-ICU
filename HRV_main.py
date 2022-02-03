# -*- coding: utf-8 -*-
"""
HRV analysis
Created: 10/2021 - 02/2022
Python v3.8
Author: M. Verboom

Basic algorithm for heart rate variability (HRV) analysis. This script was 
written during a Technical Medicine year 2 internship (TM2). The purpose of the
algorithm is to analyze the HRV of ICU patients. Further improvements include:
    - Adding timestamps to the outputfile in order to be able to analyze
      circadian rhythms
    - Improving artefact detection

Make sure the following files are stored in the same folder before running:
    - HRV_main.py
    - HRV_preprocessing.py
    - HRV_calculations.py
    - HRV_batchmode.py
    - files_id.txt
    
Output variables: 
    - batch_df: list containing dataframes with timestamps, raw- and filtered
      ECG signals per included patient
    - batch_nni: list containing arrays with nni per included patient [ms]
    - batch_rpeaks: list containing arrays with rpeak locations [s]

Output file: the output file is stored in the same folder as the current file.
    - HRVparameters.csv: file containing all calculated HRV parameters per 
      included patient. Rows = patients, columns = HRV parameters
"""
#%% Required modules
# Basic import
import numpy as np

# Visuals
import matplotlib.pyplot as plt

# import workflow
import HRV_batchmode as workflow

#%% HRV calculations    

# Specify input variables
patient_ids = 'files_id_test.txt'                                               # .txt file containing patient_IDs
sampfreq = 125                                                                  # Sample frequency in Hertz [Hz]
lead = 'II'                                                                     # ECG lead to analyze 
starttime = 0                                                                   # Starting time of analysis [s]
endtime  = 3600                                                                 # Ending time of analysis [s]

# HRV calculations for all patients specified in patient_ids
batch_df, batch_nni, batch_rpeaks, export_all = workflow.workflow_batch(patient_ids,
                                                                         sampfreq, lead, starttime, endtime)

#%% Evaluation of R-peak detection after ectopic beat removal

def visual_evaluation():
    for i in np.arange(0, len(batch_df), 1):
        dataset = batch_df[i]
        data = dataset.ecg_signal
        time = dataset.Time
        time = [x-time.iloc[0] for x in time]
        rpiek = batch_rpeaks[i]
    
        plt.figure()
        plt.plot(time, data)
        for i in np.arange(0, len(rpiek), 1):
            plt.axvline(rpiek[i], color = 'm')
            plt.xlabel('Time [s]', fontsize = 15)
            plt.ylabel('Amplitude [mV]', fontsize = 15) 
    
visual_evaluation()                                                           
    
#%% Spreiding data
#histtd = pd.read_csv('timedomain.csv')
#hist = histtd.hist()
#histfd = pd.read_csv('frequencydomain.csv')
#hist = histfd.hist()




    




