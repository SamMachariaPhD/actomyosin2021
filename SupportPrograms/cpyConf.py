"""
Go inside various complete simulation data.
Search for Conformation***.txt
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np

current_path = os.getcwd()
filename = 'Conformation_A001.txt'
c = 0
name = 'T5F0S'
change = [21,22,23,24,25]

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-18:])

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(filename,current_path+'/'+'Conf'+name+str(np.round(change[c],2))+'.txt')
    c+=1
