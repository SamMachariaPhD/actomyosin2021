#!/usr/bin/env python
# coding: utf-8
#---------------------------------------------------------------------------------------------
# Input filament, active, and defective motor binding positions
# Describe their binding behaviour
# Regards, Sam Macharia
#---------------------------------------------------------------------------------------------



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval

Ts = 501
segments = 12 # beads = 13
f = []; m1 = []; m2 = []
#---------------------------------------------------------------------------------------------



# Load all actin, active, and defective binding motor data points.
for i in range(Ts):
    #f_ = pd.read_csv('Filament_5s133R0.8Ts'+str(i)+'.csv', names=['x','y','z'], skiprows=1)
    #f.append(f_)
    m1_ = pd.read_csv('Specie1_5s133R0.8Ts'+str(i)+'.csv', names=['x','y','z'], skiprows=1)
    m1.append(m1_)
    m2_ = pd.read_csv('Specie2_5s133R0.8Ts'+str(i)+'.csv', names=['x','y','z'], skiprows=1)
    m2.append(m2_)
#---------------------------------------------------------------------------------------------



# Combine all binding motor time steps into one dataframe for easier analysis.
m1all = m1[0].drop(['z'], axis=1)
m2all = m2[0].drop(['z'], axis=1)
for i in range(Ts-1):
    m1all = m1all.append(m1[i+1].drop(['z'], axis=1))
    m2all = m2all.append(m2[i+1].drop(['z'], axis=1))
#---------------------------------------------------------------------------------------------



# The above step got time step data mixed up. 
# Identify the time step for active binding motors.
Ts_count = 0
m1_ts_no = []
for i in m1all.index == 0: # check all index having 0 (starting point of a time step)
    if i == True:
        m1_ts_no.append(Ts_count)
        Ts_count+=1
    else:
        m1_ts_no.append(Ts_count-1)
m1_ts_no = np.array(m1_ts_no) # make np array
m1_ts_no = pd.DataFrame({'Ts':m1_ts_no}) # make pd dataframe

# Identify the time step for defective binding motors.
Ts_count = 0
m2_ts_no = []
for i in m2all.index == 0: # check all index having 0 (starting point of a time step)
    if i == True:
        m2_ts_no.append(Ts_count)
        Ts_count+=1
    else:
        m2_ts_no.append(Ts_count-1)
m2_ts_no = np.array(m2_ts_no)
m2_ts_no = pd.DataFrame({'Ts':m2_ts_no})
#---------------------------------------------------------------------------------------------



# Identify the duplicated points.
m1dups = 1*m1all.duplicated() # check all duplicates. if duplicated, assign True
m1dups = pd.DataFrame({'label':m1dups}) # make a dataframe of 0 or/and 1
m2dups = 1*m2all.duplicated()
m2dups = pd.DataFrame({'label':m2dups})

# Organize and save the labeled data.
m1_ts_no_ = m1_ts_no.reset_index(drop=True) # discard the index
m2_ts_no_ = m2_ts_no.reset_index(drop=True)
m1all_ = m1all.reset_index(drop=True)
m2all_ = m2all.reset_index(drop=True)
m1dups_ = m1dups.reset_index(drop=True)
m2dups_ = m2dups.reset_index(drop=True)
m1r = pd.concat([m1_ts_no_,m1all_,m1dups_],axis=1) # make a dataframe: Ts | binding motor(x,y) | duplicate or not
m2r = pd.concat([m2_ts_no_,m2all_,m2dups_],axis=1)
#m1r.to_csv('lyf1_active.csv', index=False, float_format='%.5f') # save the above dataframe
#m2r.to_csv('lyf2_defective.csv', index=False, float_format='%.5f')
m1r_srt = m1r.sort_values(['x','Ts'],ascending=[True,True]) # sort ascending in priority of x
m2r_srt = m2r.sort_values(['x','Ts'],ascending=[True,True])
m1r_srt.to_csv('lyf3_active_srt.csv', index=False, float_format='%.5f') # save the above dataframe
m2r_srt.to_csv('lyf4_defective_srt.csv', index=False, float_format='%.5f')
#---------------------------------------------------------------------------------------------



