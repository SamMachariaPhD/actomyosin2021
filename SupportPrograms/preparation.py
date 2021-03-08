# prepared by Sam., Prof. Nitta Lab.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from termcolor import colored
from scipy.stats import norm
import matplotlib.mlab as mlab
from mpl_toolkits import mplot3d
from IPython.display import HTML
import matplotlib.animation as anim
from scipy.interpolate import spline

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 14,
        }

attach_lim = 0.12 # max z for attached filament
dt = 0.01 # change in time between rows
conf_names = ['time','x','y','z']

conf1 = pd.read_csv('Conformation_A001_r0.1.txt', names=conf_names, delim_whitespace=True)
#conf01 = conf1.drop(columns=['beads'])
conf01 = conf1.iloc[0::13,:] # jump 13 starting from the first index
conf01_df = conf01.reset_index(drop=True) # reset index to have a fresh dataframe for leading tip
#print("Conf0.1 shape before filter: ", conf01.shape)
#df01 = conf01_df.loc[conf01_df['z'] <= attach_lim] # discard dataset that have z>0.12
df01 = conf01_df.iloc[0::10, :] # jump every 10 -- coz recommended time is 0.01*10 sec
#conf01_df.to_csv('testconf.csv', encoding='utf-8', index=False)
#print("Conf0.1 shape after filter: ", df01.shape)

conf15 = pd.read_csv('Conformation_A001_r0.15.txt', names=conf_names, delim_whitespace=True)
#conf015 = conf15.drop(columns=['beads'])
conf015 = conf15.iloc[0::13,:]
conf015_df = conf015.reset_index(drop=True)
#print("Conf0.15 shape before filter: ", conf015.shape)
#df015 = conf015_df.loc[conf015_df['z'] <= attach_lim]
df015 = conf015_df.iloc[0::10, :]
#conf015_df.to_csv('testconf.csv', encoding='utf-8', index=False)
#print("Conf0.15 shape after filter: ", df015.shape)

conf2 = pd.read_csv('Conformation_A001_r0.2.txt', names=conf_names, delim_whitespace=True)
conf02 = conf2.iloc[0::13,:]
conf02_df = conf02.reset_index(drop=True)
#print("Conf0.2 shape before filter: ", conf02.shape)
#df02 = conf02_df.loc[conf02_df['z'] <= attach_lim]
df02 = conf02_df.iloc[0::10, :]
#print("Conf0.2 shape after filter: ", df02.shape)

conf25 = pd.read_csv('Conformation_A001_r0.25.txt', names=conf_names, delim_whitespace=True)
conf025 = conf25.iloc[0::13,:]
conf025_df = conf025.reset_index(drop=True)
#print("Conf0.25 shape before filter: ", conf025.shape)
#df025 = conf025_df.loc[conf025_df['z'] <= attach_lim]
df025 = conf025_df.iloc[0::10, :]
#print("Conf0.25 shape after filter: ", df025.shape)

conf3 = pd.read_csv('Conformation_A001_r0.3.txt', names=conf_names, delim_whitespace=True)
conf03 = conf3.iloc[0::13,:]
conf03_df = conf03.reset_index(drop=True)
#print("Conf0.3 shape before filter: ", conf03.shape)
#df03 = conf03_df.loc[conf03_df['z'] <= attach_lim]
df03 = conf03_df.iloc[0::10, :]
#print("Conf0.3 shape after filter: ", df03.shape)

conf35 = pd.read_csv('Conformation_A001_r0.35.txt', names=conf_names, delim_whitespace=True)
conf035 = conf35.iloc[0::13,:]
conf035_df = conf035.reset_index(drop=True)
#print("Conf0.35 shape before filter: ", conf035.shape)
#df035 = conf035_df.loc[conf035_df['z'] <= attach_lim]
df035 = conf035_df.iloc[0::10, :]
#print("Conf0.35 shape after filter: ", df035.shape)

conf4 = pd.read_csv('Conformation_A001_r0.4.txt', names=conf_names, delim_whitespace=True)
conf04 = conf4.iloc[0::13,:]
conf04_df = conf04.reset_index(drop=True)
#print("Conf0.4 shape before filter: ", conf04.shape)
#df04 = conf04_df.loc[conf04_df['z'] <= attach_lim]
df04 = conf04_df.iloc[0::10, :]
#print("Conf0.4 shape after filter: ", df04.shape)

