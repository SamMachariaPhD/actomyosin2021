#Take intParticle and MotorSpecie1 in each case
#Calculate how many motors are active out of the total binding motors
#Confirm that the output shape is as expected
#Regards, Sam Macharia

import os, glob, csv, time, sys
import numpy as np
import pandas as pd
import numpy_indexed as npi

current_path = os.getcwd()
task = 0
filename = 'AbM'
R = 0.1 
seed = '673ATP50'

dirlist = glob.glob(current_path+'/*/')
dirlist = sorted(dirlist, key=lambda x:x[-25:])

for i in dirlist:
    os.chdir(i)
    #print(i)
    intParticleLst = glob.glob('IntParticle**.vtk') # os.listdir()
    srtdIntParticle = sorted(intParticleLst, key=lambda x:x[-11:])
    intMotorSpecieLst = glob.glob('MotorSpecie1**.vtk') # os.listdir()
    srtdMotorSpecie = sorted(intMotorSpecieLst, key=lambda x:x[-11:])
    if len(srtdIntParticle) != len(srtdMotorSpecie):
        sys.exit("intParticle files != MotorSpecie files!")
    tic = time.time()
    for j in range(0, len(srtdIntParticle)):
        #print(srtdIntParticle[j])
        #print(srtdMotorSpecie[j])
        intParticle = pd.read_csv(srtdIntParticle[j], delim_whitespace=True, names=['x','y','z','nan','nan2'], low_memory=False)
        motorno = intParticle.iloc[4:5,1:2].values
        motorNo = int( np.int_(motorno) )

        intParticle = intParticle.drop(['z','nan','nan2'], axis=1)
        intParticl = intParticle.drop(intParticle.index[motorNo+5:intParticle.index[-1]+1])
        intPartic = intParticl.drop(intParticl.index[0:5])
        intPartic = intPartic.values
        bindingTotal = intPartic.astype(float)

        MotorSpecie1 = pd.read_csv(srtdMotorSpecie[j], delim_whitespace=True, names=['x','y','z','nan','nan2'], low_memory=False)
        Sp1no = MotorSpecie1.iloc[4:5,1:2].values
        Sp1No = int( np.int_(Sp1no) )

        MotorSpecie1_ = MotorSpecie1.drop(['z','nan','nan2'], axis=1)
        MotorSpecie1_ = MotorSpecie1_.drop(MotorSpecie1_.index[Sp1No+5:MotorSpecie1_.index[-1]+1])
        MotorSpecie1_ = MotorSpecie1_.drop(MotorSpecie1_.index[0:5])
        MotorSpecie1_ = MotorSpecie1_.values
        activeSpecie = MotorSpecie1_.astype(float)

        activeM = np.sum(1*npi.contains(bindingTotal,activeSpecie))

        os.chdir(current_path)
        with open(filename+seed+'R'+str(np.round(R,1))+'.csv','a') as fd:
            writer = csv.writer(fd)
            #print("Total = %s, Active = %s" %(motorNo, activeM))
            if activeM <= motorNo:
                writer.writerow([activeM])
            elif activeM > motorNo:
                sys.exit("Active motors cannot be > Total motors")
            else: # can be improved to capture the exact value
                writer.writerow([0])
        os.chdir(i)
    toc = time.time(); tym = toc-tic
    R += 0.1
    task += 1
    print("File %s took %d sec." %(task, tym))