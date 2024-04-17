# -*- coding: utf-8 -*-
"""
Created on Jun 3 2023

@author: hjoca
"""

import sys
import math
import pims
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import peakutils
from tkinter import filedialog
from os import path
from pp_style import pps_xy
from scipy import signal


# Image Parameters
fs = 9.2308
show_images = True  # True or False
export_csv = True  # True or False

# Select file window
root = tk.Tk()
filename = filedialog.askopenfilenames(parent=root,
                                       filetypes=[('TIFF Image', '*.tif')],
                                       title='Choose an TIFF Image')
root.withdraw()

if filename is None:
    sys.exit('No file selected!')

for fn in filename:
    # Open file and Select channels
    image = pims.open(fn)
    fshift = np.fft.fftshift(image[0]) # Shift zero to center
    fcorrected = np.log10(abs(fshift)) # Absolute number - Log transform
    
    profile = np.mean(fcorrected[:,240:270],1) # Select center of FFT
    fprofile = signal.savgol_filter(profile, 5, 3)  # Smooth vector
    hprofile = fprofile[(int(fprofile.size/2)-1):(fprofile.size-1)] # Select only half of the spectrum
    fvector = np.linspace(0,fs/2,hprofile.size) # create a frequency vector
    pkt = peakutils.indexes(hprofile[10:125], thres=0.30, min_dist=20)+10 # Detect Peaks
    f_index = fvector[pkt]
    baseline = np.zeros((pkt.size)) # Calculate an baseline for each harmonic
    for x in range(pkt.size):
        if x < pkt.size-1:
            baseline[x] = hprofile[pkt[x]:pkt[x+1]].min()
            continue
        baseline[x] = baseline[x-1]
        
    amplitude = hprofile[pkt] - baseline
    thd = math.sqrt(amplitude[1]**2 + amplitude[2]**2) / amplitude[0] # Total harmonic distortion
    fft_data = np.array([amplitude.size,amplitude[0],amplitude[1],amplitude[2],thd,1/f_index[0]])
    
    if show_images:
        plt.figure(figsize=(16, 5), constrained_layout=True)
        plt.imshow(fcorrected, cmap="gray") # Show FFT
        
        plt.figure(figsize=(16, 5), constrained_layout=True)
        plt.plot(fvector,hprofile)
        plt.plot(f_index,amplitude+baseline,marker='o',
                 color='r', fillstyle='none', linestyle='none')
        plt.xlabel('Spacial Frequency um-1')
        plt.ylabel('Amplitude')
        pps_xy()
    

    if export_csv:
        # Export analyzed data to .csv
        csvheader = ['NPeaks', 'First', 'Second', 'Third', 'THD','SL']
        csvheader = ','.join(csvheader)
        csvpath = path.dirname(fn)
        csvfile = path.basename(fn)
        csvfile = path.splitext(csvfile)
        npzfile = csvfile[0] + '.npz'
        csvfile = csvfile[0] + '.csv'
        npzfile = csvpath + '/' + npzfile
        csvfile = csvpath + '/' + csvfile
        
        
                
        np.savez_compressed(npzfile,signal=hprofile,xaxis=fvector,data=fft_data,sampling=fs,csvheader=csvheader)
        np.savetxt(csvfile,[fft_data],delimiter=',', header=csvheader,fmt='%1.3f')