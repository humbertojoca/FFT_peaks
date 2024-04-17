#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon 06 10:56:33 2023

@author: hjoca
"""

import sys,csv
import numpy as np
import tkinter as tk
from os import path
from tkinter import filedialog

root = tk.Tk()

# Open Files
filename = filedialog.askopenfilenames(parent=root,filetypes=[('Numpy compressed file','*.npz')],title='Choose an Data File')
root.withdraw()

if filename == None:
   sys.exit('No file selected!')

# Average multiple FFT from individual files
l = 0 # Line number
flist = []
Av_data = np.zeros((len(filename),6)) # Pre-allocate Matrix
for fn in filename:
    flist += [path.basename(fn)]
    data = np.load(fn)['data']        # Get analyzed data 
    Av_data[l,:] = data 
    l += 1                  # Increase line number

# Average contraction/transients from all selected files
Av_mean = np.nanmean(Av_data, axis=0)     # Calculate Mean 
Av_std = np.nanstd(Av_data, axis=0) # Calculate Std. Deviation 
Av_n = Av_data.shape[0]                     # Calculate N
Av_sem = Av_std/np.sqrt(Av_n)                            # Calculate S.E.M 

# Export averaged data to .csv file
csvheader = ['NPeaks', 'First', 'Second', 'Third', 'THD','SL','File']
#csvheader = ','.join(csvheader)
csvpath = path.dirname(fn)

# Select output file
csvfile = filedialog.asksaveasfilename(parent=root,initialdir=csvpath,filetypes=[('Comma-separated values','*.csv')],defaultextension=".csv",title='Save Output File')

if csvfile == None:
   sys.exit('No file selected!')

# Add individual data to csv file
with open(csvfile,'w',newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(csvheader)
    for fi in range(Av_data.shape[0]):
        row = list(Av_data[fi])
        row.append(flist[fi])
        writer.writerow(row)
# Add Mean/Std/SEM data to csv file
    writer.writerow('')
    np.savetxt(file,[Av_mean],delimiter=',',header='Mean',fmt='%1.3f')
    np.savetxt(file,[Av_std],delimiter=',',header='Stantard Deviation',fmt='%1.3f')
    np.savetxt(file,[Av_sem],delimiter=',',header='S.E.M',fmt='%1.3f')
