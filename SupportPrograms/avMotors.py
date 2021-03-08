"""
Go inside various complete simulation data.
Search for average in/active binding motors.
Regards, Sam Macharia
"""

import os, glob, csv
import numpy as np
import pandas as pd

current_path = os.getcwd()
filename = 'v9mtrs_std273s5F6pN'
DtFile=0.01
filename1 = 'bmAc'
filename2 = 'bminAc'

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)

    bmAc = pd.read_csv(filename1+'.csv', names=['bm'])
    bminAc = pd.read_csv(filename2+'.csv', names=['bm'])

    mu1 = bmAc['bm'].mean()
    sigma1 = np.std(bmAc['bm'])
    mu2 = bminAc['bm'].mean()
    sigma2 = np.std(bminAc['bm'])

    os.chdir(current_path)
    with open(filename+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow((mu1,sigma1,mu2,sigma2))