conf45 = pd.read_csv('Conformation_A001_r0.45.txt', names=conf_names, delim_whitespace=True)
conf045 = conf45.iloc[0::13,:]
conf045_df = conf045.reset_index(drop=True)
#print("Conf0.45 shape before filter: ", conf045.shape)
#df045 = conf045_df.loc[conf045_df['z'] <= attach_lim]
df045 = conf045_df.iloc[0::10, :]
#print("Conf0.45 shape after filter: ", df045.shape)

conf5 = pd.read_csv('Conformation_A001_r0.5.txt', names=conf_names, delim_whitespace=True)
conf05 = conf5.iloc[0::13,:]
conf05_df = conf05.reset_index(drop=True)
#print("Conf0.5 shape before filter: ", conf05.shape)
#df05 = conf05_df.loc[conf05_df['z'] <= attach_lim]
df05 = conf05_df.iloc[0::10, :]
#print("Conf0.5 shape after filter: ", df05.shape)

conf55 = pd.read_csv('Conformation_A001_r0.55.txt', names=conf_names, delim_whitespace=True)
conf055 = conf55.iloc[0::13,:]
conf055_df = conf055.reset_index(drop=True)
#print("Conf0.55 shape before filter: ", conf055.shape)
#df055 = conf055_df.loc[conf055_df['z'] <= attach_lim]
df055 = conf055_df.iloc[0::10, :]
#print("Conf0.55 shape after filter: ", df055.shape)

conf6 = pd.read_csv('Conformation_A001_r0.6.txt', names=conf_names, delim_whitespace=True)
conf06 = conf6.iloc[0::13,:]
conf06_df = conf06.reset_index(drop=True)
#print("Conf0.6 shape before filter: ", conf06.shape)
#df06 = conf06_df.loc[conf06_df['z'] <= attach_lim]
df06 = conf06_df.iloc[0::10, :]
#print("Conf0.6 shape after filter: ", df06.shape)

conf65 = pd.read_csv('Conformation_A001_r0.65.txt', names=conf_names, delim_whitespace=True)
conf065 = conf65.iloc[0::13,:]
conf065_df = conf065.reset_index(drop=True)
#print("Conf0.65 shape before filter: ", conf065.shape)
#df065 = conf065_df.loc[conf065_df['z'] <= attach_lim]
df065 = conf065_df.iloc[0::10, :]
#print("Conf0.65 shape after filter: ", df065.shape)

conf7 = pd.read_csv('Conformation_A001_r0.7.txt', names=conf_names, delim_whitespace=True)
conf07 = conf7.iloc[0::13,:]
conf07_df = conf07.reset_index(drop=True)
#print("Conf0.7 shape before filter: ", conf07.shape)
#df07 = conf07_df.loc[conf07_df['z'] <= attach_lim]
df07 = conf07_df.iloc[0::10, :]
#print("Conf0.7 shape after filter: ", df07.shape)

conf75 = pd.read_csv('Conformation_A001_r0.75.txt', names=conf_names, delim_whitespace=True)
conf075 = conf75.iloc[0::13,:]
conf075_df = conf075.reset_index(drop=True)
#print("Conf0.75 shape before filter: ", conf075.shape)
#df075 = conf075_df.loc[conf075_df['z'] <= attach_lim]
df075 = conf075_df.iloc[0::10, :]
#print("Conf0.75 shape after filter: ", df075.shape)

conf8 = pd.read_csv('Conformation_A001_r0.8.txt', names=conf_names, delim_whitespace=True)
conf08 = conf8.iloc[0::13,:]
conf08_df = conf08.reset_index(drop=True)
#print("Conf0.8 shape before filter: ", conf08.shape)
#df08 = conf08_df.loc[conf08_df['z'] <= attach_lim]
df08 = conf08_df.iloc[0::10, :]
#print("Conf0.8 shape after filter: ", df08.shape)

conf85 = pd.read_csv('Conformation_A001_r0.85.txt', names=conf_names, delim_whitespace=True)
conf085 = conf85.iloc[0::13,:]
conf085_df = conf085.reset_index(drop=True)
#print("Conf0.85 shape before filter: ", conf085.shape)
#df085 = conf085_df.loc[conf085_df['z'] <= attach_lim]
df085 = conf085_df.iloc[0::10, :]
#print("Conf0.85 shape after filter: ", df085.shape)

