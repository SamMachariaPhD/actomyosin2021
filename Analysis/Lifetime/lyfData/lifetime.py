# Load motor states
# Output lifetime data
# Regards, Sam Macharia
#==============================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import glob

#==============================================================
files = glob.glob('MotorStates_Ts0.**.txt')
files = sorted(files, key=lambda x:x[-20:])

#==============================================================
columns = ['ts','im','mt','c','xc','yc','zc','xm','ym','zm','fx','fy','fz'] 
# ts = timestep, im = motor index, mt = motor type (active = 1, defective = 2)
# c = contact  state, xc|yc|zc = binding motor head position, xm|ym|zm = binding motor root position 
# fx|fy|fz = xyz motor force at the root??

for r in files:
    print(r)
    ms = pd.read_csv(r, names=columns, delim_whitespace=True)

    #==============================================================
    # Separate active motor and defective binding motors.
    ms_act = ms[ms.mt == 1]
    ms_act = ms_act.reset_index(drop=True)
    ms_def = ms[ms.mt == 2]
    ms_def = ms_def.reset_index(drop=True)

    #==============================================================
    # Lifetime metric: during one lifetime, a binding motor, ( 𝑥𝑚,𝑦𝑚 ) must retain index ' 𝑖𝑚 ', 
    # and also contact state, ' 𝑐 ' in the next immediate time step ' 𝑡𝑠 '.
    act_xy = np.around( ms_act[['im','c','xm','ym']], 6).values.tolist()
    def_xy = np.around( ms_def[['im','c','xm','ym']], 6).values.tolist()

    #==============================================================
    m1lyf = {}
    for i in act_xy:
        if str(i) not in m1lyf:
            m1lyf[str(i)]=1 # approximate all binding motors to have a lifetime of 1
        else:
            m1lyf[str(i)] += 1
    #--------------------------------------------------------------        
    m2lyf = {}
    for i in def_xy:
        if str(i) not in m2lyf:
            m2lyf[str(i)]=1
        else:
            m2lyf[str(i)] += 1

    #==============================================================
    m1lyftym = np.fromiter(m1lyf.values(), dtype=int) # pick dictionary values
    m1lyf_Ag = pd.DataFrame({'life':m1lyftym}) # make pandas dataframe
    # Make a nice list from the dictionary keys.
    m1lyf_lst = []
    for i in list(m1lyf.keys()):
        m1lyf_lst.append(literal_eval(i))
    m1lyf_lst = np.array(m1lyf_lst) # nice list
    #--------------------------------------------------------------   
    m2lyftym = np.fromiter(m2lyf.values(), dtype=int) # pick dictionary values
    m2lyf_Ag = pd.DataFrame({'life':m2lyftym}) # make pandas dataframe
    # Make a nice list from the dictionary keys.
    m2lyf_lst = []
    for i in list(m2lyf.keys()):
        m2lyf_lst.append(literal_eval(i))
    m2lyf_lst = np.array(m2lyf_lst) # nice list

    #==============================================================
    m1Ag_mtr = pd.DataFrame({'xp':m1lyf_lst[:,2], 'yp':m1lyf_lst[:,3]}) # pandas dataframe of aggressive binding m1
    m1Aglyf = pd.concat([m1Ag_mtr,m1lyf_Ag], axis=1)
    #m1Aglyf = m1Aglyf[m1Aglyf.life > 0]  
    m1Aglyf.to_csv(r[12:-4]+'act_with_lyf.csv', header=False, index=False) # x,y,life
    #-------------------------------------------------------------- 
    try: 
        m2Ag_mtr = pd.DataFrame({'xp':m2lyf_lst[:,2], 'yp':m2lyf_lst[:,3]}) # pandas dataframe of aggressive binding m2
        m2Aglyf = pd.concat([m2Ag_mtr,m2lyf_Ag], axis=1)
        #m2Aglyf = m2Aglyf[m2Aglyf.life > 0]
        m2Aglyf.to_csv(r[12:-4]+'def_with_lyf.csv', header=False, index=False) # x,y,life
    except:
        print('Saving m2 passed: '+r) # No defective motors in R =1.0
    
