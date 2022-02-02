# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 08:49:37 2021

@author: marit
"""

# HRV toolbox
import pyhrv
import pyhrv.time_domain as td
import pyhrv.frequency_domain as fd

# biosppy
import biosppy

#%% Created functions

def hrv_results(nni, sampling_rate):
    """
    Function that uses pyHRV toolbox to calculate HRV values
    """
    
    # Time domain parameters
    nnpar = td.nni_parameters(nni=nni)                                           # n of intervals, mean, min and max nn interval
    nndif = td.nni_differences_parameters(nni=nni)                               # n of interval differences, mean, min and max of nn interval differences
    hr = td.hr_parameters(nni=nni)                                               # mean, min, max std of HR
    sdnn = td.sdnn(nni=nni)                                                      # standard deviation of NN interval series
    sdnni = td.sdnn_index(nni=nni, full=False, duration=300, warn=True)          # mean of std of all NN intervals within 5 minute intervals [ms]
    sdann = td.sdann(nni=nni, full=False, overlap=False, duration=300,           # std of the mean nni value of each segment    
                     warn=True)
    rmssd = td.rmssd(nni=nni)                                                    # root mean of square differences of successive NN intervals
    sdsd = td.sdsd(nni=nni)                                                      # std of differences of successive NN intervals
    nn50 = td.nn50(nni=nni)                                                      # NN differences > 50 ms                                              
    triang = td.triangular_index(nni=nni, binsize=7.8125, show=False)                        # triangular index bas on NN interval histogram
    results_td = pyhrv.utils.join_tuples(nnpar, nndif, hr, sdnn, sdnni, sdann, 
                                         rmssd, sdsd, nn50, triang)
       
         
    # Frequency domain
    fbands={'ulf': (0.00, 0.003), 'vlf': (0.003, 0.04), 'lf': (0.04, 0.15), 'hf': (0.15, 0.4)}  
    results = fd.welch_psd(nni=nni, fbands=fbands, show=False, mode='normal')
    abs_ulf = results[2][0]
    abs_vlf = results[2][1]
    abs_lf = results[2][2]
    abs_hf = results[2][3]
    rel_ulf = results[3][0]
    rel_vlf = results[3][1]
    rel_lf = results[3][2]
    rel_hf = results[3][3]
    log_ulf = results[4][0]
    log_vlf = results[4][1]
    log_lf = results[4][2]
    log_hf = results[4][3]
    norm_lf = results[5][0]
    norm_hf = results[5][1]
    ratio_lf_hf = results[6]
    total_power = results[7]
    results_fd = biosppy.utils.ReturnTuple((abs_ulf, abs_vlf, abs_lf, abs_hf, 
                                           rel_ulf, rel_vlf, rel_lf, rel_hf,
                                           log_ulf, log_vlf, log_lf, log_hf,
                                           norm_lf, norm_hf, ratio_lf_hf, total_power), 
                                          ('abs_ulf', 'abs_vlf', 'abs_lf', 'abs_hf', 
                                           'rel_ulf', 'rel_vlf', 'rel_lf', 'rel_hf',
                                           'log_ulf', 'log_vlf', 'log_lf', 'log_hf',
                                           'norm_lf', 'norm_hf',
                                           'ratio_lf_hf', 'total_power'))
    
    # Nonlinear analysis
    poincare = pyhrv.nonlinear.poincare(nni=nni, show=False)
    entropy = pyhrv.nonlinear.sample_entropy(nni)
    dfa = pyhrv.nonlinear.dfa(nni, show=False)
    results_nl = pyhrv.utils.join_tuples(poincare, entropy, dfa)
    
    return results_td, results_fd, results_nl