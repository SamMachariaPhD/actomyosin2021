# Prepare the simulation video
# Regards Sam Macharia
import fileinput, sys, shutil, os, time, socket, subprocess, glob
from paraview.simple import *
import pandas as pd

conf = pd.read_csv('Conformation_A001.txt', names=['time','x','y','z'], delim_whitespace=True)

head = 0; headO = 0
tail = 13; tailO = 13
beads = 13
steps = 100
simTym = int( (conf.shape[0]/beads)/steps ) # sec.
tStep = simTym*steps

columns = ['time', 'x_tip', 'y_tip']
df = pd.read_csv('TipXY_A001.txt', names=columns, delim_whitespace=True)
x_max = df['x_tip'].max(); x_min = df['x_tip'].min()
y_max = df['y_tip'].max(); y_min = df['y_tip'].min()

results_dir = 'ANALYSIS'
film_name = 'filament_film1'

try:  
    os.mkdir(results_dir)
except OSError:  
    print ("=> Creation of the directory: %s failed" % results_dir)
else:  
    print ("=> Successfully created %s directory." % results_dir)


Filament_file_list = glob.glob('Filament**.vtk') # all files starting with 'Filament' and ending with '.vtk'
IntSpecie1_file_list = glob.glob('IntSpecie1**.vtk')
IntSpecie2_file_list = glob.glob('IntSpecie2**.vtk')
MotorSpecie1_file_list = glob.glob('MotorSpecie1**.vtk')
MotorSpecie2_file_list = glob.glob('MotorSpecie2**.vtk')
MTPlusEnd_file_list = glob.glob('MTPlusEnd**.vtk')

filament_files = sorted(Filament_file_list, key=lambda x:x[-16:]) # sort by the last 16 characters of the file name
IntSpecie1_files = sorted(IntSpecie1_file_list, key=lambda x:x[-16:])
IntSpecie2_files = sorted(IntSpecie2_file_list, key=lambda x:x[-16:])
MotorSpecie1_files = sorted(MotorSpecie1_file_list, key=lambda x:x[-16:])
MotorSpecie2_files = sorted(MotorSpecie2_file_list, key=lambda x:x[-16:])
MTPlusEnd_files = sorted(MTPlusEnd_file_list, key=lambda x:x[-16:])

#paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
Filaments = LegacyVTKReader(FileNames=filament_files)
IntSpecie1 = LegacyVTKReader(FileNames=IntSpecie1_files)
IntSpecie2 = LegacyVTKReader(FileNames=IntSpecie2_files)
MotorSpecie1 = LegacyVTKReader(FileNames=MotorSpecie1_files)
MotorSpecie2 = LegacyVTKReader(FileNames=MotorSpecie2_files)
MTPlusEnd = LegacyVTKReader(FileNames=MTPlusEnd_files)

animationScene1 = GetAnimationScene() # get animation scene

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

renderView1 = GetActiveViewOrCreate('RenderView') # get active view
renderView1.ViewSize = [1546, 860] # set a specific view size

# get camera animation track for the view
#cameraAnimationCue1 = GetCameraTrack(view=renderView1)

renderView1.AxesGrid.Visibility = 1
renderView1.UseTexturedBackground = 0
renderView1.OrientationAxesVisibility = 1
#===================================================================================================
# set active source
SetActiveSource(Filaments)
FilamentsDisplay = Show(Filaments, renderView1) # show data in view
FilamentsDisplay.ColorArrayName = [None, ''] # trace defaults for the display properties.
FilamentsDisplay.GlyphType = 'Arrow'
FilamentsDisplay.ScalarOpacityUnitDistance = 3.0
FilamentsDisplay.LineWidth = 3.3
FilamentsDisplay.DiffuseColor = [1.0, 0.0, 0.0]
FilamentsDisplay.Opacity = 1.0

