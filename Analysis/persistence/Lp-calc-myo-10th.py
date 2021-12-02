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
plt.style.use("ggplot")
cm = 1/2.54
#====================================================================

#Import trajectory data
conff0 = glob.glob('data/ConfT5F0S**.txt'); f = 0.0
conff0 = sorted(conff0)
print("Imported data list:"); print(conff0)
#====================================================================

# Required parameters
beads = 13 # Filament beads (actin)
#jmp = 10 ; dt = 'dt0'; Dt = 0.1 # Adjust delta t
jmp = 20 ; dt = 'dt2'; Dt = 0.2
#jmp = 30 ; dt = 'dt0'; Dt = 3 # For microtubule
#v00 = 0.8 # Filament speed
v0 = 7.0; #v_1 = 7.7; v1 = 7.8
#====================================================================

# Calculate the difference and store the values
conf0 = [];
xy0 = []; xy_1 = []; xy1 = [];
xdiff0 = []; ydiff0 = []; 
for i in conff0:
    _ = pd.read_csv(i, names=['t','x','y','z'], delim_whitespace=True)
    xy0_ = _[0::beads] # jump beads
    xy0.append(xy0_) # _
    _ = xy0_[0::jmp] # _
    _ = _.reset_index(drop=True)
    conf0.append(_)
    xdiff0.append(np.diff(_['x']))
    ydiff0.append(np.diff(_['y']))
#====================================================================

# Plot sample trajectories
fig, ax = plt.subplots(1,5, figsize=(50*cm, 10*cm), sharex = True, \
sharey = True)

ax[0].plot(xy0[0]['x'], xy0[0]['y'], color='red', label='Original')
ax[0].plot(conf0[0]['x'], conf0[0]['y'], color='blue', label='Approx')
ax[0].minorticks_on()
ax[0].tick_params('both', direction='in', length=8, top=True, \
right=True, which='major')
ax[0].tick_params('both', direction='in', length=4, top=True, \
right=True, which='minor')
ax[0].set_xlabel('X($\mu m$)')
ax[0].set_ylabel('Y($\mu m$)')
ax[0].legend()

ax[1].plot(xy0[1]['x'], xy0[1]['y'], color='red')
ax[1].plot(conf0[1]['x'], conf0[1]['y'], color='blue')
ax[1].minorticks_on()
ax[1].tick_params('both', direction='in', length=8, top=True, \
right=True, which='major')
ax[1].tick_params('both', direction='in', length=4, top=True, \
right=True, which='minor')
ax[1].set_xlabel('X($\mu m$)')

ax[2].plot(xy0[2]['x'], xy0[2]['y'], color='red')
ax[2].plot(conf0[2]['x'], conf0[2]['y'], color='blue')
ax[2].minorticks_on()
ax[2].tick_params('both', direction='in', length=8, top=True, \
right=True, which='major')
ax[2].tick_params('both', direction='in', length=4, top=True, \
right=True, which='minor')
ax[2].set_xlabel('X($\mu m$)')

ax[3].plot(xy0[3]['x'], xy0[3]['y'], color='red')
ax[3].plot(conf0[3]['x'], conf0[3]['y'], color='blue')
ax[3].minorticks_on()
ax[3].tick_params('both', direction='in', length=8, top=True, \
right=True, which='major')
ax[3].tick_params('both', direction='in', length=4, top=True, \
right=True, which='minor')
ax[3].set_xlabel('X($\mu m$)')

ax[4].plot(xy0[4]['x'], xy0[4]['y'], color='red')
ax[4].plot(conf0[4]['x'], conf0[4]['y'], color='blue')
ax[4].minorticks_on()
ax[4].tick_params('both', direction='in', length=8, top=True, \
right=True, which='major')
ax[4].tick_params('both', direction='in', length=4, top=True, \
right=True, which='minor')
ax[4].set_xlabel('X($\mu m$)')

print("Trajectories: ")
plt.savefig('fig/Traj-'+str(round(f,2))+'-Dt'+str(round(Dt,2))\
+'.pdf', format='pdf', bbox_inches='tight')
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
_ = []; ds0 = []; dsm0 = []; s0 = []; c = 0; 
ds0_ = []; dsm_ = []; s_ = []

