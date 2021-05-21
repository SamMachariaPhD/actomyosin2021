# Go inside various folders.
# Get the IntParticle.vtk.
# Extract binding active and defective myosins.
# Regards, Sam.

import os, glob, csv
import pandas as pd
import numpy as np

current_path = os.getcwd()

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

name = 'R1B13S'
lst = [14,15,17,21,26,27,30,37,42,43,33,77]
c = 0

for i in dirlist:
    os.chdir(i); print(i)
    filename1 = 'bmAct_'+name+str(round(lst[c],0))
    filename2 = 'bmDef_'+name+str(round(lst[c],0))

    active_list = glob.glob('IntSpecie1**.vtk') 
    active = sorted(active_list, key=lambda x:x[-11:])
    defective_list = glob.glob('IntSpecie2**.vtk') 
    defective = sorted(defective_list, key=lambda x:x[-11:])

    try:
        os.remove(filename1+'.csv')
        os.remove(filename2+'.csv')
    except(OSError, RuntimeError, TypeError, NameError):
        pass

    for j in active:
        motor_noA = pd.read_csv(j, delim_whitespace=True)
        extractA = motor_noA.iloc[3:4,1:2].values
        extractA = int(np.int_(extractA))
        rowElementA = [str(extractA)]
        os.chdir(current_path)
        with open(filename1+'.csv','a') as fd:
            writer = csv.writer(fd)
            writer.writerow(rowElementA)
        os.chdir(i)
            
    for k in defective:
        motor_noI = pd.read_csv(k, delim_whitespace=True)
        extractI = motor_noI.iloc[3:4,1:2].values
        extractI = int(np.int_(extractI))
        rowElementI = [str(extractI)]
        os.chdir(current_path)
        with open(filename2+'.csv','a') as fd:
            writer = csv.writer(fd)
            writer.writerow(rowElementI)
        os.chdir(i)
    c+=1
