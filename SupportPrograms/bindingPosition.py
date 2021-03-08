#!/usr/bin/env python
# coding: utf-8
#
# Input binding motor contact position data.
# Output a histogram(bar graph) of binding position vs. binding occurrence.
# Regards, Sam Macharia

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Ts = 501
r = '0.8'
segments = 12 # beads = 13

acpos = []; inpos = []
for i in range(Ts):
    acpos_ = pd.read_csv('ActivePos_5s133R0.8Ts'+str(i)+'.csv', names=['ac'])
    acpos.append(acpos_)
    inpos_ = pd.read_csv('InactivePos_5s133R0.8Ts'+str(i)+'.csv', names=['in'])
    inpos.append(inpos_)
#============================================================================================= 



# collect active/inactive binding motors between beads
# prepare 12 empty buckets to put numbers between beads (for 12 segments)
ac = [[] for _ in range(segments)]
for i in range(Ts):
    for j in range(segments):
        acposx = acpos[i].loc[acpos[i]['ac'].between(j+1,j+2)]
        ac[j].append(acposx)

# Inactive:        
ina = [[] for _ in range(segments)]
for i in range(Ts):
    for j in range(segments):
        inposx = inpos[i].loc[inpos[i]['in'].between(j+1,j+2)]
        ina[j].append(inposx)      
#============================================================================================= 



# get the number of active/inactive motors binding between beads
precision = 5
abm = [[] for _ in range(segments)]
for i in range(Ts):
    for j in range(segments):
        abmx = len(ac[j][i]) # get the number of motors binding in specific positions (between beads)
        abm[j].append(abmx)
abm_mn = [[] for _ in range(segments)]
abm_std = [[] for _ in range(segments)]
for k in range(segments):
    # get the mean and std deviation
    abm_mn[k] = round(np.mean(abm[k]),precision) # get the mean number binding in specific positions
    abm_std[k] = round(np.std(abm[k]),precision) # get the standard deviation 
    
# Inactive: # repeat the above algorithm for the inactive motors
ibm = [[] for _ in range(segments)]
for i in range(Ts):
    for j in range(segments):
        ibmx = len(ina[j][i])
        ibm[j].append(ibmx)
ibm_mn = [[] for _ in range(segments)]
ibm_std = [[] for _ in range(segments)]
for k in range(segments):
    # get the mean and std deviation
    ibm_mn[k] = round(np.mean(ibm[k]),precision)
    ibm_std[k] = round(np.std(ibm[k]),precision)
#============================================================================================= 



# Are there duplicated contact states within a timestep?
for j in range(Ts):
    for i in range(segments):
        if np.sum(1*ac[i][j]['ac'].duplicated()) == 1:
            print("\n")
            print("#=========================================")
            print('Active contact state duplicate: segment %s Ts %s'%(i,j))
            print(ac[i][j])
            print("#=========================================")

for j in range(Ts):
    for i in range(segments):
        if np.sum(1*ina[i][j]['in'].duplicated()) == 1:
            print("\n")
            print("#=========================================")
            print('Defective contact state duplicate: segment %s Ts %s'%(i,j))
            print(ina[i][j])
            print("#=========================================")
#============================================================================================= 



# Plot the bar graph.
fig, a = plt.subplots(2,1)
#plt.subplots_adjust(hspace=0.15)
bins = np.arange(1.5,13.5)
fig.set_size_inches(8,8)
a[0].bar(bins,abm_mn, yerr=abm_std, align='center', ecolor='red', error_kw=dict(lw=3,capsize=3,capthick=1), facecolor='green', alpha=0.1, ec='green')
a[0].bar(bins,abm_mn, yerr=abm_std, align='center', ecolor='white', error_kw=dict(lw=1,capsize=1,capthick=.5), facecolor='green', alpha=0.6, ec='green', label='Active motor')
a[0].set_xticks(np.arange(1,14,1))
a[0].set_yticks(np.arange(0,6,1))
a[0].spines['top'].set_visible(False)
a[0].spines['right'].set_visible(False)
a[0].spines['bottom'].set_bounds(1,13)
a[0].spines['left'].set_bounds(0,5)
a[0].invert_xaxis()
a[0].tick_params(axis='x', which='both', pad=25)
a[0].legend(loc = 'upper left')
a[0].set_title('R = '+r, fontsize=15)
#fig.set_size_inches(8,2)
#=========================================================================================
a[1].bar(bins,ibm_mn, yerr=ibm_std, align='center', ecolor='red', error_kw=dict(lw=3,capsize=3,capthick=1), facecolor='blue', alpha=0.1, ec='blue')
a[1].bar(bins,ibm_mn, yerr=ibm_std, align='center', ecolor='white', error_kw=dict(lw=1,capsize=1,capthick=.5), facecolor='blue', alpha=0.6, ec='blue', label='Defective motor')
a[1].set_xticks(np.arange(1,14,1))
a[1].set_yticks(np.arange(0,6,1))
a[1].spines['bottom'].set_position('zero')
a[1].spines['bottom'].set_bounds(1,13)
a[1].spines['left'].set_bounds(0,5)
a[1].invert_yaxis()
a[1].invert_xaxis()
a[1].tick_params(axis='x', direction='in')#, length=6, width=2, colors='r',grid_color='r', grid_alpha=0.5)
a[1].set_xticklabels([])
a[1].spines['top'].set_visible(False)
a[1].spines['right'].set_visible(False)
a[1].legend(loc = 'lower left')

fig.text(1.07, 0.47, 'Actin binding position', ha='center', fontsize=15)
fig.text(0.04, 0.5, 'Binding occurrences', va='center', rotation='vertical', fontsize=15) # Mean binding occurrences

plt.savefig('motors_MNpos.svg', fmt='.svg', dpi=1200, bbox_inches='tight')
#plt.savefig('motors_MNpos.png', fmt='.png', dpi=1500, bbox_inches='tight')

plt.show()

