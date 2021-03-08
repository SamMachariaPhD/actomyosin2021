#!/usr/bin/env python
# coding: utf-8
# Various anlaysis
# Regards, Sam Macharia

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, glob, csv, io, sys
import scipy.stats as stats
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
#import sympy as sym

results_dir = 'ANALYSIS'

try:  
    os.mkdir(results_dir)
except OSError:  
    print ("=> Creation of the directory: %s failed" % results_dir)
else:  
    print ("=> Successfully created %s directory." % results_dir)

conf = pd.read_csv('Conformation_A001.txt', names=['time','x','y','z'], delim_whitespace=True)

dt = 0.01
dt01 = 0.1
#===================================================================================================
columns = ['time', 'x_tip', 'y_tip']; DtFile=0.01
df_load = pd.read_csv('TipXY_A001.txt', names=columns, delim_whitespace=True)
df_nice = df_load.drop(['time'], axis=1)
df = df_nice.iloc[0::10, :] #pick every 9th row starting from the first
df.to_csv(results_dir+'/SkippedTipXY_A001.csv', encoding='utf-8', index=False)

Dx_tip = np.diff(df['x_tip']); Dy_tip = np.diff(df['y_tip'])
DD=np.sqrt((Dx_tip**2)+(Dy_tip**2))
np.savetxt(results_dir+'/DD_A001.csv', DD, delimiter=',')
v=DD/(10*DtFile); Av_vel = np.mean(v)
np.savetxt(results_dir+'/v.csv', v, delimiter=',')
vSD=np.sum(((v-Av_vel)**2)/(np.size(v)-1)); vSD=np.sqrt(vSD)

plt.figure(figsize=(10,8))
plt.axes().set_aspect('equal')
plt.plot(df['x_tip'],df['y_tip'],label='Leading tip', color='green', linestyle='dashed', linewidth=1)
plt.scatter(df['x_tip'],df['y_tip'], marker='.', s=3, color='blue')
plt.xlabel('X', fontsize=16); plt.ylabel('Y', fontsize=16)
plt.title('Actin filament tip movement '); plt.legend(loc='upper left'); plt.grid()
plt.savefig(results_dir+'/'+'tipXY.png', fmt='png', dpi=300, bbox_inches='tight')
#===================================================================================================
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

xHead = np.arange(0,spdHead.shape[0])
xHead01 = np.arange(0,spdHead.shape[0], step=10)

#xHead = np.linspace(0,spdHead.shape[0],spdHead.shape[0])
#xHead01 = np.linspace(0,spdHead.shape[0],spdHead.shape[0])

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

xTail = np.arange(0,spdTail.shape[0])
xTail01 = np.arange(0,spdTail.shape[0], step=10)
#===================================================================================================
fig, ax = plt.subplots(figsize=(15,10))

plt.title('Instantaneous Speed', fontsize=16)

ax.plot(xHead01,spdHead01, color='red', label='Head: dt 0.01, spd %.4f $\mu m/s$, stdev %.4f | dt 0.1, spd %.4f $\mu m/s$, stdev %.4f'%(avSpdHead,stdHead,avSpdHead01,stdHead01))
ax.plot(xTail01,spdTail01, color='blue', label='Tail: dt 0.01, spd %.4f $\mu m/s$, stdev %.4f | dt 0.1, spd %.4f $\mu m/s$, stdev %.4f'%(avSpdTail,stdTail,avSpdTail01,stdTail01))

ax.set_xlabel('Time step', fontsize=16)
ax.set_ylabel('Speed ($\mu m/s$)', fontsize=16)
ax.tick_params(labelsize=16)

ax.legend()
plt.grid(color='gray', which='both', linestyle=':', linewidth=0.25)
#plt.savefig(results_dir+'/'+'inst.svg', fmt='svg', dpi=3000, bbox_inches='tight')
plt.savefig(results_dir+'/'+'inst.png', fmt='png', dpi=300, bbox_inches='tight')
#===================================================================================================
fig, ax = plt.subplots(figsize=(15,12))

plt.title('XY Trajectory [dt = 0.1]', fontsize=16)

ax.set_aspect('equal')

ax.plot(Head01['x'], Head01['y'], marker='.', linestyle='-', color='red', label='Head')
ax.plot(Tail01['x'], Tail01['y'], marker='.', linestyle='-', color='dodgerblue', label='Tail')

ax.set_xlabel('X', fontsize=16)
ax.set_ylabel('Y', fontsize=16)
ax.tick_params(labelsize=16)
ax.legend()

plt.grid(color='gray', which='both', linestyle=':', linewidth=0.25)
#plt.savefig(results_dir+'/'+'xyTraj.svg', fmt='svg', dpi=3000, bbox_inches='tight')
plt.savefig(results_dir+'/'+'xyTraj.png', fmt='png', dpi=300, bbox_inches='tight')
#===================================================================================================
current_path = os.getcwd()
filename1 = 'bmAc'
filename2 = 'bminAc'