conf9 = pd.read_csv('Conformation_A001_r0.9.txt', names=conf_names, delim_whitespace=True)
conf09 = conf9.iloc[0::13,:]
conf09_df = conf09.reset_index(drop=True)
#print("Conf0.9 shape before filter: ", conf09.shape)
#df09 = conf09_df.loc[conf09_df['z'] <= attach_lim]
df09 = conf09_df.iloc[0::10, :]
#print("Conf0.9 shape after filter: ", df09.shape)

conf95 = pd.read_csv('Conformation_A001_r0.95.txt', names=conf_names, delim_whitespace=True)
conf095 = conf95.iloc[0::13,:]
conf095_df = conf095.reset_index(drop=True)
#print("Conf0.95 shape before filter: ", conf095.shape)
#df095 = conf095_df.loc[conf095_df['z'] <= attach_lim]
df095 = conf095_df.iloc[0::10, :]
#print("Conf0.95 shape after filter: ", df095.shape)

conf10 = pd.read_csv('Conformation_A001_r1.0.txt', names=conf_names, delim_whitespace=True)
conf10 = conf10.iloc[0::13,:]
conf10_df = conf10.reset_index(drop=True)
#print("Conf1.0 shape before filter: ", conf10.shape)
#df10 = conf10_df.loc[conf10_df['z'] <= attach_lim]
df10 = conf10_df.iloc[0::10, :]
#print("Conf1.0 shape after filter: ", df10.shape)

# bm -- binding motor number, bmd -- binding motor conformation data
column_name = ['b_m']
bm_01 = pd.read_csv('binding_motors_r0.1.csv', names=column_name)
bm01 = bm_01.iloc[0::10,:]
bm01 = bm01.drop(bm01.index[30])
bmd01 = df01[['x','y']]
#bmd01 = bmd01.iloc[0::2,:]

bm_02 = pd.read_csv('binding_motors_r0.2.csv', names=column_name)
bm02 = bm_02.iloc[0::10,:]
bm02 = bm02.drop(bm02.index[30])
bmd02 = df02[['x','y']]
#bmd02 = bmd02.iloc[0::2,:]


bm_03 = pd.read_csv('binding_motors_r0.3.csv', names=column_name)
bm03 = bm_03.iloc[0::10,:]
bm03 = bm03.drop(bm03.index[30])
bmd03 = df03[['x','y']]
#bmd03 = bmd03.iloc[0::2,:]


bm_04 = pd.read_csv('binding_motors_r0.4.csv', names=column_name)
bm04 = bm_04.iloc[0::10,:]
bm04 = bm04.drop(bm04.index[30])
bmd04 = df04[['x','y']]
#bmd04 = bmd04.iloc[0::2,:]


bm_05 = pd.read_csv('binding_motors_r0.5.csv', names=column_name)
bm05 = bm_05.iloc[0::10,:]
bm05 = bm05.drop(bm05.index[30])
bmd05 = df05[['x','y']]
#bmd05 = bmd05.iloc[0::2,:]


bm_06 = pd.read_csv('binding_motors_r0.6.csv', names=column_name)
bm06 = bm_06.iloc[0::10,:]
bm06 = bm06.drop(bm06.index[30])
bmd06 = df06[['x','y']]
#bmd06 = bmd06.iloc[0::2,:]


bm_07 = pd.read_csv('binding_motors_r0.7.csv', names=column_name)
bm07 = bm_07.iloc[0::10,:]
bm07 = bm07.drop(bm07.index[30])
bmd07 = df07[['x','y']]
#bmd07 = bmd07.iloc[0::2,:]


bm_08 = pd.read_csv('binding_motors_r0.8.csv', names=column_name)
bm08 = bm_08.iloc[0::10,:]
bm08 = bm08.drop(bm08.index[30])
bmd08 = df08[['x','y']]
#bmd08 = bmd08.iloc[0::2,:]


bm_09 = pd.read_csv('binding_motors_r0.9.csv', names=column_name)
bm09 = bm_09.iloc[0::10,:]
bm09 = bm09.drop(bm09.index[30])
bmd09 = df09[['x','y']]
#bmd09 = bmd09.iloc[0::2,:]


bm_10 = pd.read_csv('binding_motors_r1.0.csv', names=column_name)
bm10 = bm_10.iloc[0::10,:]
bm10 = bm10.drop(bm10.index[30])
bmd10 = df10[['x','y']]
#bmd10 = bmd10.iloc[0::2,:]

