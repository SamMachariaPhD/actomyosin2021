# Python 2 -- pvpython
# Find Filament, Specie1, Specie2, MotorSpecie1, and MotorSpecie2 .vtk files (Assay time steps)
# Get the clean points (exact location) plottable in matplotlib
# Save the points as .csv files
# Regards, Sam Macharia

import os, glob, csv, sys
from paraview.simple import *
import numpy as np

paraview.simple._DisableFirstRenderCameraReset()

current_path = os.getcwd()
flmt = 'Filament_'
mtr1 = 'Specie1_'
mtr2 = 'Specie2_'
mtsp1 = 'MotorSpecie1_'
mtsp2 = 'MotorSpecie2_'
Fcount = 0
M1count = 0
M2count = 0
Mt1count = 0
Mt2count = 0
rc = 0
seed = 't5S77'

r = [0.70,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.0]
r_precision = 2

#dirlist = ['R0.8B13.0ATP2000.0MD3000.0']
dirlist = glob.glob(current_path+'/*/') # comment out this if only using the above one folder
dirlist = sorted(dirlist, key=lambda x:x[-28:]) # comment out this one also if only using the above one folder

for i in dirlist:
    os.chdir(i); print(i)
    #==================================================
    filament_list = glob.glob('Filament_A001T**.vtk') # os.listdir()
    filaments = sorted(filament_list, key=lambda x:x[-11:])
    fnos = len(filaments)
    specie1_list = glob.glob('IntSpecie1_A001T**.vtk') 
    specie1 = sorted(specie1_list, key=lambda x:x[-11:])
    s1nos = len(specie1)
    specie2_list = glob.glob('IntSpecie2_A001T**.vtk') 
    specie2 = sorted(specie2_list, key=lambda x:x[-11:])
    s2nos = len(specie2)
    motor1_list = glob.glob('MotorSpecie1_A001T**.vtk') 
    motor1 = sorted(motor1_list, key=lambda x:x[-11:])
    m1nos = len(motor1)
    motor2_list = glob.glob('MotorSpecie2_A001T**.vtk') 
    motor2 = sorted(motor2_list, key=lambda x:x[-11:])
    m2nos = len(motor2)
    #=====================================================
    if fnos == s1nos == s2nos == m1nos == m2nos:
        print('Number of files = %s'%fnos)
        for i in filaments:
            f = LegacyVTKReader(FileNames=[i]) # create a new 'Legacy VTK Reader'
            try:
                os.remove(flmt+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Fcount,1))+'.csv')
                print('Deleted: '+flmt+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Fcount,1))+'.csv')
            except(OSError, RuntimeError, TypeError, NameError):
                pass
            SaveData(flmt+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Fcount,1))+'.csv', proxy=f, Precision=6)
            print('Saved: '+flmt+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Fcount,1))+'.csv')
            Fcount = Fcount+1
        for j in specie1:
            m1 = LegacyVTKReader(FileNames=[j])
            try:
                os.remove(mtr1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M1count,1))+'.csv')
                print('Deleted: '+mtr1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M1count,1))+'.csv')
            except(OSError, RuntimeError, TypeError, NameError):
                pass
            SaveData(mtr1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M1count,1))+'.csv', proxy=m1, Precision=6)
            print('Saved: '+mtr1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M1count,1))+'.csv')
            M1count = M1count+1
        for k in specie2:
            m2 = LegacyVTKReader(FileNames=[k])
            try:
                os.remove(mtr2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M2count,1))+'.csv')
                print('Deleted: '+mtr2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M2count,1))+'.csv')
            except(OSError, RuntimeError, TypeError, NameError):
                pass
            SaveData(mtr2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M2count,1))+'.csv', proxy=m2, Precision=6)
            print('Saved: '+mtr2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(M2count,1))+'.csv')
            M2count = M2count+1
        for l in motor1:
            mt1 = LegacyVTKReader(FileNames=[l])
            try:
                os.remove(mtsp1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt1count,1))+'.csv')
                print('Deleted: '+mtsp1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt1count,1))+'.csv')
            except(OSError, RuntimeError, TypeError, NameError):
                pass
            SaveData(mtsp1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt1count,1))+'.csv', proxy=mt1, Precision=6)
            print('Saved: '+mtsp1+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt1count,1))+'.csv')
            Mt1count = Mt1count+1
        for m in motor2:
            mt2 = LegacyVTKReader(FileNames=[m])
            try:
                os.remove(mtsp2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt2count,1))+'.csv')
                print('Deleted: '+mtsp2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt2count,1))+'.csv')
            except(OSError, RuntimeError, TypeError, NameError):
                pass
            SaveData(mtsp2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt2count,1))+'.csv', proxy=mt2, Precision=6)
            print('Saved: '+mtsp2+seed+'R'+str(np.round(r[rc],r_precision))+'Ts'+str(np.round(Mt2count,1))+'.csv')
            Mt2count = Mt2count+1
    else:
        sys.exit('Error! The number of files are different!')

    rc+=1
    Fcount = 0
    M1count = 0
    M2count = 0
    Mt1count = 0
    Mt2count = 0


