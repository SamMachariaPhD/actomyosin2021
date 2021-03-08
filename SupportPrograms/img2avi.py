"""
Go inside paraview image output folder.
Search for *.png
Make *.avi out of the sorted *.png.
Regards, Sam Macharia
"""

import cv2
import numpy as np
import glob

fRate = 15
movieName = 'actoMyosin.avi'

frames = []
images = glob.glob('*.png')
images.sort()

for i in images:
    frame = cv2.imread(i); print(i)
    H, W, layers = frame.shape
    size = (W,H)
    frames.append(frame)

out = cv2.VideoWriter(movieName,cv2.VideoWriter_fourcc(*'DIVX'),fRate,size)

for j in range(len(frames)):
    out.write(frames[j])
out.release()