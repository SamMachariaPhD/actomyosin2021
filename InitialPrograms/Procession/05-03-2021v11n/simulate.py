# prepared by Sam. feel free to consult (sirmaxford@gmail.com).
import fileinput, sys, shutil, os, time, socket, subprocess, datetime

#Dt = 5e-7 -- now an input from param_set.txt
outDt = 0.01

max_comp_simulations = 11

files = ['MotilityAssayActin2MotorsParameters_v06a.f90', 'mt.f90', 'MotilityAssayActin2MotorsConfinements_v02a.f90', 'MotilityAssayActin2MotorsForce_v01a.f90', 'MotilityAssayActin2MotorsFunc_v01k.f90', 'MotilityAssayActin2MotorsOutput_v01d.f90', 'MotilityAssayActin2MotorsMain_v011n.f90', 'analysis.py', 'film1.py', 'film2.py', 'tar.py', 'untar.py']

param_file = "MotilityAssayActin2MotorsParameters_v06a.f90"

pc_hostname = socket.gethostname()
date_today = time.strftime("%d-%m-%Y")
dir_name = date_today+pc_hostname #dynamic folder based on date and PC used
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))

current_path = os.getcwd()  

run_range = range(1,max_comp_simulations+1)
simulations = int(input("\n=> Enter the total number (int) of simulations to be performed in this Computer today: "))
if simulations in run_range:
    print("\n=> %s simulations will be performed in this computer." %simulations)
else:
    sys.exit("\n=> Please enter a number (int) between 1 and %s" %max_comp_simulations)

print ("=> The current working directory is: %s" % current_path) 

try:  
    os.mkdir(dir_name)
except OSError:  
    print ("=> Creation of the directory: %s failed" % dir_name)
else:  
    print ("=> Successfully created today's simulation directory: %s\n" % dir_name)

simulation_runs = simulations
simulations_counter = 0
dir_arr = []

while simulation_runs > 0:
    params = open('param_set.txt')
    read_params = params.readlines()
    species_ratio, beads_number, ATP_value, MD_value, seed, simul_tym_sec, Dt = map(float,read_params[simulations_counter].split(',')) #dynamic parameters based on .txt file
    params.close()
    #species_ratio, beads_number, ATP_value, MD_value = map(float,input().split(',')) #Bad. I have to enter each param.
    new_dir = 'R'+str(species_ratio)+'B'+str(int(float(beads_number)))+'ATP'+str(int(float(ATP_value)))+'MD'+str(int(float(MD_value)))+'S'+str(int(float(seed)))+'T'+str(round(float(simul_tym_sec),1)) #dynamic folder name
    dir_arr.append(new_dir)
    os.chdir(dir_name)
    os.mkdir(new_dir)
    #print ("=> New folder successfully created: %s " % new_dir) #print outs for debugging
    os.chdir(current_path)
    for f in files:
        shutil.copy(f, dir_name+'/'+new_dir)
    #print ("=> Files successfully copied to the new folder:\n%s" % files)
    os.chdir(dir_name+'/'+new_dir)
    # replace all occurrences of 'ATP = 2000.0' with 'ATP = ATP_value'
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('Type1Ratio = 0.60', 'Type1Ratio = '+str(species_ratio)))
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('NumBeads = 13', 'NumBeads = '+str(int(float(beads_number))) ))
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('ATP = 2000.0', 'ATP = '+str(float(ATP_value)) ))
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('Motor_Density = 3000.0', 'Motor_Density = '+str(float(MD_value)) ))
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('seed = 273', 'seed = '+str(int(float(seed))) ))
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('dt=5.0E-7', 'dt='+str(Dt) ))    
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('NumTimeStep = 6E6', 'NumTimeStep = '+str( int( round(float(simul_tym_sec),1)/(Dt) ) ) )) # NumTimeStep = T/Dt
    for i, line in enumerate(fileinput.input(param_file, inplace=1)):
        sys.stdout.write(line.replace('OutPutDiv=2E4', 'OutPutDiv='+str( int( (outDt)/float(Dt) ) ) )) # OutPutDiv = outDt/Dt    -- outDt is declared above, usually 0.01
    #print ("\n=> Param. file in %s successfully updated." % new_dir)
    #print ("\n=> Simulation program started!: %s" % new_dir)
    subprocess.call("ifort MotilityAssayActin2MotorsParameters_v06a.f90 mt.f90 MotilityAssayActin2MotorsConfinements_v02a.f90 MotilityAssayActin2MotorsForce_v01a.f90 MotilityAssayActin2MotorsFunc_v01k.f90 MotilityAssayActin2MotorsOutput_v01d.f90 MotilityAssayActin2MotorsMain_v011n.f90", shell=True)
    #print ("=> Programs successfully compiled:\n%s " % files)
    print("\n==========----------==========-----START-----==========----------==========", file=open('pyout.txt','a'))
    print(pc_hostname, file=open('pyout.txt','a')) # PC something
    print(s.getsockname()[0], file=open('pyout.txt','a')) # IP something
    print(new_dir+' dt'+str(float(Dt)), file=open('pyout.txt','a'))
    print("Start datetime: ", file=open('pyout.txt','a'))
    print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
    tic=time.time()
    subprocess.call("ulimit -s unlimited;./a.out", shell=True)
    toc=time.time()
    tym=toc-tic
    print("\nTotal time in sec: ", file=open('pyout.txt','a'))
    print(tym, file=open('pyout.txt','a'))
    print("\nTotal time in hrs: ", file=open('pyout.txt','a'))
    print(tym/3600, file=open('pyout.txt','a'))
    print("\nTotal time in days: ", file=open('pyout.txt','a'))
    print(tym/86400, file=open('pyout.txt','a'))
    print("\nEnd datetime: ", file=open('pyout.txt','a'))
    print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
    print("\n===========----------==========-----END-----==========----------===========", file=open('pyout.txt','a'))
    print ("\n=> Programs in %s have successfully run complete!\n" % new_dir)
    simulation_runs = simulation_runs-1
    simulations_counter = simulations_counter+1 #simulation_counter for making dirs and prog. progress
    os.chdir(current_path)
    time.sleep(1)


print("\n=> All the %s simulations are successfully completed.\nDone!\n" %simulations)


for dirr in dir_arr:
    os.chdir(dir_name+'/'+dirr)
    #==============================================
    try:
        os.system('python3 analysis.py')
    except Exception as e:
        print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
        print("\nANALYSIS ERROR: ", file=open('pyout.txt','a'))
        print(e, file=open('pyout.txt','a'))
        print("Sorry, 'analysis.py' has an error.")
        pass
    #==============================================
    try:
        os.system('pvpython film1.py')
    except Exception as e:
        print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
        print("\nFILM1 ERROR: ", file=open('pyout.txt','a'))
        print(e, file=open('pyout.txt','a'))
        print("Sorry, 'film1.py' has an error.")
        pass
    #==============================================
    try:
        os.system('pvpython film2.py')
    except Exception as e:
        print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
        print("\nFILM2 ERROR: ", file=open('pyout.txt','a'))
        print(e, file=open('pyout.txt','a'))
        print("Sorry, 'film2.py' has an error.")
        pass
    #==============================================
    try:
        os.system('python3 tar.py')
    except Exception as e:
        print(datetime.datetime.now().strftime("%H:%M %d-%m-%Y"), file=open('pyout.txt','a'))
        print("\nTAR ERROR: ", file=open('pyout.txt','a'))
        print(e, file=open('pyout.txt','a'))
        print("Sorry, 'tar.py' has an error.")
        pass
    #==============================================
    os.chdir(current_path)

