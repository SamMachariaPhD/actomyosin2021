#!/bin/bash
# Tell git to stop tracking these files 
# Regards, Sam Macharia
git rm -rf --cached Analysis/AssayTimeSteps/*/ # subfolders inside "Analysis/AssayTimeSteps" but not files
git rm -rf --cached Analysis/ATP_Speed/*/
git rm -rf --cached Analysis/BindingMotors/*/
git rm -rf --cached Analysis/Changing_k_dt/*/
git rm -rf --cached Analysis/ContactStates/*/
git rm -rf --cached Analysis/DifferenceInFiles/*/
git rm -rf --cached Analysis/DOE/*/
git rm -rf --cached Analysis/dt_Speed/*/
git rm -rf --cached Analysis/Force_Rate/*/
git rm -rf --cached Analysis/FxnPlot/*/
git rm -rf --cached Analysis/MotorDensity_Speed/*/
git rm -rf --cached Analysis/MotorRatio_Speed/*/
git rm -rf --cached Analysis/NewLifetime/*/
git rm -rf --cached Analysis/PersistenceLength/*/
git rm -rf --cached Analysis/PullingAF/*/
git rm -rf --cached Analysis/Spring/*/
git rm -rf --cached Analysis/TangentForce/*/
git rm -rf --cached Analysis/Trajectories/*/