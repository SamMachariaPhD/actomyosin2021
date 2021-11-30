#!/usr/bin/env python
# coding: utf-8

# Input: trajectory x,y data
# Output: persistence length plots
#====================================================================


# Import important libs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os, glob
from scipy.optimize import curve_fit
plt.style.use("seaborn-whitegrid")
# plt.style.use("classic")
# plt.style.use("ggplot")
cm = 1/2.54
#====================================================================


#Import trajectory data
#conff0 = glob.glob('may_data/md10/data_A0**.txt')
#conff0 = glob.glob('may_data/md20/data_A0**.txt')
#conff0 = glob.glob('may_data/md30/data_A0**.txt')
#conff0 = glob.glob('may_data/md40/data_A0**.txt')
conff0 = glob.glob('may_data/md50/data_A0**.txt')
conff0 = sorted(conff0)
print("Imported data list:"); print(conff0)
#====================================================================


# Required parameters
beads = 13 # Filament beads
#jmp = 1 ; dt = 'dt0'; Dt = 0.1 # Adjust delta t
#jmp = 10 ; dt = 'dt0'; Dt = 1 
#jmp = 20 ; dt = 'dt0'; Dt = 2
jmp = 30 ; dt = 'dt0'; Dt = 3
v00 = 0.8 # Filament speed
v0 = 7.0; v_1 = 7.7; v1 = 7.8
#====================================================================


# Calculate the difference and store the values
conf0 = [];
xy0 = []; xy_1 = []; xy1 = [];
xdiff0 = []; ydiff0 = []; 
for i in conff0:
    _ = pd.read_csv(i, names=['t','x','y','z'], delim_whitespace=True)
    #xy0_ = _[0::beads]
    xy0.append(_)
    _ = _[0::jmp]
    conf0.append(_)
    xdiff0.append(np.diff(_['x']))
    ydiff0.append(np.diff(_['y']))
#====================================================================


# Plot some sample trajectories
fig, ax = plt.subplots(1,3, figsize=(30*cm, 10*cm), sharex = True, sharey = True)

ax[0].plot(xy0[0]['x'], xy0[0]['y'], color='red')
ax[0].plot(conf0[0]['x'], conf0[0]['y'], color='blue')
ax[0].minorticks_on()
ax[0].tick_params('both', direction='in', length=8, which='major')
ax[0].tick_params('both', direction='in', length=4, which='minor')
ax[0].set_xlabel('X($\mu m$)')
ax[0].set_ylabel('Y($\mu m$)')

ax[1].plot(xy0[1]['x'], xy0[1]['y'], color='red')
ax[1].plot(conf0[1]['x'], conf0[1]['y'], color='blue')
ax[1].minorticks_on()
ax[1].tick_params('both', direction='in', length=8, which='major')
ax[1].tick_params('both', direction='in', length=4, which='minor')
ax[1].set_xlabel('X($\mu m$)')

ax[2].plot(xy0[2]['x'], xy0[2]['y'], color='red')
ax[2].plot(conf0[2]['x'], conf0[2]['y'], color='blue')
ax[2].minorticks_on()
ax[2].tick_params('both', direction='in', length=8, which='major')
ax[2].tick_params('both', direction='in', length=4, which='minor')
ax[2].set_xlabel('X($\mu m$)')

print("Trajectories: ")
#plt.savefig('fig/may/Traj5-may-md40-Dt3.pdf', format='pdf', bbox_inches='tight')

plt.show()
#====================================================================


# Calculate unit vector
ubx0 = []; uby0 = []
ubx_1 = []; uby_1 = []
ubx1 = []; uby1 = []

for i in range(len(xdiff0)):
    b0 = np.sqrt(xdiff0[i]**2 + ydiff0[i]**2)
    ubx0.append(xdiff0[i]/b0)
    uby0.append(ydiff0[i]/b0)
#====================================================================


# Change numpy array to pandas
ub0 = []; ub_1 = []; ub1 = []

for i in range(len(ubx0)):
    ub0.append(pd.DataFrame({'ubx':ubx0[i], 'uby':uby0[i]}))
#====================================================================    


# Calculate the dot product/correlations
_ = []; ds0 = []; dsm0 = []; s0 = []; c = 0; ds0_ = []; dsm_ = []; s_ = []

# try:
#     os.remove('ds_ub_status.txt')
# except:
#     print("'ds_ub_status.txt' does not exist.")
    
for h in range(len(ub0)):
    for i in range(len(ub0[h])): # -1
#         print("Ds = %s"%i, file=open('ds_ub_status.txt','a'))
        for j in range(len(ub0[h])): # -1
            try:
                _.append(np.dot(ub0[h].loc[j].values,ub0[h].loc[j+i].values))
#                 print("Ub%s.Ub%s"%(j,j+i), file=open('ds_ub_status.txt','a'))
            except:
                pass #print("No: Ub%s.Ub%s"%(j,j+i))
        ds0_.append(_) # not necessary to save or is it?
        dsm_.append(np.mean(_))
        s_.append(c)
        _ = [] # empty this bucket
        c+=1;
    s0.append(s_)
    dsm0.append(dsm_)
    ds0.append(ds0_)
    c = 0; ds0_ = []; dsm_ = []; s_ = [] # reset stuff

