"""
Go inside various compiled simulation.
Search for a.out file
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np

current_path = os.getcwd()
filename = 'a.out'
c = 0
name = 'f9.2R'
change = [0.10,0.20,0.30,0.40,0.50,0.60]

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)
    shutil.copy2(filename,current_path+'/'+name+str(np.round(change[c],2))+'.out')
    c+=1
