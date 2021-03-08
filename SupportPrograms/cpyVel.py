"""
Go inside various complete simulation data.
Search for v.csv in ANALYSIS folder
Copy and paste to some place with a new name.
Regards, Sam Macharia
"""

import os, glob, shutil
import numpy as np
import pandas as pd

current_path = os.getcwd()
file1 = 'v.csv'; # file2 = 'bminAc.csv'
#change = [2,5,7,10] # 0.1 # change in the variable
name = 'velR05-09s5'
#count = 0

DtFile=0.01
columns = ['time', 'x_tip', 'y_tip']
vel = []

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-18:]) # name folders with equal no of figures e.g. 001,010,100,... not 1,10,100

for i in dirlist:
    os.chdir(i); print(i)

    df_load = pd.read_csv('TipXY_A001.txt', names=columns, delim_whitespace=True)
    df_nice = df_load.drop(['time'], axis=1)
    df = df_nice.iloc[0::10, :] #pick every 9th row starting from the first

    Dx_tip = np.diff(df['x_tip']); Dy_tip = np.diff(df['y_tip'])
    DD=np.sqrt((Dx_tip**2)+(Dy_tip**2))
    v=DD/(10*DtFile); #Av_vel = np.mean(v)
    #vSD=np.sum(((v-Av_vel)**2)/(np.size(v)-1)); vSD=np.sqrt(vSD)

    vel.append(v)

    #count+=1

os.chdir(current_path)
vel = np.array(vel)
np.savetxt(name+'.csv', vel.T, delimiter=',')
