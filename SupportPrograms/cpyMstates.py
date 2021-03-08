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
change = [70, 80, 90, 94, 98] # 0.1 # change in the variable
name = 'MotorStates_Ts0.001_S273T5R0.'
count = 0

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-18:]) # name folders with equal no of figures e.g. 001,010,100,... not 1,10,100

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(fileName,current_path+'/'+str(name)+str(change[count])+'.txt')
    count+=1