s0 = np.array(s0)
#ds0 = np.array(ds0)
dsm0 = np.array(dsm0)
#====================================================================


# Calculate the mean of the correlations
dfs0 = pd.DataFrame(s0.T)
dfdsm0 = pd.DataFrame(dsm0.T)

s0_m = dfs0.mean(axis=1)*v00*Dt
dsm0_m = dfdsm0.mean(axis=1)
#====================================================================


# Take a look at the data
print("Take a look at s*v*dt: ")
print(dfs0)

print("Take a look at the Lp: ")
print(dfdsm0)


# Plot all the persistence length changes and the mean 
fig, ax = plt.subplots(1,1, figsize=(10*cm,10*cm))

dts = [0.05,0.1,0.2,0.3,0.5]; c=4

# for i in range(len(s0m)):
#     ax.plot(s0m[i],dsm0[i], marker='o', markersize=3, ls='--', lw=1, markerfacecolor='lime', label=r'$\Delta t = %.2f sec.$'%dts[c])
#     #c+=1
for i in range(0,30): #7
    ax.plot(s0_m,dfdsm0[i], marker='o', markersize=3, ls='--', lw=1, color='lightblue', markerfacecolor='lime')#, label=r'$\Delta t = %.2f sec.$'%dts[c])
#for i in range(27,30): #7
#    ax.plot(dfs0[i],dfdsm0[i], marker='o', markersize=3, ls='--', lw=1, color='blue', markerfacecolor='lime')#, label=r'$\Delta t = %.2f sec.$'%dts[c])

#ax.plot(dfs0[19],dfdsm0[19], marker='o', markersize=3, ls='--', lw=1, color='blue', markerfacecolor='lime')
    
ax.plot(s0_m,dsm0_m, marker='o', markersize=3, ls='--', lw=1, color='red', markerfacecolor='lime')

#ax.minorticks_on()
ax.tick_params('both', direction='in', top=True, right=True, length=8, which='major')
ax.tick_params('both', direction='in', length=4, which='minor')

ax.set_xlabel(r'$S \cdot V \cdot \Delta t$', fontsize=14)
ax.set_ylabel(r'$\langle cos \Delta \theta (S) \rangle$', fontsize=14)

#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 0.1 sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 1 sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD20', fontsize=14)
#ax.set_title('F = 0.0 pN | MD20 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD40 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD40', fontsize=14)
#ax.set_title('F = 0.0 pN | MD30', fontsize=14)
#ax.set_title('F = 0.0 pN | MD30 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD50 | $\Delta t = 1\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD50', fontsize=14)
ax.set_title('F = 0.0 pN | MD50 | $\Delta t = 3\ sec.$', fontsize=14)
#plt.legend()
plt.grid(0)

#plt.savefig('fig/may/LpAllT5-may-md10-Dt0.1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md10.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md10-Dt1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md10-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md20.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md20-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md30.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md30-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md40.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md40-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md50.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md50-Dt1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/LpAllT5-may-md50-Dt3.pdf', format='pdf', bbox_inches='tight')

plt.show()
#====================================================================


# Calculate the log of y and then do fitting
x = s0_m 
y = dsm0_m 
y = np.log(y)

def func(x,Lp):
    return 1*(-x/(2*Lp))
popt, pcov = curve_fit(func, x, y)
#====================================================================


# Plot the persistence length with fitting, showing the Lp
fig, ax = plt.subplots(1,1, figsize=(10*cm,10*cm), sharey=True)

ax.plot(x,y, marker='o', c='r', ls='--', lw=1, markerfacecolor='lime')#, label=r'$\Delta t = 0.1 sec.$')
ax.plot(x, func(x,*popt), label='Lp = %s'%np.round(popt[0],6))

#ax.minorticks_on()
ax.tick_params('both', direction='in', top=True, right=True, length=8, which='major')
ax.tick_params('both', direction='in', length=4, which='minor')

ax.set_xlabel(r'$S \cdot V \cdot \Delta t$', fontsize=14)
ax.set_ylabel(r'$log \langle cos \Delta \theta (S) \rangle$', fontsize=14)

#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 0.1 sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 1 sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD10 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD20', fontsize=14)
#ax.set_title('F = 0.0 pN | MD20 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD30', fontsize=14)
#ax.set_title('F = 0.0 pN | MD30 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD40', fontsize=14)
#ax.set_title('F = 0.0 pN | MD40 | $\Delta t = 3\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD50', fontsize=14)
#ax.set_title('F = 0.0 pN | MD50 | $\Delta t = 1\ sec.$', fontsize=14)
#ax.set_title('F = 0.0 pN | MD50 | $\Delta t = 3\ sec.$', fontsize=14)

ax.legend()
plt.grid(0)

#plt.savefig('fig/may/Lp-md10-Dt0.1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md10.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md10-Dt1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md10-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md20.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md20-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md30.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md30-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md40-Dt3.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md40.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md50.pdf', format='pdf', bbox_inches='tight') 
#plt.savefig('fig/may/Lp-md50-Dt1.pdf', format='pdf', bbox_inches='tight')
#plt.savefig('fig/may/Lp-md50-Dt3.pdf', format='pdf', bbox_inches='tight')

plt.show()
#====================================================================