#=============================================================================================
# Types of active/defective binding motors (discovered during a preliminary analysis)
# ## 1. Disappearing motor
# A disappearing motor has a lifetime of less than 0.01 sec (one time step).
# 
# There are two kinds of a disappearing motors.
# ### (i) Unique-disappearing motor (labelled as 0.0)
# Unique-disappearing motor,Uq, appears in only one time step then disappears forever.
# ### (ii) Persistent-disappearing motor (labelled as 0.1)
# Persistent-disappearing motor,Pe, appears in more than one time step but does not live up to the next immediate time step
# 
# ## 2. Aggressive motor (labelled as 1.0)
# Aggressive motor,Ag, has a lifetime of 0.01 sec. or more. It exists in more that one consecutive time step.
# 
# NB: An aggressive motor can become a persistent-disappering motor and vice versa.
# 
# - some aggressive motors are hopping -- incessant on and off 
#==============================================================================================



# Label the binding behaviour as described above.
m1r_new = m1r_srt.reset_index(drop=True) # discard the index for the sorted data
m2r_new = m2r_srt.reset_index(drop=True)
m1xy = np.around( m1r_new[m1r_new.columns[1:3]], 5).values.tolist() # extract the binding data (x,y) from the sorted dataframe 
m2xy = np.around( m2r_new[m2r_new.columns[1:3]], 5).values.tolist()

# Label the active binding motors.
idx = 0
for i in m1xy:
    if m1xy[idx+1] == m1xy[idx]:
        if np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx]) == 1: # identify an aggressive motor (label 1.0)
            m1r_new['label'].loc[idx] = 1.0
            m1r_new['label'].loc[idx+1] = 1.0
        elif np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx]) != 1: # identify a persistent disappearing motor (label 0.1)
            try:
                if m1xy[idx+1] != m1xy[idx+2]:
                    #m1r_new['label'].loc[idx] = 0.1#7 over-egged pudding --> re-labelling 1.0 to 0.1
                    m1r_new['label'].loc[idx+1] = 0.1
                elif m1xy[idx+1] == m1xy[idx+2]:
                    if np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx+2]) != 1:
                        m1r_new['label'].loc[idx+1] = 0.1
                    elif np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx+2]) == 1:
                        if m1xy[idx+1] == m1xy[idx+2] and m1xy[idx] == m1xy[idx-1] and (np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx]) != 1) and (np.absolute(m1r_new['Ts'][idx] - m1r_new['Ts'][idx-1]) == 1):
                            m1r_new['label'].loc[idx] = 1.0 # Aggressive rare/special
                        else:
                            m1r_new['label'].loc[idx] = 0.1
            except Exception as e:
                if str(e) == 'list index out of range':
                    pass
                else:
                    print('Unknown error!')
    elif m1xy[idx+1] != m1xy[idx]: # identify a unique disappearing motor (label 0.0)
        try:
            if m1xy[idx+1] != m1xy[idx+2]:
                m1r_new['label'].loc[idx+1] = 0.0
            elif m1xy[idx+1] == m1xy[idx+2]:
                if np.absolute(m1r_new['Ts'][idx+1] - m1r_new['Ts'][idx+2]) != 1: # a persistent disappearing motor
                    m1r_new['label'].loc[idx+1] = 0.1
        except Exception as e:
            if str(e) == 'list index out of range':
                m1r_new['label'].loc[idx+1] = 0.0
            else:
                print('Unknown error!')
    if idx < (len(m1xy)-2):
        idx+=1
m1r_new.to_csv('lyf5_active_srt_labelled.csv', index=False, float_format='%.5f')

