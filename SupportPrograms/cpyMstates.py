"""
Go inside various complete simulation data.
Search for bm*.csv
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np

current_path = os.getcwd()
fileName = 'MotorStates_A001.txt'
change = [0.10, 0.20, 0.30, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00] # 0.1 # change in the variable
name = 'MStates_Ts0.0005_S77T5R'
count = 0

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:]) # name folders with equal no of figures e.g. 001,010,100,... not 1,10,100

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(fileName,current_path+'/'+str(name)+str(format(change[count],'.2f'))+'.txt')
    count+=1
