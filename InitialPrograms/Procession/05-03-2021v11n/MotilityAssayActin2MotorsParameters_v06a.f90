MODULE PARAMETERS

IMPLICIT NONE


! Unit: um, sec, pN



INTEGER, PARAMETER ::		Range15 = SELECTED_INT_KIND(15), &
				DP = SELECTED_REAL_KIND(14), &
				NumAssay = 1, &
				NumFilament = 1, &
				NumBeads = 13, &
				NumType = 2, &
				MaxNumIteration=1E6, &
				AreaRenewDiv = 2E4, &
				OutPutDiv=2E4, &
				MaxInteractinNum = 1, & !Maximum Number of filaments which a complex can interact with
				seed = 273 !97845 !445 !78448 !657 !2215 !78448 !7484541 !4397 ! 242, 6990, 52804, 2072544

INTEGER(KIND = Range15), PARAMETER :: NumTimeStep = 6E6, TimeStepEquil = 1E9, MaxNumMotors = 1E6, TimeForceON = 1E9

INTEGER, PARAMETER :: MaxAreaNum = NumTimeStep/AreaRenewDiv + 1

REAL(KIND = DP), PARAMETER :: 	pi = 3.14159265358979_DP, &
				kBT = 0.0041_DP, &
				dt=5.0E-7_DP, &
				Tol=1.0E-6_DP, &
				BondLength=0.25_DP, &
				EI=0.073_DP, &						!Actin Filament (Gittes et al., JCB 1993)
				DiameterAF = 0.006_DP, &
				Motor_Density = 3000.0_DP, &
				k = 300.0_DP,& 
!
				Stepsize = 1.0E-2_DP, & 			! was 1.0E-2
				k_a = 40.0_DP, &
				k_d0 = 350.0_DP, &
				k_t = 2.0_DP, &						! /ATP[uM]
				ATP = 2000.0_DP, &					![uM]
				k_hp = 100.0_DP, &
				k_hm = 10.0_DP, &
				delta_x = -1.86E-3_DP, &
!
				F_Motor_Detach1 = 9.2_DP,&
				F_Motor_Detach2 = 9.2_DP,&
				CaptureRadius=0.020_DP, &
				Type1Ratio = 0.60_DP, &

!---External Force----------------------------------------------------
				ExtForceDensity0 = 0.0_DP, & !pN/um
				ExtForceMag = 0.0_DP, &

!---Track Surface-----------------------------------------------------
				XLimit = 500.0_DP, &

!---Track Surface-----------------------------------------------------
				HorizontalLength = DBLE(NumBeads-1)*BondLength + 1.0_DP, &
				VerticalLength = 0.5*DBLE(NumBeads-1)*BondLength + 1.0_DP

INTEGER, PARAMETER ::		OutPutDiv2 = NINT(0.0005/dt) !0.0005/dt -- output timestep for MotorStates output = 0.0005

END MODULE PARAMETERS
