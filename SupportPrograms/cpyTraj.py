"""
Go inside various complete simulation data.
Search for TipXY***.txt
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np

current_path = os.getcwd()
filename = 'TipXY_A001.txt'
c = 0
name = 't5S77R'
change = [0.70,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.0]

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-18:])

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(filename,current_path+'/'+'TipXY'+name+str(np.round(change[c],2))+'.txt')
    c+=1
