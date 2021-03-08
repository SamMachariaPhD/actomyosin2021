# Python 3
# Collect ContactStates... .vtk files
# Get the position of binding motors
# Separate binding active(a) and inactive(i) motor position(pos)
# Sort the points in ascending order
# Save the points as ['apos','ipos'] .csv files
# Regards, Sam Macharia

import os, glob, csv
import numpy as np
import pandas as pd

current_path = os.getcwd()
filename1 = 'ActivePos_'
filename2 = 'InactivePos_'
seed = '5s113'
r = 0.8 
r_precision = 1
count = 0

dirlist = ['R0.8B13ATP2000MD3000S233T3']
dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)
    #=================================================
    cont_list = glob.glob('ContactStates_A001T**.txt') 
    conts = sorted(cont_list, key=lambda x:x[-11:])
    print('ContactState files = %s'%len(conts))
    #=================================================
    for i in conts:
        print(i)
        #cnt = pd.read_csv(i, names=['mt','cnt'], delim_whitespace=True) # version 1 # comment on thin one
        cnt = pd.read_csv(i, names=['idx','mt','cnt'], delim_whitespace=True) # version 2 
        bm = cnt[cnt.cnt>0.0001] # get binding motors -- from dataframe cnt, pick column 'cnt' > 0.0001
        #bmA = bm[bm['mt']%10 == 1] # get the binding active motors -- the last value is 1 # version 1 # comment on this one
        bmA = bm[bm['mt'] == 1] # get the binding active motors -- the last value is 1 # version 2 
        bmAs = bmA.sort_values(by='cnt',ascending=True) # sort to ascending order ---> ['apos']
        blankIndex=['']*len(bmAs['cnt'])
        bmAs['cnt'].index = blankIndex # ---> ['apos'] only without index
        bmAs = bmAs['cnt'].values # remove name and dtype foot text
        #================================================================
        #bmI = bm[bm['mt']%10 == 2] # get the binding inactive motors -- the last value is 2 # version 1
        bmI = bm[bm['mt'] == 2] # get the binding inactive motors -- the last value is 2 # version 2
        bmIs = bmI.sort_values(by='cnt',ascending=True) # sort to ascending order ---> ['ipos']
        blankIndex=['']*len(bmIs['cnt'])
        bmIs['cnt'].index = blankIndex # ---> ['ipos'] only without index
        bmIs = bmIs['cnt'].values # remove name and dtype foot text
        #================================================================
        try:
            os.remove(filename1+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
            print('Deleted: '+filename1+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
            os.remove(filename2+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
            print('Deleted: '+filename2+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
        except(OSError, RuntimeError, TypeError, NameError):
            pass
        np.savetxt(filename1+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv', bmAs.T, fmt='%.5f')
        print('Saved: '+filename1+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
        np.savetxt(filename2+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv', bmIs.T, fmt='%.5f')
        print('Saved: '+filename2+seed+'R'+str(np.round(r,r_precision))+'Ts'+str(np.round(count,1))+'.csv')
        count += 1
    r += 0.1
    count = 0
