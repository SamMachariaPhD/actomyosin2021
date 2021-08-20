#!/usr/bin/env python
# coding: utf-8
# Get x,y trajectory data, output a path persistence length plot
# Regards, Sam Macharia

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os
plt.style.use("ggplot")
cm = 1/2.54

conf = pd.read_csv('data/Conformation_A001r1.txt', names=['t','x','y','z'], delim_whitespace=True)

beads = 13
jmp = 10

tip = conf[0::beads]
tip = tip[0::jmp]

# $|b_1| = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$

xdiff = np.diff(tip['x'])
ydiff = np.diff(tip['y'])
b = np.sqrt(xdiff**2 + ydiff**2)

# $U_{b1} = \frac{1}{|b_1|} \times ((x_2-x_1), (y_2-y_1))$

ub = pd.DataFrame({'ubx':xdiff/b, 'uby':ydiff/b})


# for $\Delta s = 1$, calculate $<cos \Delta \theta(1)>$: <br>
# mean of $Ub_1\cdot Ub_{1+1} + Ub_2\cdot Ub_{2+1} + Ub_3\cdot Ub_{3+1} + \cdots + Ub_{L-1}\cdot Ub_L$ <br>
# 
# for $\Delta s = 2$, calculate $<cos \Delta \theta(2)>$: <br>
# mean of $Ub_1\cdot Ub_{1+2} + Ub_2\cdot Ub_{2+2} + Ub_3\cdot Ub_{3+2} + \cdots + Ub_{L-2}\cdot Ub_L$ <br>
# 
# Persistence length = plot(s,mean of Ubs)

#=======================================================================================
_ = []; ds = []; dsm = []; s = []; c = 0

try:
    os.remove('ds_ub_status.txt')
except:
    print("'ds_ub_status.txt' does not exist.")

for i in range(len(ub)-1):
    print("Ds = %s"%i, file=open('ds_ub_status.txt','a'))
    for j in range(len(ub)-1):
        try:
            _.append(np.dot(ub.loc[j].values,ub.loc[j+i].values))
            print("Ub%s.Ub%s"%(j,j+i), file=open('ds_ub_status.txt','a'))
        except:
            pass #print("No: Ub%s.Ub%s"%(j,j+i))
    ds.append(_)
    dsm.append(np.mean(_))
    s.append(c)
    _ = [] # empty this bucket
    c+=1

s = np.array(s)
dsm = np.array(dsm)
#=======================================================================================

fig, ax = plt.subplots(1,1, figsize=(10*cm,10*cm))
ax.plot(s,dsm, marker='o', c='r', ls='--', lw=1, markerfacecolor='lime')

ax.set_xlabel(r'$\Delta s$', fontsize=14)
ax.set_ylabel(r'$\langle cos(\Delta \theta)(s) \rangle$', fontsize=14)
plt.show()

