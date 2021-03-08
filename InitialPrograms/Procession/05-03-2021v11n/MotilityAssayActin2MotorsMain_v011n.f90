PROGRAM MAIN
	
	
	USE PARAMETERS
	USE mtmod
	USE FUNC
	USE OUTPUT
	
	USE PLANAR_TRACK_CONFINEMENT
	USE UNIFORM_FORCE_X
	
	
	
	IMPLICIT NONE
	

	INTEGER	:: seed_Assay, I_Assay, I, J, AreaCounter, EraseCounter, NumIteration, &
		OutputfileCounter, UnitNumConformation, UnitNumTipXY, UnitNumMotorStates, UnitNumAreaEraseCounter

	INTEGER(KIND = Range15):: TS, IM, ActiveMotorIdxOffset, ActiveMotorIdxEnd
	
	INTEGER(KIND = Range15), DIMENSION(MaxAreaNum) :: AddedMotorNum
	
	INTEGER, DIMENSION(MaxNumMotors) :: 	Release_ADP, &
											MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)
	
	REAL(KIND = DP) ::	IniAngle, UR1, UR2, UR3, gamma_Bead, D_Bead, XCM, YCM
	
	REAL(KIND = DP), DIMENSION(MaxAreaNum) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy
	
	REAL(KIND = DP), DIMENSION(NumBeads) :: XI, YI, ZI, XI_temp, YI_temp, ZI_temp, &
				FIx, FIy, FIz, &
				NormRandVector4Beads, XINormRandVector4Beads, YINormRandVector4Beads, ZINormRandVector4Beads
	
	REAL(KIND = DP), DIMENSION(MaxNumMotors) :: XM, YM, ZM, Elongation
	
	REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors) :: ContactState, TempContact
	
	REAL(KIND = DP), DIMENSION(MaxNumMotors) :: F_Motor_X, F_Motor_Y, F_Motor_Z
	
	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: X, Y, Z, Fx, Fy, Fz, Force_Bead_X, Force_Bead_Y, Force_Bead_Z, &
				XNormRandVector4Beads, YNormRandVector4Beads, ZNormRandVector4Beads
	
	LOGICAL :: StateConstraint, StatConfinement

	LOGICAL, DIMENSION(MaxNumMotors) :: MotorStateUpdate

	CHARACTER(LEN=30) :: OutFileName
	
	

	
	seed_Assay = seed
	
	!---Calculating Parameters
	
	gamma_Bead = 3.0_DP*pi*0.001_DP*BondLength/DLOG(BondLength/DiameterAF)
	D_Bead = kBT/gamma_Bead
	
	
			
	!---Output chamber boundary in vtk format--------------------------------
	!CALL OutputBoundary
	
	OPEN(10,FILE='InitialCondition.txt')
	
	
	!---Repeat Assay------------------------------------------------------
	
	Loop_Assay: DO I_Assay=1, NumAssay
	
	
	!---Assay Initial Condition-------------------------------------------
	
	CALL sgrnd(seed_Assay)
	
	TS = 0
	ActiveMotorIdxOffset = 0
	ActiveMotorIdxEnd = 0
		
	AreaCounter = 1
	EraseCounter = 0
	
	OutputfileCounter = 0
	

	XM = -100.0_DP
	YM = 5.0_DP
	ZM = 0.0_DP
	
	Release_ADP = 0
	
	!UR1 = grnd()
	!IniAngle = 2.0_DP*pi*UR1
	IniAngle = 0.0_DP*pi
	
	
	WRITE(10,'(I3,I7,F15.10)') I_Assay, seed_Assay, IniAngle
	
	
	seed_Assay = seed_Assay+1
	

	!---OPEN OUTPUT FILE-----------------------------------------------------
	
	!!! Unit = #33 for VTK file outputs

	WRITE(OutFileName,'(A,I3.3,A)') 'ForCheck_A', I_Assay, '.txt'		! Output file for checking the program
	OPEN(20,FILE=OutFileName)											! Output file for checking the program

	UnitNumConformation = 11
	WRITE(OutFileName,'(A,I3.3,A)') 'Conformation_A', I_Assay, '.txt'
	OPEN(UnitNumConformation,FILE=OutFileName)
	
	UnitNumTipXY = 12
	WRITE(OutFileName,'(A,I3.3,A)') 'TipXY_A', I_Assay, '.txt'
	OPEN(UnitNumTipXY,FILE=OutFileName)
	
	UnitNumMotorStates = 13
	WRITE(OutFileName,'(A,I3.3,A)') 'MotorStates_A', I_Assay, '.txt'
	OPEN(UnitNumMotorStates,FILE=OutFileName)
	
	UnitNumAreaEraseCounter = 14
	WRITE(OutFileName,'(A,I3.3,A)') 'AreaEraseCounter_A', I_Assay, '.txt'
	OPEN(UnitNumAreaEraseCounter,FILE=OutFileName)
	
	
	!---Initial Conformation of Filaments-----------------------------
	
	DO I=1, NumFilament
	
		X(NumBeads,I) = 0.0_DP
		Y(NumBeads,I) = 0.0_DP
		Z = 0.0125_DP
	
		DO J=NumBeads-1, 1, -1
	
			X(J,I) = X(J+1,I) + BondLength*DCOS(IniAngle)
			Y(J,I) = Y(J+1,I) + BondLength*DSIN(IniAngle)
	
		END DO
	END DO
		
	
	!---Initial Motor Location-----------------------------------------
	
	CALL InitialMotorLocations(ActiveMotorIdxOffset, ActiveMotorIdxEnd, IniAngle, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
	!---Filament-Motor Contact--------------------------------------------
	
	TempContact = 0.0_DP
	DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
		CALL CheckMotorFilamentProximity(X, Y, Z, XM(IM), YM(IM), ZM(IM), ContactState(:,IM), TempContact(:,IM))
	END DO
	CALL InitialMotorBinding(ActiveMotorIdxOffset, ActiveMotorIdxEnd, ContactState, TempContact)
	
	
	!---Calculating Forces upon Motors and Beads---------------
	
	CALL CalculateForceMotor(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, ContactState, F_Motor_X, F_Motor_Y, F_Motor_Z, Elongation)
	CALL CalculateForceBead(ActiveMotorIdxOffset, ActiveMotorIdxEnd, ContactState, Force_Bead_X, Force_Bead_Y, Force_Bead_Z, F_Motor_X, F_Motor_Y, F_Motor_Z)
	
	
	!---Calculating Forces upon Beads-------------------------------------
	
	Fx=Force_Bending(X) + Force_Bead_X + ExtF_X(TS, X, Y, Z)
	Fy=Force_Bending(Y) + Force_Bead_Y + ExtF_Y(TS, X, Y, Z)
	Fz=Force_Bending(Z) + Force_Bead_Z + ExtF_Z(TS, X, Y, Z)	
	
	
	!---Output Area & Erase Counters--------------------------------------
	
	WRITE(UnitNumAreaEraseCounter,*) TS, AreaCounter, EraseCounter

	
	!---Various Outputs-------------------------------
	
	CALL OutputConformation(UnitNumConformation,TS,X,Y,Z)
	CALL OutputTipXY(UnitNumTipXY,TS,X,Y)
	CALL OutputMotorStates(UnitNumMotorStates, TS, ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, F_Motor_X, F_Motor_Y, F_Motor_Z, ContactState, MotorType)
	CALL OutputFilamentVTK(I_Assay, OutputfileCounter, X, Y, Z)
	CALL OutputFilamentPlusEndVTK(I_Assay, OutputfileCounter, X, Y, Z)		
	CALL OutputContactState(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState)
	CALL OutputIntMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState, XM, YM, ZM)		
	CALL OutputMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, XM, YM, ZM)	


