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
    - batch_nni_first: list containing arrays with nni per included patient 
      [ms], before ectopic beat- and outlier removal
    - batch_rpeaks: list containing arrays with rpeak locations [s]
    - batch_rpeaks_first: list containing array with rpeak locations [s]-
      before ectopic beat- and outlier removal

Output file: the output file is stored in the same folder as the current file.
    - HRVparameters.csv: file containing all calculated HRV parameters per 
      included patient. Rows = patients, columns = HRV parameters
"""
#%% Required modules
import HRV_batchmode as workflow
import HRV_evaluation as viseval

#%% HRV calculations    

# Specify input variables
patient_ids = 'files_id.txt'                                                    # .txt file containing patient_IDs
sampfreq = 125                                                                  # Sample frequency in Hertz [Hz]
lead = 'II'                                                                     # ECG lead to analyze 
starttime = 0                                                                   # Starting time of analysis [s]
endtime  = 3600                                                                 # Ending time of analysis [s]

# HRV calculations for all patients specified in patient_ids
batch_df, batch_nni_first, batch_rpeaks_first, batch_nni, batch_rpeaks, export_all = workflow.workflow_batch(patient_ids,
                                                                         sampfreq, lead, starttime, endtime)

#%% Visual evaluation 
   
viseval.visual_evaluation_rpeaks(batch_df, batch_rpeaks)                        # Visual evaluation of R-peak detection             
viseval.visual_evaluation_nni(batch_nni, batch_rpeaks, batch_nni_first,         # Visual evaluation of NNI correction
                              batch_rpeaks_first)                                                 
                                                               
#%% 



    




