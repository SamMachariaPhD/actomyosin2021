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
				OutPutDiv = 1E5, &
				MaxInteractinNum = 1, & !Maximum Number of filaments which a complex can interact with
				seed = 77 !97845 !445 !78448 !657 !2215 !78448 !7484541 !4397 ! 242, 6990, 52804, 2072544

INTEGER(KIND = Range15), PARAMETER :: NumTimeStep = 50000000, TimeStepEquil = 1E9, MaxNumMotors = 1E6, TimeForceON = 0

INTEGER, PARAMETER :: MaxAreaNum = NumTimeStep/AreaRenewDiv + 1

REAL(KIND = DP), PARAMETER :: 	pi = 3.14159265358979_DP, &
				kBT = 0.0041_DP, &
				dt= 1.0E-7_DP, &
				Tol=1.0E-6_DP, &
				BondLength=0.25_DP, &
				EI=0.073_DP, &		!EI = Lp(100um Takatsuki 2014 AF bundle estimate)*kBT !was 0.073				!Actin Filament (Gittes et al., JCB 1993)
				DiameterAF = 0.006_DP, &
				Motor_Density = 3000.0_DP, &
				Motor_Density_Upper = 3000.0_DP, &
				Motor_Density_Lower = 1000.0_DP, &
				k = 300.0_DP,& 
!
				Stepsize = 1.0E-2_DP, & 			! was 1.0E-2
				k_a = 40.0_DP, &
				k_d0 = 350.0_DP, &
				k_t = 2.0_DP, &						! /ATP[uM]
				ATP = 3000.0_DP, &					![uM]
				k_hp = 100.0_DP, &
				k_hm = 10.0_DP, &
				delta_x = -1.86E-3_DP, &
!
				F_Motor_Detach1 = 9.2_DP,&
				F_Motor_Detach2 = 9.2_DP,&
				CaptureRadius=0.020_DP, &
				Type1Ratio = 1.00_DP, &

!---External Force----------------------------------------------------
				ExtForceDensity0 = -0.0_DP, & !pN/um
				ExtForceMag = 0.0_DP, &

!---Track Surface-----------------------------------------------------
				XLimit = 500.0_DP, &

!---Track Surface-----------------------------------------------------
				ChannelWidth = 5.0_DP, &
				HorizontalLength = DBLE(NumBeads-1)*BondLength + 1.0_DP, &
				VerticalLength = 0.25_DP*DBLE(NumBeads-1)*BondLength + 1.0_DP
!				VerticalLength = 2.5_DP*ChannelWidth

INTEGER, PARAMETER ::		OutPutDiv2 = 1E5	!0.0005/dt

END MODULE PARAMETERS