# Label the defective binding motors.
idx = 0
for i in m2xy:
    if m2xy[idx+1] == m2xy[idx]:
        if np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx]) == 1: # identify an aggressive motor (label 1.0)
            m2r_new['label'].loc[idx] = 1.0
            m2r_new['label'].loc[idx+1] = 1.0
        elif np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx]) != 1: # identify a persistent disappearing motor (label 0.1)
            try:
                if m2xy[idx+1] != m2xy[idx+2]:
                    m2r_new['label'].loc[idx+1] = 0.1
                elif m2xy[idx+1] == m2xy[idx+2]:
                    if np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx+2]) != 1:
                        m2r_new['label'].loc[idx+1] = 0.1
                    elif np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx+2]) == 1:
                        if m2xy[idx+1] == m2xy[idx+2] and m2xy[idx] == m2xy[idx-1] and (np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx]) != 1) and (np.absolute(m2r_new['Ts'][idx] - m2r_new['Ts'][idx-1]) == 1):
                            m2r_new['label'].loc[idx] = 1.0 # Aggressive rare/special
                        else:
                            m2r_new['label'].loc[idx] = 0.1
            except Exception as e:
                if str(e) == 'list index out of range':
                    pass
                else:
                    print('Unknown error!')
    elif m2xy[idx+1] != m2xy[idx]: # identify a unique disappearing motor (label 0.0)
        try:
            if m2xy[idx+1] != m2xy[idx+2]:
                m2r_new['label'].loc[idx+1] = 0.0
            elif m2xy[idx+1] == m2xy[idx+2]:
                if np.absolute(m2r_new['Ts'][idx+1] - m2r_new['Ts'][idx+2]) != 1: # a persistent disappearing motor
                    m2r_new['label'].loc[idx+1] = 0.1
        except Exception as e:
            if str(e) == 'list index out of range':
                m2r_new['label'].loc[idx+1] = 0.0
            else:
                print('Unknown error!')
    if idx < (len(m2xy)-2):
        idx+=1
m2r_new.to_csv('lyf6_defective_srt_labelled.csv', index=False, float_format='%.5f')

# Make separate dataframes for diferent binding motor types.
m1r_Ag = m1r_new[m1r_new.label == 1.0] # active and aggressive
m1r_Ag = m1r_Ag.reset_index(drop=True) 
m1r_Pe = m1r_new[m1r_new.label == 0.1] # active and persistent
m1r_Pe = m1r_Pe.reset_index(drop=True)
m1r_Uq = m1r_new[m1r_new.label == 0.0] # active and unique
m1r_Uq = m1r_Uq.reset_index(drop=True)

m2r_Ag = m2r_new[m2r_new.label == 1.0] # defective and aggressive
m2r_Ag = m2r_Ag.reset_index(drop=True)
m2r_Pe = m2r_new[m2r_new.label == 0.1] # defective and persistent
m2r_Pe = m2r_Pe.reset_index(drop=True)
m2r_Uq = m2r_new[m2r_new.label == 0.0] # defective and unique
m2r_Uq = m2r_Uq.reset_index(drop=True)
#---------------------------------------------------------------------------------------------



# Test if the expected Ag data is correct.
#for i in range(3317):
#    if m2r_Ag['x'].loc[i+1] - m2r_Ag['x'].loc[i] == 0:
#        if np.absolute(m2r_Ag['Ts'].loc[i+1] - m2r_Ag['Ts'].loc[i]) == 1:
#            pass
#        elif np.absolute(m2r_Ag['Ts'].loc[i+1] - m2r_Ag['Ts'].loc[i+2]) != 1:
#            print('Check index %s'%(i+1))
#    elif np.absolute(m2r_Ag['Ts'].loc[i+1] - m2r_Ag['Ts'].loc[i]) != 1 and (m2r_Ag['x'].loc[i+1] - m2r_Ag['x'].loc[i] == 0):
#        print('Check special index %s'%i)
#    else:
#        #print('Check passed :) !')
#        pass
#---------------------------------------------------------------------------------------------



