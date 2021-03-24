#! /bin/bash
pwd
cd ./test1
pwd


#---------------------------------------------------------------------


ulimit -s unlimited

time ./a.out



aa=1
while test $aa -le 10
do

	if test $aa -le 9
	then
	aa=00$aa
	elif test $aa -le 99
	then
	aa=0$aa
	fi

	tar cfz Filament_A$aa.tar.gz Filament_A$aa*.vtk
	tar cfz MabikiFilament_A$aa.tar.gz Filament_A$aa*0.vtk

	tar cfz PlusEnd_A$aa.tar.gz PlusEnd_A$aa*.vtk
	tar cfz MabikiPlusEnd_A$aa.tar.gz PlusEnd_A$aa*0.vtk


	tar cfz Motor_A$aa.tar.gz Motor_A$aa*.vtk
	tar cfz MabikiMotor_A$aa.tar.gz Motor_A$aa*0.vtk

#	tar cfz AllKinesin_A$aa.tar.gz AllKinesin_A$aa*.vtk
#	tar cfz MabikiAllKinesin_A$aa.tar.gz AllKinesin_A$aa*0.vtk


	tar cfz IntMotor_A$aa.tar.gz IntMotor_A$aa*.vtk
	tar cfz MabikiIntMotorA$aa.tar.gz IntMotor_A$aa*0.vtk


	tar cfz ContactStates_A$aa.tar.gz ContactStates_A$aa*



#	echo $aa
	aa=$(expr $aa + 1)

done
rm Filament_A*.vtk
rm PlusEnd_A*.vtk
rm Motor_A*.vtk
rm IntMotor_A*.vtk
rm ContactStates_A*.txt



#---------------------------------------------------------------------


cd ../