SetActiveSource(IntSpecie1)
IntSpecie1Display = Show(IntSpecie1, renderView1)
IntSpecie1Display.ColorArrayName = [None, '']
IntSpecie1Display.GlyphType = 'Arrow'
IntSpecie1Display.ScalarOpacityUnitDistance = 1.1290635824750306
IntSpecie1Display.DiffuseColor = [0.0, 0.6666666666666666, 0.0]
IntSpecie1Display.PointSize = 2.0
IntSpecie1Display.Opacity = 1.0

SetActiveSource(IntSpecie2)
IntSpecie2Display = Show(IntSpecie2, renderView1)
IntSpecie2Display.ColorArrayName = [None, '']
IntSpecie2Display.GlyphType = 'Arrow'
IntSpecie2Display.ScalarOpacityUnitDistance = 1.359827204011562
IntSpecie2Display.DiffuseColor = [0.0, 0.0, 1.0]
IntSpecie2Display.PointSize = 2.0
IntSpecie2Display.Opacity = 1.0

SetActiveSource(MotorSpecie1)
MotorSpecie1Display = Show(MotorSpecie1, renderView1)
MotorSpecie1Display.ColorArrayName = [None, '']
MotorSpecie1Display.GlyphType = 'Arrow'
MotorSpecie1Display.ScalarOpacityUnitDistance = 0.17092807973526433
MotorSpecie1Display.DiffuseColor = [0.0, 0.6666666666666666, 0.0]
MotorSpecie1Display.PointSize = 2.0
MotorSpecie1Display.Opacity = 0.1

SetActiveSource(MotorSpecie2)
MotorSpecie2Display = Show(MotorSpecie2, renderView1)
MotorSpecie2Display.ColorArrayName = [None, '']
MotorSpecie2Display.GlyphType = 'Arrow'
MotorSpecie2Display.ScalarOpacityUnitDistance = 0.22681864097717136
MotorSpecie2Display.DiffuseColor = [0.0, 0.0, 1.0]
MotorSpecie2Display.PointSize = 2.0
MotorSpecie2Display.Opacity = 0.1

SetActiveSource(MTPlusEnd)
MTPlusEndDisplay = Show(MTPlusEnd, renderView1)
MTPlusEndDisplay.ColorArrayName = [None, '']
MTPlusEndDisplay.GlyphType = 'Arrow'
MTPlusEndDisplay.ScalarOpacityUnitDistance = 0.0
MTPlusEndDisplay.DiffuseColor = [0.0, 0.0, 0.0]
MTPlusEndDisplay.PointSize = 3.5
MTPlusEndDisplay.Opacity = 1.0

annotateTime1 = AnnotateTime()
SetActiveSource(annotateTime1)
annotateTime1Display = Show(annotateTime1, renderView1)
annotateTime1Display.FontSize = 12
annotateTime1Display.FontFamily = 'Courier'
annotateTime1Display.WindowLocation = 'LowerLeftCorner'
# Properties modified on annotateTime1Display
#annotateTime1Display.WindowLocation = 'AnyLocation'
annotateTime1.Format = 'Tstep: %.0f (' + str(simTym) + ' sec)'
annotateTime1Display = Show(annotateTime1, renderView1)

# create a new 'Text'
text1 = Text()
text1.Text = '@NittaLab'
text1Display = Show(text1, renderView1)
text1Display.FontFamily = 'Courier'
text1Display.FontSize = 5
text1Display.WindowLocation = 'LowerRightCorner'
text1Display.Shadow = 1
text1Display.Color = [0.3333333333333333, 1.0, 1.0]
text1Display.Justification = 'Right'
text1Display.Opacity = 0.7
text1Display.Bold = 0
#===================================================================================================
# current camera placement for renderView1
#renderView1.CameraPosition = [5.566566450844984, -3.271004214234651, 18.733021468562196]
#renderView1.CameraFocalPoint = [5.566566450844984, -3.271004214234651, 0.012500000186264515]
# reset view to fit data
renderView1.ResetCamera(0.0,x_max,y_min,0.0,x_min,y_max)
renderView1.CameraParallelScale = 1.5

# save animation images/movie
WriteAnimation(results_dir+'/'+film_name+'.avi', Magnification=1, FrameRate=10.0, Quality=70, Compression=True)
