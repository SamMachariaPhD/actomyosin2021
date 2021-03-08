# Use conformation file to plot various speeds using various dt
# Regards, Sam Macharia

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

results_dir = 'ANALYSIS'
try:  
    os.mkdir(results_dir)
except OSError:  
    print ("=> Creation of the directory: %s failed" % results_dir)
else:  
    print ("=> Successfully created %s directory." % results_dir)

conf = pd.read_csv('Conformation_A001.txt', names=['time','x','y','z'], delim_whitespace=True)

dt = 0.01; dt002 = 0.02; dt005 = 0.05; dt01 = 0.1; dt02 = 0.2; dt05 = 0.5; dt1 = 1; dt2 = 2; dt5 = 5
x = np.array([0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0])


#============================================================================
Head = conf.iloc[0::13,:]
Head = Head.reset_index(drop=True)
#============================================================================
Head002 = Head.iloc[0::2,:]
Head002 = Head002.reset_index(drop=True)
#============================================================================
Head005 = Head.iloc[0::5,:]
Head005 = Head005.reset_index(drop=True)
#============================================================================
Head01 = Head.iloc[0::10,:]
Head01 = Head01.reset_index(drop=True)
#============================================================================
Head02 = Head.iloc[0::20,:]
Head02 = Head02.reset_index(drop=True)
#============================================================================
Head05 = Head.iloc[0::50,:]
Head05 = Head05.reset_index(drop=True)
#============================================================================
Head1 = Head.iloc[0::100,:]
Head1 = Head1.reset_index(drop=True)
#============================================================================
Head2 = Head.iloc[0::200,:]
Head2 = Head2.reset_index(drop=True)
#============================================================================
Head5 = Head.iloc[0::500,:]
Head5 = Head5.reset_index(drop=True)
#============================================================================

#============================================================================
dxHead = np.diff(Head['x'])
dyHead = np.diff(Head['y'])
#============================================================================
dxHead002 = np.diff(Head002['x'])
dyHead002 = np.diff(Head002['y'])
#============================================================================
dxHead005 = np.diff(Head005['x'])
dyHead005 = np.diff(Head005['y'])
#============================================================================
dxHead01 = np.diff(Head01['x'])
dyHead01 = np.diff(Head01['y'])
#============================================================================
dxHead02 = np.diff(Head02['x'])
dyHead02 = np.diff(Head02['y'])
#============================================================================
dxHead05 = np.diff(Head05['x'])
dyHead05 = np.diff(Head05['y'])
#============================================================================
dxHead1 = np.diff(Head1['x'])
dyHead1 = np.diff(Head1['y'])
#============================================================================
dxHead2 = np.diff(Head2['x'])
dyHead2 = np.diff(Head2['y'])
#============================================================================
dxHead5 = np.diff(Head5['x'])
dyHead5 = np.diff(Head5['y'])
#============================================================================

#============================================================================
distHead = np.sqrt((dxHead**2)+(dyHead**2))
spdHead = distHead/(1*dt)
avSpdHead = np.mean(spdHead)
#============================================================================
distHead002 = np.sqrt((dxHead002**2)+(dyHead002**2))
spdHead002 = distHead002/(2*dt)
avSpdHead002 = np.mean(spdHead002)
#============================================================================
distHead005 = np.sqrt((dxHead005**2)+(dyHead005**2))
spdHead005 = distHead005/(5*dt)
avSpdHead005 = np.mean(spdHead005)
#============================================================================
distHead01 = np.sqrt((dxHead01**2)+(dyHead01**2))
spdHead01 = distHead01/(10*dt)
avSpdHead01 = np.mean(spdHead01)
#============================================================================
distHead02 = np.sqrt((dxHead02**2)+(dyHead02**2))
spdHead02 = distHead02/(20*dt)
avSpdHead02 = np.mean(spdHead02)
#============================================================================
distHead05 = np.sqrt((dxHead05**2)+(dyHead05**2))
spdHead05 = distHead05/(50*dt)
avSpdHead05 = np.mean(spdHead05)
#============================================================================
distHead1 = np.sqrt((dxHead1**2)+(dyHead1**2))
spdHead1 = distHead1/(100*dt)
avSpdHead1 = np.mean(spdHead1)
#============================================================================
distHead2 = np.sqrt((dxHead2**2)+(dyHead2**2))
spdHead2 = distHead2/(200*dt)
avSpdHead2 = np.mean(spdHead2)
#============================================================================
distHead5 = np.sqrt((dxHead5**2)+(dyHead5**2))
spdHead5 = distHead5/(500*dt)
avSpdHead5 = np.mean(spdHead5)
#============================================================================
avSpdH = np.array([avSpdHead,avSpdHead002,avSpdHead005,avSpdHead01,avSpdHead02,avSpdHead05,avSpdHead1,avSpdHead2,avSpdHead5])