# try:
#     os.remove('ds_ub_status.txt')
# except:
#     print("'ds_ub_status.txt' does not exist.")
    
for h in range(len(ub0)):
    for i in range(len(ub0[h])): # Save status for checking
#         print("Ds = %s"%i, file=open('ds_ub_status.txt','a'))
        for j in range(len(ub0[h])):
            try:
                _.append(np.dot(\
                ub0[h].loc[j].values,ub0[h].loc[j+i].values))
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
s0_m = dfs0.mean(axis=1)*v0*Dt
dsm0_m = dfdsm0.mean(axis=1)
#====================================================================

# Plot all the persistence length changes and the mean 
# Plot the persistence length with fitting, showing the Lp
fig, ax = plt.subplots(1,2, figsize=(20*cm,10*cm))
plt.subplots_adjust(wspace=0.3)

def tenth(x):
    dftenth = int(round(0.3*(len(x)+.1),0)) # 10% and round to the nearest whole
    return x[:dftenth]

for i in range(len(conff0)): # All trajectory plots
    ax[0].plot(tenth(s0_m), tenth(dfdsm0[i]), marker='o', markersize=3, ls='--', lw=1, \
    color='lightblue', markerfacecolor='lime', label='_nolegend_')
   
ax[0].plot(tenth(s0_m), tenth(dsm0_m), marker='o', markersize=3, ls='--', lw=1, \
color='red', markerfacecolor='lime', label='Average') # Mean plot
#ax[0].set_yticks(np.arange(-1,1.1,0.25)) # For actin
ax[0].minorticks_on()
ax[0].tick_params('both', direction='in', top=True, right=True, \
length=8, which='major')
ax[0].tick_params('both', direction='in', length=4, which='minor')
ax[0].set_xlabel(r'$(S \cdot V \cdot \Delta t)\ \mu m$', fontsize=14)
ax[0].set_ylabel(r'$\langle cos \Delta \theta (S) \rangle$', fontsize=14)
ax[0].set_title('F = %.2f pN | $\Delta t = %.2f\ sec$'%(f,Dt), fontsize=14)

#---------------------------------------------------------
# Calculate the log of y and then do fitting
x = s0_m 
y = dsm0_m 


x = tenth(x); print(x)
y = tenth(y); print(y)

y = np.log(y); print(y)
df_xy = pd.DataFrame({'x':x, 'y':y})
df_xy = df_xy.dropna() # remove any NaN
x = np.array(df_xy['x']); print(x)
y = np.array(df_xy['y']); print(y)

ax[1].plot(x,y, marker='o', c='r', ls='--', lw=1, markerfacecolor='lime')

def func(x,Lp): # fitting function
    return 1*(-x/(2*Lp)) 
params, covs = curve_fit(func, x, y)
y = func(x,*params)
perr = np.sqrt(np.diag(covs[0])) # Error on params
#---------------------------------------------------------
ax[1].plot(x, y, label=r'Lp = %.4f $\pm$ %.4f $\mu m$'\
%(params[0],perr)) # curve fit
#ax[1].set_yticks(np.arange(-3,0.1,0.5))
ax[1].minorticks_on()
ax[1].tick_params('both', direction='in', top=True, right=True, \
length=8, which='major')
ax[1].tick_params('both', direction='in', length=4, which='minor')
ax[1].set_xlabel(r'$(S \cdot V \cdot \Delta t)\ \mu m$', fontsize=14)
ax[1].set_ylabel(r'$log \langle cos \Delta \theta (S) \rangle$', \
fontsize=14)
ax[1].set_title('F = %.2f pN | $\Delta t = %.2f\ sec$'%(f,Dt), fontsize=14)

ax[1].legend()
plt.savefig('fig/LpF10th-'+str(round(f,2))+'-Dt'+str(round(Dt,2))\
+'.pdf', format='pdf', bbox_inches='tight')
plt.show()
#====================================================================