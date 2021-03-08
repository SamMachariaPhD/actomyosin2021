#!/usr/bin/env python
# coding: utf-8
#
# Get output data from bindingLifetime.py.
# Exclude unwanted motors (motors not in question).
# Make a movie using the binding motors in question.
# Regards, Sam Macharia


import numpy as np
import pandas as pd
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os, glob, time, cv2


# Preparation.
results_dir = 'lifetimeMovie'
try:  
    os.mkdir(results_dir)
except OSError:  
    print ("=> Creation of the directory: %s failed" % results_dir)
else:  
    print ("=> Successfully created %s directory." % results_dir)
Ts = 501
segments = 12 # beads = 13
r = '0.8'
dt = 0.01
#====================================================================================================



# Load necessary files.
fil = []
for i in range(Ts):
    fil_ = pd.read_csv('Filament_5s133R0.8Ts'+str(i)+'.csv', names=['x','y','z'], skiprows=1) 
    fil.append(fil_)
m1r_Ag_upd = pd.read_csv('lyf8_active_label_life.csv')
m2r_Ag_upd = pd.read_csv('lyf10_defective_label_life.csv')
#====================================================================================================



# Cuf off unwanted binding motors, sort, and clean up.
m1lyfCutOff = round(m1r_Ag_upd['life'].mean(), 0)
m2lyfCutOff = round(m2r_Ag_upd['life'].mean(), 0)
m1r_Ag_upd = m1r_Ag_upd[m1r_Ag_upd.life >= m1lyfCutOff] # desired cutoff lifetime
m2r_Ag_upd = m2r_Ag_upd[m2r_Ag_upd.life >= m2lyfCutOff]
m1r_Ag_upd = m1r_Ag_upd.sort_values(['Ts'], ascending=[True])
m2r_Ag_upd = m2r_Ag_upd.sort_values(['Ts'], ascending=[True])
m1r_Ag_u = m1r_Ag_upd.set_index('Ts')
m2r_Ag_u = m2r_Ag_upd.set_index('Ts')
#====================================================================================================



# Plot each timestep.
plt.style.use('ggplot')
#idx = 19
i=0
unplottedA = []
unplottedI = []
while i < Ts:
    for idx in range(i,i+1):
        fig, ax = plt.subplots(figsize=(10,8))

        ax.plot(fil[idx]['x'],fil[idx]['y'], marker='o', color='red', markerfacecolor='None', linestyle='-', linewidth=2, label='Actin')
        ax.scatter(fil[idx]['x'][0],fil[idx]['y'][0], marker='D', color='black', label='Leading tip')
        try:
            ax.scatter(m1r_Ag_u.loc[idx]['x'], m1r_Ag_u.loc[idx]['y'], marker='o', color='lightgreen', label='Active')
        except Exception as e:
            unplottedA.append(e)
        try:
            ax.scatter(m2r_Ag_u.loc[idx]['x'], m2r_Ag_u.loc[idx]['y'], marker='o', color='blue', label='Defective') # aggressive
        except Exception as e:
            unplottedI.append(e)
        ax.set_xticks(np.arange(0.4,6.1,0.4))
        ax.set_yticks(np.arange(-2.0,2.4,0.4))
        
        ax.minorticks_on()
        ax.tick_params('both', direction='in', top=True, right=True, length=9, width=0.5, which='major') #
        ax.tick_params('both', direction='in', top=True, right=True, length=4, width=0.4, which='minor') #

        ax.set_xlabel('X ($\mu m$)', fontsize=15) #
        ax.set_ylabel('Y ($\mu m$)', fontsize=15) #
        
        ax.text(0.95,-0.06,'@NittaLab', color='grey', horizontalalignment ='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_aspect('equal') #
        ax.legend(loc = 'upper left')

        if i <10:
            ax.set_title('R = '+r+' | Def. life $\geq$ '+str(m2lyfCutOff*dt)+' sec | Act. life $\geq$ '+str(m1lyfCutOff*dt)+' sec | Ts: 00%s'%i, fontsize=16) # > mean
            plt.savefig(results_dir+'/'+'00'+str(i)+'.png', fmt='.png', dpi=500, bbox_inches='tight')
        if i >9 and i <100:
            ax.set_title('R = '+r+' | Def. life $\geq$ '+str(m2lyfCutOff*dt)+' sec | Act. life $\geq$ '+str(m1lyfCutOff*dt)+' sec | Ts: 0%s'%i, fontsize=16) # > mean
            plt.savefig(results_dir+'/'+'0'+str(i)+'.png', fmt='.png', dpi=500, bbox_inches='tight')
        if i >99 and i < Ts:
            ax.set_title('R = '+r+' | Def. life $\geq$ '+str(m2lyfCutOff*dt)+' sec | Act. life $\geq$ '+str(m1lyfCutOff*dt)+' sec | Ts: %s'%i, fontsize=16) # > mean
            plt.savefig(results_dir+'/'+str(i)+'.png', fmt='.png', dpi=500, bbox_inches='tight')

        plt.close()
    i+=1

#plt.show()
plt.close()
#====================================================================================================



# Make a movie.
fRate = 15
start = 0
dx = 50
for film in range(10):
    movieName = results_dir+'/DefectiveActiveAggressiveTs'+str(start)+'_'+str(start+dx)+'.avi'

    frames = []
    images = glob.glob(results_dir+'/*.png')
    images = sorted(images, key=lambda x:x[-7:])
    images = images[start:start+dx]

    for i in images:
        frame = cv2.imread(i)#; print(i)
        H, W, layers = frame.shape
        size = (W,H)
        frames.append(frame)

    out = cv2.VideoWriter(movieName,cv2.VideoWriter_fourcc(*'DIVX'),fRate,size)

    for j in range(len(frames)):
        out.write(frames[j])
    out.release()
    start+=dx
    time.sleep(15)
#====================================================================================================
