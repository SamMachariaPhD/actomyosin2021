"""
Go inside various complete simulation data.
Get persistence length.
Regards, Sam Macharia
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, glob, csv, io, sys
import scipy.stats as stats
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

current_path = os.getcwd()
filename = 'v9Lp_std213s5F6pN'
DtFile=0.01
#filename1 = 'bmAc'
#filename2 = 'bminAc'

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)

    #bmAc = pd.read_csv(filename1+'.csv', names=['bm'])
    #bminAc = pd.read_csv(filename2+'.csv', names=['bm'])
    Ds = pd.read_csv('Ds.csv',names=['s','Ds'])

    t10h1 = int(np.around(Ds.shape[0]*0.1,0))
    t20h1 = int(np.around(Ds.shape[0]*0.2,0))
    Ds1_10th = Ds[0:t10h1]
    Ds1_20th = Ds[0:t20h1]

    Ds2 = Ds.drop(Ds.index[0])
    Ds2 = Ds2.reset_index(drop=True)
    t10h2 = int(np.around(Ds2.shape[0]*0.1,0))
    t20h2 = int(np.around(Ds2.shape[0]*0.2,0))
    Ds2_10th = Ds2[0:t10h2]
    Ds2_20th = Ds2[0:t20h2]
    #Ds2_20th=======================================================================
    xf = np.array(Ds2_20th['s'], dtype=float) #transform your data in a numpy array of floats 
    yf = np.array(Ds2_20th['Ds'], dtype=float) #so the curve_fit can work
    #curve function
    def func(xf, Lp):
        return np.exp(-xf/(2*Lp))
    #curve fit
    popt, pcov = curve_fit(func, xf, yf)

    os.chdir(current_path)
    with open(filename+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow([np.around(popt[0],8)])