!---End of Initial Setting------------------------------------------------------------------
	
	

!---Start of Time Evolution----------------------------------------------------
	
	Loop_Time: DO TS=1, NumTimeStep
	
	
!!--Update of Motor States-----------------------------------------------------
	
	TempContact = 0.0_DP
	MotorStateUpdate = .FALSE.
	DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd

!---Forced Detachment of Bound Motors---------------------------------------
		IF (ContactState(1,IM) >= 1.0_DP) THEN

			CALL MotorForcedDetachment(F_Motor_X(IM), F_Motor_Y(IM), F_Motor_Z(IM), ContactState(:,IM), Release_ADP(IM), Elongation(IM), MotorType(IM), MotorStateUpdate(IM))
!			CALL MotorForcedDetachmentRate(F_Motor_X(IM), F_Motor_Y(IM), F_Motor_Z(IM), ContactState(:,IM), Release_ADP(IM), Elongation(IM), MotorType(IM), MotorStateUpdate(IM))
!            CALL MotorForcedDetachmentRateWithCheck(TS, F_Motor_X(IM), F_Motor_Y(IM), F_Motor_Z(IM), ContactState(:,IM), Release_ADP(IM), Elongation(IM), MotorType(IM), MotorStateUpdate(IM))

!---Filament-Motor Binding--------------------------------------------------
        ELSE IF (NINT(ContactState(1,IM)) == 0) THEN

			CALL CheckMotorFilamentProximity(X, Y, Z, XM(IM), YM(IM), ZM(IM), ContactState(:,IM), TempContact(:,IM))

			CALL MotorBinding(ContactState(:,IM), TempContact(:,IM), MotorStateUpdate(IM))

			IF (MotorType(IM) == 1) THEN
				CALL MotorStep(ContactState(:,IM), TempContact(:,IM))
			ELSE IF (MotorType(IM) == 2) THEN
				CALL MotorStuck(ContactState(:,IM), TempContact(:,IM))
			END IF
		END IF
	END DO	
    
    
	!---State Conversion of Motors--------------------------------------------
	
	DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
		IF ((MotorType(IM) == 1) .AND. (MotorStateUpdate(IM) == .FALSE.)) THEN
			CALL MotorStateConv(X, Y, Z, F_Motor_X(IM), F_Motor_Y(IM), F_Motor_Z(IM), ContactState(:,IM), Release_ADP(IM))
		END IF
	END DO
	
	
    !---Renew Motor Population--------------------------------------------
	
	IF (MOD(TS,AreaRenewDiv)==0) THEN
	
		CALL RenewMotorPopulation(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, EraseCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	END IF

	
	!!--Update of Filament States-----------------------------------------------------
	
	!---Generating RND Num Matrix-----------------------------------------
	
	DO I=1,NumFilament
		CALL NormRNDVector(NumBeads, NormRandVector4Beads)
	
		DO J=1,NumBeads
			XNormRandVector4Beads(J,I) = NormRandVector4Beads(J)
		END DO
	END DO
	
	DO I=1,NumFilament
		CALL NormRNDVector(NumBeads, NormRandVector4Beads)
	
		DO J=1,NumBeads
			YNormRandVector4Beads(J,I) = NormRandVector4Beads(J)
		END DO
	END DO
	
	DO I=1,NumFilament
		CALL NormRNDVector(NumBeads, NormRandVector4Beads)
	
		DO J=1,NumBeads
			ZNormRandVector4Beads(J,I) = NormRandVector4Beads(J)
		END DO
	END DO
	
	
	Loop_Filament: DO I=1, NumFilament
	

		DO J=1, NumBeads
			XI(J)=X(J,I)
		END DO
		DO J=1, NumBeads
			YI(J)=Y(J,I)
		END DO
		DO J=1, NumBeads
			ZI(J)=Z(J,I)
		END DO
	
		DO J=1, NumBeads
			FIx(J)=Fx(J,I)
		END DO
		DO J=1, NumBeads
			FIy(J)=Fy(J,I)
		END DO
		DO J=1, NumBeads
			FIz(J)=Fz(J,I)
		END DO
	
		DO J=1, NumBeads
			XINormRandVector4Beads(J)=XNormRandVector4Beads(J,I)
		END DO
		DO J=1, NumBeads
			YINormRandVector4Beads(J)=YNormRandVector4Beads(J,I)
		END DO
		DO J=1, NumBeads
			ZINormRandVector4Beads(J)=ZNormRandVector4Beads(J,I)
		END DO
	
	
	!---Unconstrained Movements of Beads--------------------------------------------------------
	
		XI_temp = XI + FIx/gamma_Bead*dt + XINormRandVector4Beads * DSQRT(2.0_DP * D_Bead * dt)
		YI_temp = YI + FIy/gamma_Bead*dt + YINormRandVector4Beads * DSQRT(2.0_DP * D_Bead * dt)
		ZI_temp = ZI + FIz/gamma_Bead*dt + ZINormRandVector4Beads * DSQRT(2.0_DP * D_Bead * dt)
	
	
	!---Iteration until Constraint and Confinement are Statisfied
	
		NumIteration = 0
		StateConstraint = .FALSE.
		StatConfinement = .FALSE.
	
		IterationConstraintConfinement: DO
	
	!		IF ((StateConstraint) .OR. (NumIteration > MaxNumIteration)) EXIT IterationConstraintConfinement
	
			IF (StateConstraint .AND. StatConfinement) EXIT IterationConstraintConfinement
	
			IF (NumIteration > MaxNumIteration) THEN
				WRITE(*,*) "Too many iterations!"
				EXIT IterationConstraintConfinement
			END IF
	
			NumIteration = NumIteration + 1
	
	
	!---Confinement (Filament)--------------------------------------------
	
			StatConfinement = .TRUE.
	
	
			Loop_Bead_Confinement: DO J=1, NumBeads
	
				CALL Confinement(XI_temp(J), YI_temp(J), ZI_temp(J), XI(J), YI(J), ZI(J), StatConfinement)
	
			END DO Loop_Bead_Confinement
	
		
	!---Constraint--------------------------------------------------------
	
			StateConstraint = .TRUE.
	
			Loop_Bond_Constraint: DO J=1, NumBeads-1
	
				CALL Constraint(XI_temp(J), YI_temp(J), ZI_temp(J), XI_temp(J+1), YI_temp(J+1), ZI_temp(J+1), &
						XI(J), YI(J), ZI(J), XI(J+1), YI(J+1), ZI(J+1), StateConstraint)
	
			END DO Loop_Bond_Constraint
	
		
	!---------------------------------------------------------------------
	
		END DO IterationConstraintConfinement
	
	!---Update of Position Variables--------------------------------------
	
		DO J=1,NumBeads
			X(J,I) = XI_temp(J)
		END DO
		DO J=1,NumBeads
			Y(J,I) = YI_temp(J)
		END DO
		DO J=1,NumBeads
			Z(J,I) = ZI_temp(J)
		END DO
	
	
	END DO Loop_Filament


	!---Calculating Forces upon Motors and dividing the Force to Beads---------------
	
	CALL CalculateForceMotor(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, ContactState, F_Motor_X, F_Motor_Y, F_Motor_Z, Elongation)
	CALL CalculateForceBead(ActiveMotorIdxOffset, ActiveMotorIdxEnd, ContactState, Force_Bead_X, Force_Bead_Y, Force_Bead_Z, F_Motor_X, F_Motor_Y, F_Motor_Z)
	
	
	!---Calculating Total Forces upon Beads-------------------------------------
	
	Fx=Force_Bending(X) + Force_Bead_X + ExtF_X(TS, X, Y, Z)
	Fy=Force_Bending(Y) + Force_Bead_Y + ExtF_Y(TS, X, Y, Z)
	Fz=Force_Bending(Z) + Force_Bead_Z + ExtF_Z(TS, X, Y, Z)
	
	IF (MOD(TS,OutPutDiv2)==0) THEN
		CALL OutputMotorStates(UnitNumMotorStates, TS, ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, F_Motor_X, F_Motor_Y, F_Motor_Z, ContactState, MotorType)
	END IF
	
	IF (MOD(TS,OutPutDiv)==0) THEN
	!IF ((TS >= 5E6) .AND. (TS <= 6E6) .AND. (MOD(TS,OutPutDiv)==0)) THEN
	
		OutputfileCounter = OutputfileCounter + 1
	
	
	!---Output Area & Erase Counters--------------------------------------
	
		WRITE(UnitNumAreaEraseCounter,*) TS, AreaCounter, EraseCounter

	
		!---Various Outputs Filament Conformation-------------------------------
		
		CALL OutputConformation(UnitNumConformation,TS,X,Y,Z)
		CALL OutputTipXY(UnitNumTipXY,TS,X,Y)
!		CALL OutputMotorStates(UnitNumMotorStates, TS, ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, F_Motor_X, F_Motor_Y, F_Motor_Z, ContactState, MotorType)
		CALL OutputFilamentVTK(I_Assay, OutputfileCounter, X, Y, Z)
		CALL OutputFilamentPlusEndVTK(I_Assay, OutputfileCounter, X, Y, Z)		
		CALL OutputContactState(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState)
		CALL OutputIntMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState, XM, YM, ZM)		
		CALL OutputMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, XM, YM, ZM)	
	

	!---------------------------------------------------------------------
	
	
	END IF
	
	
	IF (X(1,1) > XLimit) EXIT Loop_Time
	
	
	END DO Loop_Time
	
	
	CLOSE(UnitNumConformation)
	CLOSE(UnitNumTipXY)
	CLOSE(UnitNumMotorStates)
	CLOSE(UnitNumAreaEraseCounter)	
	
	
	END DO Loop_Assay
	

	CLOSE(10)
	
	
	
	END PROGRAM MAIN
	