active_list = glob.glob('IntSpecie1**.vtk') 
active = sorted(active_list, key=lambda x:x[-11:])
inactive_list = glob.glob('IntSpecie2**.vtk') 
inactive = sorted(inactive_list, key=lambda x:x[-11:])

try:
    os.remove(filename1+'.csv')
    os.remove(filename2+'.csv')
except(OSError, RuntimeError, TypeError, NameError):
    pass

for j in active:
    motor_noA = pd.read_csv(j, delim_whitespace=True)
    extractA = motor_noA.iloc[3:4,1:2].values
    extractA = int(np.int_(extractA))
    rowElementA = [str(extractA)]
    os.chdir(current_path)
    with open(filename1+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow(rowElementA)
        
for k in inactive:
    motor_noI = pd.read_csv(k, delim_whitespace=True)
    extractI = motor_noI.iloc[3:4,1:2].values
    extractI = int(np.int_(extractI))
    rowElementI = [str(extractI)]
    os.chdir(current_path)
    with open(filename2+'.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow(rowElementI)

bmAc = pd.read_csv(filename1+'.csv', names=['bm'])
bminAc = pd.read_csv(filename2+'.csv', names=['bm'])

mu1 = bmAc.mean()
sigma1 = np.std(bmAc)
mu2 = bminAc.mean()
sigma2 = np.std(bminAc)
#===================================================================================================
fig, ax = plt.subplots(2,2,figsize=(15,7))
plt.subplots_adjust(wspace=0.2)
plt.subplots_adjust(hspace=0.4)
#plt.axes().set_aspect('equal')

ax[0,0].set_title('Instantaneous binding active motors', fontsize=16)
ax[0,0].plot(bmAc['bm'].T, color='green')
ax[0,0].grid(color='gray', which='both', linestyle=':', linewidth=0.25)
ax[0,0].tick_params(labelsize=14)
ax[0,0].set_xlabel('Time step', fontsize=14)
ax[0,0].set_ylabel('Motor number', fontsize=14)

ax[0,1].set_title('Binding active motors: $\mu = %.2f, \sigma = %.2f$'%(mu1, sigma1), fontsize=16)
ax[0,1].hist(bmAc['bm'].T,30,normed=True, alpha=1, histtype='bar', ec='black', color='green') # change 'normed' to 'density'
ax[0,1].grid(color='gray', which='both', linestyle=':', linewidth=0.25)
ax[0,1].tick_params(labelsize=14)
ax[0,1].set_xlabel('Motor number', fontsize=14)
ax[0,1].set_ylabel('Density', fontsize=14)

ax[1,0].set_title('Instantaneous binding inactive motors', fontsize=16)
ax[1,0].plot(bminAc['bm'].T, color='blue')
ax[1,0].grid(color='gray', which='both', linestyle=':', linewidth=0.25)
ax[1,0].tick_params(labelsize=14)
ax[1,0].set_xlabel('Time step', fontsize=14)
ax[1,0].set_ylabel('Motor number', fontsize=14)

ax[1,1].set_title('Binding inactive motors: $\mu = %.2f, \sigma = %.2f$'%(mu2, sigma2), fontsize=16)
ax[1,1].hist(bminAc['bm'].T,30,normed=True, alpha=1, histtype='bar', ec='black', color='blue')
ax[1,1].grid(color='gray', which='both', linestyle=':', linewidth=0.25)
ax[1,1].tick_params(labelsize=14)
ax[1,1].set_xlabel('Motor number', fontsize=14)
ax[1,1].set_ylabel('Density', fontsize=14)

#plt.savefig(results_dir+'/'+'Mbding.svg', fmt='svg', dpi=3000, bbox_inches='tight')
plt.savefig(results_dir+'/'+'Mbding.png', fmt='png', dpi=300, bbox_inches='tight')
#===================================================================================================
v = avSpdHead01
dt = dt01

lIndex = Head01.shape[0]-2

p = 0; q = 1; df = Head01

try:
    os.remove('ub.csv')
except(OSError, RuntimeError, TypeError, NameError):
    pass

while q<lIndex:
    x0 = df.loc[p,'x']
    x1 = df.loc[q,'x']
    y0 = df.loc[p,'y']
    y1 = df.loc[q,'y']
    u = np.array([(x1-x0),(y1-y0)])
    ub = np.true_divide(u,np.sqrt((x1-x0)**2 + (y1-y0)**2))
    with open('ub.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow(ub)
    p = p+1; q = q+1
ub = pd.read_csv('ub.csv', names=['dx','dy'])

no=0

while no<lIndex+2:
  try:
    os.remove('ds'+str(no)+'.csv')
    os.remove('Ds.csv')
  except(OSError, RuntimeError, TypeError, NameError):
    pass
  no=no+1

i = 0; ii = 0; il = lIndex-1; s=0; no = 0

#dsArr = []

while il>0:
    while i<il:
        ds = np.dot(ub.loc[i],ub.loc[(i+ii)])
        with open('ds'+str(no)+'.csv','a') as fd:
            writer = csv.writer(fd)
            writer.writerow([ds])
        #dsArr.append(ds)
        i=i+1
        #print('i = ',i)
    ds = pd.read_csv('ds'+str(no)+'.csv',names=['ds']) #dsArr[no]#
    Ds = float(ds.mean()); print('Mean ds %s'%no)
    s_ = v*dt*s
    rows = np.array([s_,Ds])
    with open('Ds.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow(rows)
    i=0; ii=ii+1; il=il-1; s=s+1; no=no+1
    #print('il = ',il)
    #os.remove('ds1.csv')


# All correlation

Ds = pd.read_csv('Ds.csv',names=['s','Ds'])

plt.figure(figsize=(10,8))
plt.scatter(Ds['s'],Ds['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
plt.title(r'$S\ vs.\ <\cos\ \Delta \Theta >$ (All S)')
plt.xlabel(r'$S\ (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig(results_dir+'/'+'allPersistence.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
#===================================================================================================
t10h1 = int(np.around(Ds.shape[0]*0.1,0))
t20h1 = int(np.around(Ds.shape[0]*0.2,0))
Ds1_10th = Ds[0:t10h1]
Ds1_20th = Ds[0:t20h1]

Ds2 = Ds.drop(Ds.index[0])
Ds2 = Ds2.reset_index(drop=True)
t10h2 = int(np.around(Ds2.shape[0]*0.1,0))
t20h2 = int(np.around(Ds2.shape[0]*0.2,0))
Ds2_10th = Ds2[0:t10h2]
Ds2_20th = Ds2[0:t20h2]

# Curve fitting including correlation 1

plt.figure(figsize=(10,8))
plt.scatter(Ds1_10th['s'],Ds1_10th['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
xf = np.array(Ds1_10th['s'], dtype=float) #transform your data in a numpy array of floats 
yf = np.array(Ds1_10th['Ds'], dtype=float) #so the curve_fit can work
#curve function
def func(xf, Lp):
    return np.exp(-xf/(2*Lp))
#curve fit
popt, pcov = curve_fit(func, xf, yf)
plt.plot(xf, func(xf, *popt), color='green', label=r'Fitted Curve: $<\cos \Delta \Theta >=\exp \left(\frac{-S}{2Lp}\right), Lp = %s\ \mu m$'%np.around(popt[0],6))
#plt.text(30, 0.8, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$ (10th S with corr 1)')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig(results_dir+'/'+'curveFit1_10th.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
#===================================================================================================
# Curve fitting including correlation 1

plt.figure(figsize=(10,8))
plt.scatter(Ds1_20th['s'],Ds1_20th['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
xf = np.array(Ds1_20th['s'], dtype=float) #transform your data in a numpy array of floats 
yf = np.array(Ds1_20th['Ds'], dtype=float) #so the curve_fit can work
#curve function
def func(xf, Lp):
    return np.exp(-xf/(2*Lp))
#curve fit
popt, pcov = curve_fit(func, xf, yf)
plt.plot(xf, func(xf, *popt), color='green', label=r'Fitted Curve: $<\cos \Delta \Theta >=\exp \left(\frac{-S}{2Lp}\right), Lp = %s\ \mu m$'%np.around(popt[0],6))
#plt.text(30, 0.8, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$ (20th S with corr 1)')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig(results_dir+'/'+'curveFit1_20th.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
#===================================================================================================
# Curve fitting including correlation 2

plt.figure(figsize=(10,8))
plt.scatter(Ds2_10th['s'],Ds2_10th['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
xf = np.array(Ds2_10th['s'], dtype=float) #transform your data in a numpy array of floats 
yf = np.array(Ds2_10th['Ds'], dtype=float) #so the curve_fit can work
#curve function
def func(xf, Lp):
    return np.exp(-xf/(2*Lp))
#curve fit
popt, pcov = curve_fit(func, xf, yf)
plt.plot(xf, func(xf, *popt), color='green', label=r'Fitted Curve: $<\cos \Delta \Theta >=\exp \left(\frac{-S}{2Lp}\right), Lp = %s\ \mu m$'%np.around(popt[0],6))
#plt.text(30, 0.8, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$ (10th S)')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig(results_dir+'/'+'curveFit2_10th.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
#===================================================================================================
# Curve fitting including correlation 2

plt.figure(figsize=(10,8))
plt.scatter(Ds2_20th['s'],Ds2_20th['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
xf = np.array(Ds2_20th['s'], dtype=float) #transform your data in a numpy array of floats 
yf = np.array(Ds2_20th['Ds'], dtype=float) #so the curve_fit can work
#curve function
def func(xf, Lp):
    return np.exp(-xf/(2*Lp))
#curve fit
popt, pcov = curve_fit(func, xf, yf)
plt.plot(xf, func(xf, *popt), color='green', label=r'Fitted Curve: $<\cos \Delta \Theta >=\exp \left(\frac{-S}{2Lp}\right), Lp = %s\ \mu m$'%np.around(popt[0],6))
#plt.text(30, 0.8, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$ (20th S)')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig(results_dir+'/'+'curveFit2_20th.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()