#============================================================================
stdHead = np.sum(((spdHead-avSpdHead)**2)/(np.size(spdHead)-1))
stdHead = np.sqrt(stdHead)
#============================================================================
stdHead002 = np.sum(((spdHead002-avSpdHead002)**2)/(np.size(spdHead002)-1))
stdHead002 = np.sqrt(stdHead002)
#============================================================================
stdHead005 = np.sum(((spdHead005-avSpdHead005)**2)/(np.size(spdHead005)-1))
stdHead005 = np.sqrt(stdHead005)
#============================================================================
stdHead01 = np.sum(((spdHead01-avSpdHead01)**2)/(np.size(spdHead01)-1))
stdHead01 = np.sqrt(stdHead01)
#============================================================================
stdHead02 = np.sum(((spdHead02-avSpdHead02)**2)/(np.size(spdHead02)-1))
stdHead02 = np.sqrt(stdHead02)
#============================================================================
stdHead05 = np.sum(((spdHead05-avSpdHead05)**2)/(np.size(spdHead05)-1))
stdHead05 = np.sqrt(stdHead05)
#============================================================================
stdHead1 = np.sum(((spdHead1-avSpdHead1)**2)/(np.size(spdHead1)-1))
stdHead1 = np.sqrt(stdHead1)
#============================================================================
stdHead2 = np.sum(((spdHead2-avSpdHead2)**2)/(np.size(spdHead2)-1))
stdHead2 = np.sqrt(stdHead2)
#============================================================================
stdHead5 = np.sum(((spdHead5-avSpdHead5)**2)/(np.size(spdHead5)-1))
stdHead5 = np.sqrt(stdHead5)
#============================================================================
stdH = np.array([stdHead,stdHead002,stdHead005,stdHead01,stdHead02,stdHead05,stdHead1,stdHead2,stdHead5])


#============================================================================
xHead = np.arange(0,spdHead.shape[0])
xHead01 = np.arange(0,spdHead.shape[0], step=10)
#============================================================================
np.savetxt(results_dir+'/'+'v9DtvsSpd.csv', np.transpose([x,avSpdH,stdH]), fmt='%.8f', delimiter=',')

fig, ax = plt.subplots(figsize=(15,12))

ax.errorbar(x,avSpdH,stdH, capsize=3, linestyle='--', marker='o', color='blue', ecolor='green', label='Speed changes')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_yticks(np.arange(0,15,2))
ax.set_xticks(np.arange(0.0,6.2,1.0))
ax.tick_params(labelsize=18)

ax.set_xlabel('$\Delta t$', fontsize=18)
ax.set_ylabel('Speed ($\mu m/s$)', fontsize=18)
#ax.set_title('R = 0.3, $F_{M_2}$ = 5.0 pN', fontsize=18)

ax.legend()

#plt.savefig(results_dir+'/'+'v9RvsSpd.png', fmt='png', dpi=500, bbox_inches='tight')
plt.savefig(results_dir+'/'+'v9DtvsSpd.svg', fmt='svg', dpi=3000, bbox_inches='tight')