# Calculate the lifetime of the aggressive active motors and save to file.
m1ltym = {} # lifetime
idx = 0
m1Ag_on_ = [] # time step where the aggressive motor started
arr = np.around( m1r_Ag[m1r_Ag.columns[1:3]], 5).values.tolist()
for x in arr:
    if str(x) not in m1ltym:
        m1ltym[str(x)]=0
        m1Ag_on_.append(m1r_Ag[m1r_Ag.columns[0]].iloc[idx])
    else:
        if np.absolute(m1r_Ag[m1r_Ag.columns[0]].iloc[idx] - m1r_Ag[m1r_Ag.columns[0]].iloc[idx-1]) == 1:
            m1ltym[str(x)] += 1
        #if (m1ltym[str(x)] >2) and ( np.absolute(m1r_Ag[m1r_Ag.columns[0]].iloc[idx] - m1r_Ag[m1r_Ag.columns[0]].iloc[idx-1]) != np.absolute(m1r_Ag[m1r_Ag.columns[0]].iloc[idx-1] - m1r_Ag[m1r_Ag.columns[0]].iloc[idx-2]) ):
            #m1ltym[str(x)] -= 1 
        #if (m1ltym[str(x)] == 5) and ( np.absolute(m1r_Ag[m1r_Ag.columns[0]].iloc[idx] - m1r_Ag[m1r_Ag.columns[0]].iloc[idx-1]) != np.absolute(m1r_Ag[m1r_Ag.columns[0]].iloc[idx-1] - m1r_Ag[m1r_Ag.columns[0]].iloc[idx-2]) ):
            #m1ltym[str(x)] = 4 
    idx+=1
    
m1Ag_onx = np.array(m1Ag_on_) # make np array
m1Ag_on = pd.DataFrame({'Ts':m1Ag_onx}) # make pd dataframe
m1lftym = np.fromiter(m1ltym.values(), dtype=int) # pick dictionary values
m1lftym_Ag = pd.DataFrame({'life':m1lftym}) # make them to be pandas dataframe
#m1Ag_mtr = pd.DataFrame({'mtr':np.array(list(m1ltym.keys()))}) # pick dictionary keys and make pd df

# make a nice list from the dictionary keys, then make a pandas dataframe
# NB: from ast import literal_eval
m1ltym_list = []
for i in list(m1ltym.keys()):
    m1ltym_list.append(literal_eval(i))    

m1ltym_list = np.array(m1ltym_list)
m1Ag_mtr = pd.DataFrame({'x':m1ltym_list[:,0], 'y':m1ltym_list[:,1]})
m1r_Aglf = pd.concat([m1Ag_on,m1Ag_mtr,m1lftym_Ag],axis=1) # combine, sort, and clean
m1r_Aglf = m1r_Aglf.sort_values(['Ts'],ascending=[True])
m1r_Aglf = m1r_Aglf.reset_index(drop=True)
m1r_Aglf.to_csv('lyf7_active_aggressive.csv', index=False, float_format='%.5f')

lyf0 = np.zeros((m1r_new.shape[0],1), dtype=int) # make zero dataframe
lyf0 = pd.DataFrame(lyf0,columns=['life'])
m1r_lyf0 = pd.concat([m1r_new,lyf0], axis=1)

# update the life column of m1r_lyf0 with the actual life from m1r_Aglf
lyf_list = np.around(m1r_Aglf[m1r_Aglf.columns[1:3]], 5).values.tolist()
lyf0_list = np.around(m1r_lyf0[m1r_lyf0.columns[1:3]], 5).values.tolist()

for i in range(len(lyf0_list)):
    for j in range(len(lyf_list)):
        if lyf_list[j] == lyf0_list[i]:
            if m1r_lyf0['label'].loc[i] == 1.0:
                m1r_lyf0['life'].loc[i] = int(m1r_Aglf['life'].loc[j])
                
m1r_lyf0['label'] = m1r_lyf0['label'].map(lambda x: '%.1f' % x) # make label column have only one decimal
m1r_lyf0.to_csv('lyf8_active_label_life.csv', float_format='%.5f', index=False)
#---------------------------------------------------------------------------------------------



