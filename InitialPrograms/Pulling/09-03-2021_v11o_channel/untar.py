import tarfile, glob, os, sys

toTar = ['ContactStates**.txt','Filament**.vtk','IntSpecie1**.vtk','IntSpecie2**.vtk','MotorSpecie1**.vtk','MotorSpecie2**.vtk','ds**.csv']
tarF = ['ContactStates.tar','Filament.tar','IntSpecie1.tar','IntSpecie2.tar','MotorSpecie1.tar','MotorSpecie2.tar','ds.tar']
grp = []

for u in range(0,len(tarF)):
    try:
        check_dir = glob.glob('*.tar')
        for item in check_dir:
            tar = tarfile.open(item, "r:")
            tar.extractall(); print("Extracting: %s" %item)
            tar.close()
    except: #(OSError, RuntimeError, TypeError, NameError):
        #sys.exit("\n=> Tar "+check_dir+" extraction failed")
        print("\n=> Tar "+check_dir+" extraction failed")
        pass

for g in range(0,len(toTar)):
    group = glob.glob(toTar[g])
    group = sorted(group, key=lambda x:x[-11:])
    grp.append(group)

for t in range(0,len(toTar)):
    tarGrp = []
    with tarfile.open(tarF[t], mode='r') as ta:
        for member in ta.getmembers():
            tarGrp.append(member.name)
            if tarGrp == grp[t]:
                try:
                    print("Deleting: %s" %tarF[t])
                    os.remove(tarF[t])
                except:
                    print("Error while deleting file : %s" %tarF[t])
                    pass
