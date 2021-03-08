# How to use simulate.py
# Regards, Sam Macharia

# METHOD 1 -- full auto
#--------------------------------------------------------
> ssh (do it with -X permissions) into the ubuntu (16.04) computer you want to run simulation:
    $ ssh -X 10.226.27.26 -l nitta
> Make a new folder where you want your simulation to run in.
> Copy all the 12 files into that new folder:
    param_set.txt, simulate.py, plot.py, film.py, autocomp_py.sh, autorun_py.sh, 
    ...Parameters... .f90, ...Confinements... .f90, ...Functions... .f90,
    ...Deformation... .f90, ...Main... .f90, mt.f90
> Open the 'param_set.txt' file and set the desired parameters as instructed in that file. Save changes.
> simulate.py is, by default, set to run 5 simulations max. at a go. 
> To change to x simulations, edit line 5 'max_comp_simulations = 5' to 'max_comp_simulations = x' where x=integer.
> If you change the simulation Dt in parameters... .f90, change also the Dt in the simulate.py

> Open terminal in that folder or $ cd into that folder.
> Ensure that ifortran is installed.
    $ ifort --version
> Ensure that the 'autocomp_py.sh' and 'autorun_py.sh' have execute permissions:
    $ chmod -x autocomp_py.sh
    $ chmod -x autorun_py.sh
> Ensure that you have python 2 and 3 installled:
    $ python2 --version
    $ python3 --version
> Run the following commands:
    $ sudo apt-get install python3-numpy
    $ sudo apt-get install python3-matplotlib
    $ sudo apt-get install python3-pandas
    $ sudo apt-get install python3.5-tk
    $ sudo apt-get install python-pandas
    $ sudo apt-get install paraview
    $ pvpython --version

> Run python3: '$ python3'.
> Test if all the required libraries can import without error:
    >>> import fileinput, sys, shutil, os, time, socket, subprocess
    >>> import matplotlib; matplotlib.use('Agg') 
    >>> import matplotlib.pyplot as plt; import pandas as pd; import numpy as np
> If there is an error, quit python3 and install the above libraries. For example:
    $ sudo apt-get install python3-pandas
> Run pvpython: '$ pvpython'.
> Test if all the required libraries can import without error:
    >>> import fileinput, sys, shutil, os, time, socket, subprocess, glob
    >>> from paraview.simple import *
    >>> import pandas as pd
> If there is an error, quit pvpython and install the above libraries. For example:
    $ sudo apt-get install paraview

> To run simulations, run '$ python3 simulate.py'

> To ONLY do plots or make a film, copy the plot.py/film.py into the folder containing:
    The 'TipXY_A001.txt' file
    ALL 'Filament**.vtk' files
    ALL 'MotorSpecie1**0.vtk' files
    ALL 'MotorSpecie1**0.vtk' files
> Run '$ python3 plot.py' to do plot.
> Run '$ pvpython film.py' to make a film.

# METHOD 2 -- semi auto
#--------------------------------------------------------
For slightly faster and safe runs free from network breakdowns,
> Run simulate.py as above
> Once a.out is produced and the simulation seems to run as expected, 
> Stop the simulation, copy and rename a.out as you wish, say, R07ATP2000.out
> $ ssh 10.226.27.26 -l nitta NOT $ ssh -X 10.226.27.26 -l nitta (Do not use the -X option)
> Run the following command and close the terminal
> $ ulimit -s unlimited; ./R07ATP2000.out &
> "&" will make sure that the program is running in the background of that computer
> Open a different terminal and run $ top
> Make sure you can see the program running
> After the program is complete, run the appropriate analysis.py scripts
> You may run as many as programs as you can depending on the available memory displayed on $ top (<25%)



#====================ADDITIONAL NOTES===================

> Converting jupyter notebook to html file:
    $ jupyter nbconvert --to html mynotebook.ipynb



#----------------------END--------------------