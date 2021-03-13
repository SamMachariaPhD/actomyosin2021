#! /bin/bash
pwd
cd ./test1
pwd


ifort MotilityAssayActin2MotorsParameters_v06c.f90 mt.f90 MotilityAssayActin2MotorsSubstrate_v01a.f90 MotilityAssayActin2MotorsForce_v01a.f90 \
        MotilityAssayActin2MotorsFunc_v01L.f90 MotilityAssayActin2MotorsOutput_v01d.f90 MotilityAssayActin2MotorsMain_v011p.f90


cd ../
