# -*- coding: utf-8 -*-
"""
Created on Feb 23 2024

@author: hjoca
"""

import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog
from os import path

# Select file window
root = tk.Tk()
filename = filedialog.askopenfilenames(parent=root,
                                       filetypes=[('NumPy Binary', '*.npz')],
                                       title='Choose an NPZ File')
root.withdraw()

if filename is None:
    sys.exit('No file selected!')
    
for fn in filename:
    # Open file and Select channels
    data = np.load(fn)
    export = np.column_stack((data['xaxis'],data['signal']))
    
    csvheader = ['Frequency', 'Amplitude']
    csvheader = ','.join(csvheader)
    csvpath = path.dirname(fn)
    csvfile = path.basename(fn)
    csvfile = path.splitext(csvfile)
    csvfile = csvfile[0] + '_Trace.csv'
    csvfile = csvpath + '/' + csvfile

    np.savetxt(csvfile,export,delimiter=',', header=csvheader,fmt='%1.3f')
