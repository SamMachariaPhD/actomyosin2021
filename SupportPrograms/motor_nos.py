"""
Go inside various complete simulation data.
Search for MotorSpecie1 or 2 _A001T***.vtk
Extract total motor number
Regards, Sam Macharia
"""

import os, glob, csv
import numpy as np
import pandas as pd

current_path = os.getcwd()
filename = 'MS1_no_'
r = 0.8
seed = '113'

dirlist = ['R0.8B13.0ATP2000.0MD3000.0']
#dirlist = glob.glob(current_path+'/*/')
#dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)
    file_list = glob.glob('MotorSpecie1_A001T**.vtk') # os.listdir()
    files = sorted(file_list, key=lambda x:x[-11:])
    for j in files:
        print(j)
        motor_no = pd.read_csv(j, delim_whitespace=True)
        extract = motor_no.iloc[3:4,1:2].values
        extract = int(np.int_(extract))
        rowElement = [str(extract)]
        os.chdir(current_path)
        with open(filename+seed+'R'+str(np.round(r,1))+'.csv','a') as fd:
            writer = csv.writer(fd)
            writer.writerow(rowElement)
        os.chdir(i)
    r=r+0.1
