#!/usr/bin/env python3
# Plot persistence length graphs
# Sam Macharia

import io, csv, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import sympy as sym
plt.style.use('default')
plt.rcParams.update({'font.size': 13})

confName = 'Conformation_A001.txt'
v=7.19351; dt=0.1

Conf = pd.read_csv(confName, names=['t','x','y','z'], delim_whitespace=True)

conf1 = Conf.iloc[0::13,:]
conf1 = conf1.reset_index(drop=True)
conf2 = conf1.iloc[0::10, :]
conf2 = conf2[['x','y']]
conf = conf2.reset_index(drop=True)

conf.to_csv('conf.csv',index=False)

xmax_ = conf['x'].max(); xmin_ = conf['x'].min()
ymax_ = conf['y'].max(); ymin_ = conf['y'].min()
x1_ = (0.01*(xmax_-xmin_))+xmin_
y1_ = (0.90*(ymax_-ymin_))+ymin_
x2_ = (0.15*(xmax_-xmin_))+xmin_ 
y2_ = (0.85*(ymax_-ymin_))+ymin_

plt.figure(figsize=(10,8))
plt.plot(conf['x'],conf['y'], label='Leading tip', color='green', marker='.', linestyle='solid')
plt.text(x1_, y1_, 'avSpeed = '); plt.text(x2_, y1_, r'%.5f $\mu m/sec$'%v)
plt.xlabel('X'); plt.ylabel('Y')
plt.title('Actin Filament Leading Tip Movement'); plt.legend(loc='upper left')
plt.savefig('leadTrajectory.svg',bbox_inches='tight', format='svg', dpi=500)
plt.close()

lIndex = conf.shape[0]-2

p = 0; q = 1; df = conf

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

i = 0; ii = 0; il = lIndex-1; s=0; no = 1

while il>0:
    while i<il:
        ds = np.dot(ub.loc[i],ub.loc[(i+ii)])
        with open('ds'+str(no)+'.csv','a') as fd:
            writer = csv.writer(fd)
            writer.writerow([ds])
        i=i+1
        #print('i = ',i)
    ds = pd.read_csv('ds'+str(no)+'.csv',names=['ds'])
    Ds = float(ds.mean())
    s_ = v*dt*s
    rows = np.array([s_,Ds])
    with open('Ds.csv','a') as fd:
        writer = csv.writer(fd)
        writer.writerow(rows)
    i=0; ii=ii+1; il=il-1; s=s+1; no=no+1
    #print('il = ',il)
    #os.remove('ds1.csv')

Ds = pd.read_csv('Ds.csv',names=['s','Ds'])

plt.figure(figsize=(10,8))
plt.scatter(Ds['s'],Ds['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
plt.title(r'$S\ vs.\ <\cos\ \Delta \Theta >$')
plt.xlabel(r'$S\ (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig('allPersistence.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()

tenth = int(np.around(Ds.shape[0]/10,0)); Ds=Ds[0:tenth] #10th(10%) or 20eth(5%)

plt.figure(figsize=(10,8))
plt.scatter(Ds['s'],Ds['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig('tenthPersistence.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()

#curve fitting
plt.figure(figsize=(10,8))
plt.scatter(Ds['s'],Ds['Ds'],facecolors='none',edgecolors='b', label=r'Correlation')
xf = np.array(Ds['s'], dtype=float) #transform your data in a numpy array of floats 
yf = np.array(Ds['Ds'], dtype=float) #so the curve_fit can work
#curve function
def func(xf, Lp):
    return np.exp(-xf/(2*Lp))
#curve fit
popt, pcov = curve_fit(func, xf, yf)
plt.plot(xf, func(xf, *popt), color='green', label=r'Fitted Curve: $<\cos \Delta \Theta >=\exp \left(\frac{-S}{2Lp}\right)$')
plt.text(30, 0.8, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ <\cos \Delta \Theta >$')
plt.xlabel(r'$S (\mu m)$'); plt.ylabel(r'$<\cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig('curveFit.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
print("curveFitLp = %s micrometer" %np.around(popt[0],6))

"""
x = Ds['s']
y = np.log(Ds['Ds'])
plt.figure(figsize=(10,8))
plt.scatter(x,y,facecolors='none',edgecolors='b', label=r'lnCorrelation')
plt.title(r'$S\ vs.\ ln<cos \Delta \Theta $>')
plt.xlabel(r'$S (\mu m)$')
plt.ylabel(r'$ln<cos \Delta \Theta $>')
plt.legend(loc='best')
plt.savefig('tenthLogPersistence.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()

#line fitting
x = Ds['s']
y = np.log(Ds['Ds'])
plt.figure(figsize=(10,8))
plt.scatter(x,y,facecolors='none',edgecolors='b', label=r'lnCorrelation')
xlf = np.array(x, dtype=float) #transform your data in a numpy array of floats 
ylf = np.array(y, dtype=float) #so the curve_fit can work
#line function
def func2(xlf, Lp):
    return (-1/(2*Lp))*xlf
#line fit
popt, pcov = curve_fit(func2, xlf, ylf)
plt.plot(xf, func2(xf, *popt), color='green', label=r'Fitted Line: $ln<\cos \Delta \Theta >=\frac{-S}{2Lp}$')
plt.text(30, -1, r'$Lp = %s\ \mu m$'%np.around(popt[0],6))
plt.title(r'$S\ vs.\ ln<cos \Delta \Theta >$')
plt.xlabel(r'$S (\mu m)$')
plt.ylabel(r'$ln<cos \Delta \Theta >$')
plt.legend(loc='best')
plt.savefig('lineFit.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()
print("lineFitLp = %s micrometer" %np.around(popt[0],6))
"""

"""
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x,p(x))
x_1 = np.max(abs(x))/2 #10.0
y_ = -np.max(abs(y))/2
y_1 = slope*x_1+intercept
c_line ='y={0:.5f}x+{1:.5f}'.format(z[0],z[1])
plt.figure(figsize=(10,8))
plt.scatter(x,y, facecolors='none', edgecolors='b', label='ln<cos $\Delta \Theta $>')
plt.plot(x,p(x), color='r', label='trendline', linewidth=1, marker="_")
plt.annotate('y={0:.7f}x+{1:.7f}'.format(z[0],z[1]), xy=(x_1,y_1),xycoords='data',\
             xytext=(x_1,y_),textcoords='data',arrowprops=dict(arrowstyle="->",connectionstyle='arc3,rad=-.5'))
#plt.text(10.1,7,'r value ='); plt.text(11.6,7,r_value)
#plt.text(10.1,6.6,'p value ='); plt.text(11.66,6.6,p_value)# "%.2g" %p_value for 2dp
#plt.text(10.1,6.2,'slope std error ='); plt.text(12.83,6.2,slope_std_error)
plt.title('S vs. ln<cos $\Delta \Theta $>')
plt.xlabel('S ($\mu$m)')
plt.ylabel('ln<cos $\Delta \Theta $>')
plt.legend(loc='best')
plt.savefig('logFitPersistence.svg',bbox_inches='tight', format='svg',dip=300)
plt.close()

Lp = -1/(2*z[0])
print("Persistence Length = ",np.around(Lp,5), "micrometer")
"""
