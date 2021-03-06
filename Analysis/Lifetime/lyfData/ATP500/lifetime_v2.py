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
files = glob.glob('MStates_Ts0.**.txt')
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
    #act_xy = np.around( ms_act[['im','c','xm','ym']], 6).values.tolist()
    #def_xy = np.around( ms_def[['im','c','xm','ym']], 6).values.tolist()

    ms_act = ms_act.drop(['ts','mt','xc','yc','zc','zm','fx','fy','fz'],1) # remove the unused columns
    ms_act = ms_act.groupby(ms_act.columns.tolist(), as_index=False).size() # count duplicated rows
    ms_act.rename(columns={'size':'lyf'}, inplace=True)

    ms_def = ms_def.drop(['ts','mt','xc','yc','zc','zm','fx','fy','fz'],1)
    ms_def = ms_def.groupby(ms_def.columns.tolist(), as_index=False).size()
    ms_def.rename(columns={'size':'lyf'}, inplace=True)

    #==============================================================
   
    #==============================================================
    ms_act.to_csv('actLyf'+r[7:-4]+'.csv', header=False, index=False, float_format='%.6f') # x,y,life
    #-------------------------------------------------------------- 
    try: 
        ms_def.to_csv('defLyf'+r[7:-4]+'.csv', header=False, index=False, float_format='%.6f') # x,y,life
    except:
        print('Saving m2 passed: '+r) # No defective motors in R =1.0
    