# Calculate the lifetime of the aggressive defective motors and save to file.
m2ltym = {} # lifetime
idx = 0
m2Ag_on_ = [] # time step where the aggressive motor started
arr = np.around( m2r_Ag[m2r_Ag.columns[1:3]], 5).values.tolist()
for x in arr:
    if str(x) not in m2ltym:
        m2ltym[str(x)]=0
        m2Ag_on_.append(m2r_Ag[m2r_Ag.columns[0]].iloc[idx])
    else:
        if np.absolute(m2r_Ag[m2r_Ag.columns[0]].iloc[idx] - m2r_Ag[m2r_Ag.columns[0]].iloc[idx-1]) == 1:
            m2ltym[str(x)] += 1
    idx+=1

m2Ag_onx = np.array(m2Ag_on_) # make np array
m2Ag_on = pd.DataFrame({'Ts':m2Ag_onx}) # make pd dataframe
m2lftym = np.fromiter(m2ltym.values(), dtype=int) # pick dictionary values
m2lftym_Ag = pd.DataFrame({'life':m2lftym}) # make them to be pandas dataframe
#m2Ag_mtr = pd.DataFrame({'mtr':np.array(list(m2ltym.keys()))}) # pick dictionary keys and make pd df

# make a nice list from the dictionary keys, then make a pandas dataframe
# NB: from ast import literal_eval
m2ltym_list = []
for i in list(m2ltym.keys()):
    m2ltym_list.append(literal_eval(i))
    
m2ltym_list = np.array(m2ltym_list)
m2Ag_mtr = pd.DataFrame({'x':m2ltym_list[:,0], 'y':m2ltym_list[:,1]})
m2r_Aglf = pd.concat([m2Ag_on,m2Ag_mtr,m2lftym_Ag],axis=1) # combine, sort, and clean
m2r_Aglf = m2r_Aglf.sort_values(['Ts'],ascending=[True])
m2r_Aglf = m2r_Aglf.reset_index(drop=True)
m2r_Aglf.to_csv('lyf9_defective_aggressive.csv', index=False, float_format='%.5f')

lyf0 = np.zeros((m2r_new.shape[0],1), dtype=int)
lyf0 = pd.DataFrame(lyf0,columns=['life'])
m2r_lyf0 = pd.concat([m2r_new,lyf0], axis=1)

# update the life column of m1r_lyf0 with the actual life from m1r_Aglf
lyf_list = np.around(m2r_Aglf[m2r_Aglf.columns[1:3]], 5).values.tolist()
lyf0_list = np.around(m2r_lyf0[m2r_lyf0.columns[1:3]], 5).values.tolist()

for i in range(len(lyf0_list)):
    for j in range(len(lyf_list)):
        if lyf_list[j] == lyf0_list[i]:
            if m2r_lyf0['label'].loc[i] == 1.0:
                m2r_lyf0['life'].loc[i] = int(m2r_Aglf['life'].loc[j])
                
m2r_lyf0['label'] = m2r_lyf0['label'].map(lambda x: '%.1f' % x) # make label column have only one decimal
m2r_lyf0.to_csv('lyf10_defective_label_life.csv', float_format='%.5f', index=False)
#---------------------------------------------------------------------------------------------



#m1r_lyf_ = m1r_lyf0.sort_values(['Ts'], ascending=[True])
#m2r_lyf_ = m2r_lyf0.sort_values(['Ts'], ascending=[True])
print("\n")
print("===========================================")
print("%s Persistent active motors"%(len(m1r_Pe)))
print("%s Unique active motors"%(len(m1r_Uq)))
print("%s Aggressive active motors"%(len(m1r_Ag)))
print("===========================================")
print("%s Persistent defective motors"%(len(m2r_Pe)))
print("%s Unique defective motors"%(len(m2r_Uq)))
print("%s Aggressive defective motors"%(len(m2r_Ag)))
print("===========================================")
print("\n")
#---------------------------------------------------------------------------------------------

