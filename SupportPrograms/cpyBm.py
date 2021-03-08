"""
Go inside various complete simulation data.
Search for bm*.csv
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np

current_path = os.getcwd()
file1 = 'bmAc.csv'; file2 = 'bminAc.csv'
change = [2,5,7,10] # 0.1 # change in the variable
name = 'R09s1'
count = 0

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-18:]) # name folders with equal no of figures e.g. 001,010,100,... not 1,10,100

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(file1,current_path+'/'+'acBm'+'_'+str(name)+'dt'+str(change[count])+'.csv')
    shutil.copy2(file2,current_path+'/'+'defBm'+'_'+str(name)+'dt'+str(change[count])+'.csv')
    count+=1
