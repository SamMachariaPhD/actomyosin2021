"""
Go inside various complete simulation data.
Search for binding motors.
Output binding ratio of active and defective myosin
Regards, Sam Macharia
"""

import os, glob, csv
import numpy as np
import pandas as pd

current_path = os.getcwd()
filename = 'BM_ratio_std27s5kBT0042'
DtFile=0.01
filename1 = 'bmAc'
filename2 = 'bminAc'

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)

    bmAc = pd.read_csv(filename1+'.csv', names=['bm'])
    bminAc = pd.read_csv(filename2+'.csv', names=['bm'])

    # mu1 = bmAc['bm'].mean()
    # sigma1 = np.std(bmAc['bm'])
    # mu2 = bminAc['bm'].mean()
    # sigma2 = np.std(bminAc['bm'])

    mu1_ = bmAc['bm']/(bmAc['bm'] + bminAc['bm'])
    mu1 = mu1_.mean()
    sigma1 = np.std(mu1_)
    mu2_ = bminAc['bm']/(bmAc['bm'] + bminAc['bm'])
    mu2 = mu2_.mean()
    sigma2 = np.std(mu2_)

    os.chdir(current_path)
    with open(filename+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow((mu1,sigma1,mu2,sigma2))
