# Tar files in the list
# Regards, Sam Macharia

import tarfile, glob, os, sys
#============================================
toTar = ['ContactStates**.txt','Filament**.vtk','IntSpecie1**.vtk','IntSpecie2**.vtk','MotorSpecie1**.vtk','MotorSpecie2**.vtk',\
    'MTPlusEnd**.vtk','ds**.csv','MotorSpecie1_**.csv','MotorSpecie2_**.csv','Filament_**.csv','Specie1_**.csv','Specie2_**.csv',\
        'ActivePos_**.csv','InactivePos_**.csv']
tarF = ['ContactStates.tar','Filament.tar','IntSpecie1.tar','IntSpecie2.tar','MotorSpecie1.tar','MotorSpecie2.tar','MTPlusEnd.tar',\
    'ds.tar','MotorSpecie1_csv.tar','MotorSpecie2_csv.tar','Filament_csv.tar','Specie1_csv.tar','Specie2_csv.tar','ActivePos_csv.tar','InactivePos_csv.tar']
grp = []
#============================================
for g in range(0,len(toTar)):
    group = glob.glob(toTar[g])
    group = sorted(group, key=lambda x:x[-11:])
    grp.append(group)
#============================================
for t in range(0,len(toTar)):
    try:
        with tarfile.open(tarF[t], mode='w') as tar:
            for file in grp[t]:
                tar.add(file); print("Tarred: %s" %file)
    except (OSError, RuntimeError, TypeError, NameError):
        print("\n=> "+ tarF[t] +" was not created.")
        #sys.exit("\n=> Tar creation failed")
        pass
#============================================
for t in range(0,len(toTar)):
    tarGrp = []
    with tarfile.open(tarF[t], mode='r') as ta:
        for member in ta.getmembers():
            tarGrp.append(member.name)
            if tarGrp == grp[t]:
                for filePath in grp[t]:
                    try:
                        print("Deleting: %s" %filePath)
                        os.remove(filePath)
                    except:
                        print("Error while deleting file : %s" %filePath)
                        pass
#============================================
