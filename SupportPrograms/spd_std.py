"""
Go inside various complete simulation data.
Search for conformation file.
Compute the Head and Tail mean speeds and the standard deviations, and return the dataframe thereof.
Regards, Sam Macharia
"""

import os, glob, csv
import numpy as np
import pandas as pd

current_path = os.getcwd()
filename = 'spd_std273'
dt = 0.01
dt01 = 0.1

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-28:])

for i in dirlist:
    os.chdir(i); print(i)
    #-------------------------------------------------
    conf = pd.read_csv('Conformation_A001.txt', names=['time','x','y','z'], delim_whitespace=True)
    #-------------------------------------------------
    Head = conf.iloc[0::13,:]
    Head = Head.reset_index(drop=True)
    Head01 = Head.iloc[0::10,:]
    Head01 = Head01.reset_index(drop=True)

    dxHead = np.diff(Head['x'])
    dyHead = np.diff(Head['y'])
    dxHead01 = np.diff(Head01['x'])
    dyHead01 = np.diff(Head01['y'])

    distHead = np.sqrt((dxHead**2)+(dyHead**2))
    spdHead = distHead/(1*dt)
    avSpdHead = np.mean(spdHead)
    distHead01 = np.sqrt((dxHead01**2)+(dyHead01**2))
    spdHead01 = distHead01/(10*dt)
    avSpdHead01 = np.mean(spdHead01)

    stdHead = np.sum(((spdHead-avSpdHead)**2)/(np.size(spdHead)-1))
    stdHead = np.sqrt(stdHead)
    stdHead01 = np.sum(((spdHead01-avSpdHead01)**2)/(np.size(spdHead01)-1))
    stdHead01 = np.sqrt(stdHead01)
    #-------------------------------------------------
    Tail = conf.iloc[12::13,:]
    Tail = Tail.reset_index(drop=True)
    Tail01 = Tail.iloc[0::10,:]
    Tail01 = Tail01.reset_index(drop=True)

    dxTail = np.diff(Tail['x'])
    dyTail = np.diff(Tail['y'])
    dxTail01 = np.diff(Tail01['x'])
    dyTail01 = np.diff(Tail01['y'])

    distTail = np.sqrt((dxTail**2)+(dyTail**2))
    spdTail = distTail/(1*dt)
    avSpdTail = np.mean(spdTail)
    distTail01 = np.sqrt((dxTail01**2)+(dyTail01**2))
    spdTail01 = distTail01/(10*dt)
    avSpdTail01 = np.mean(spdTail01)

    stdTail = np.sum(((spdTail-avSpdTail)**2)/(np.size(spdTail)-1))
    stdTail = np.sqrt(stdTail)
    stdTail01 = np.sum(((spdTail01-avSpdTail01)**2)/(np.size(spdTail01)-1))
    stdTail01 = np.sqrt(stdTail01)
    #-------------------------------------------------
    os.chdir(current_path)
    with open(filename+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow((avSpdHead,stdHead,avSpdHead01,stdHead01,avSpdTail,stdTail,avSpdTail01,stdTail01))
