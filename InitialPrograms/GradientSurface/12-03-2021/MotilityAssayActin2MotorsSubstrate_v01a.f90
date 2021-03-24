

MODULE PLANAR_SURFACE

USE PARAMETERS
USE mtmod

IMPLICIT NONE

CONTAINS



SUBROUTINE OutputBoundary

	USE PARAMETERS, ONLY : DP, HorizontalLength, VerticalLength

	INTEGER :: Openstatus333



	OPEN (UNIT = 333, FILE = "ChamberBoundary.vtk", STATUS = "NEW", &
		ACTION = "WRITE", POSITION = "REWIND", IOSTAT = Openstatus333)
	IF (Openstatus333 > 0) STOP "*** Can't open file ***"


	WRITE(333,'(A)') "# vtk DataFile Version 2.0"
	WRITE(333,'(A)') "Chamber Boundary"
	WRITE(333,'(A)') "ASCII"
	WRITE(333,'(A)') "DATASET UNSTRUCTURED_GRID"
	WRITE(333,'(A, I10, A)') "POINTS", 4, " float"


	WRITE(333,'(3F10.5)') (0.5_DP)*HorizontalLength, (-0.5_DP)*VerticalLength, 0.0_DP
	WRITE(333,'(3F10.5)') (0.5_DP)*HorizontalLength, (0.5_DP)*VerticalLength, 0.0_DP
	WRITE(333,'(3F10.5)') (-0.5_DP)*HorizontalLength, (0.5_DP)*VerticalLength, 0.0_DP
	WRITE(333,'(3F10.5)') (-0.5_DP)*HorizontalLength, (-0.5_DP)*VerticalLength, 0.0_DP


	WRITE(333,'(A, I10, I10)') "CELLS", 1, 5


	WRITE(333,'(4I5)') 4, 0, 1, 2, 3


	WRITE(333,'(A, I10)') "CELL_TYPES ", 1


	WRITE(333,'(I5)') 7


	CLOSE(333)



END SUBROUTINE OutputBoundary





!---Initial Motor Location----------------------------------------------------------------

SUBROUTINE InitialMotorLocations(ActiveMotorIdxOffset, ActiveMotorIdxEnd, IniAngle, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
	USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
	USE mtmod


	INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)

	REAL(KIND = DP), INTENT(IN) ::  IniAngle
	
	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y

	REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM

	REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState

	INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum

	INTEGER, INTENT(INOUT)	:: AreaCounter

	REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy

	INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd



	INTEGER(KIND = Range15):: IM, AddedMotorCounter

	INTEGER :: JJ, JJJ

	REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3

	LOGICAL :: NearBoundary, InNewArea, OutOldArea






	ActiveMotorIdxOffset = 0



	XCM=SUM(X(:,1))/DBLE(NumBeads)
	YCM=SUM(Y(:,1))/DBLE(NumBeads)
	
	AreaOriginUx(AreaCounter) = DCOS(IniAngle)
	AreaOriginUy(AreaCounter) = DSIN(IniAngle)
	
	AreaOriginX(AreaCounter) = XCM
	AreaOriginY(AreaCounter) = YCM
	
	
	
	DO IM=1, NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)
	
		UR1 = grnd()
		UR2 = grnd()
	
		XM(IM) = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
		YM(IM) = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)
		ZM(IM) = 0.0_DP
	
	
		UR1 = grnd()
		IF (UR1 <= Type1Ratio) THEN
			MotorType(IM) = 1
			UR2 = grnd()
			IF(UR2 <= 0.091)THEN
				ContactState(:,IM) = -1.0_DP
			ELSE
				ContactState(:,IM) = 0.0_DP
			END IF
		ELSE
			MotorType(IM) = 2
			ContactState(:,IM) = 0.0_DP
		END IF
	
	END DO
	
	ActiveMotorIdxEnd = ActiveMotorIdxEnd + NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)
	AddedMotorNum(AreaCounter) = NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)

END SUBROUTINE InitialMotorLocations





	!---Subroutine RenewMotorPopulation-----------------------------------
	
SUBROUTINE RenewMotorPopulation(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, EraseCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
	USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
	USE mtmod


	INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y

	REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM

	REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState

	INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum

	INTEGER, INTENT(INOUT)	:: AreaCounter, EraseCounter

	REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy

	INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd



	INTEGER(KIND = Range15):: IM, AddedMotorCounter

	INTEGER :: I_Area, JJ, JJJ

	REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3

	LOGICAL :: NearBoundary, InNewArea, OutOldArea



!---Erase Old Motor Region--------------------------------------------

	OutOldArea = .TRUE.

	DO JJJ=1, NumBeads
		IF ((DABS((X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUx(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUy(EraseCounter+1)) <= 0.5_DP*HorizontalLength + 0.5_DP) .AND. &
		(DABS(-(X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUy(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUx(EraseCounter+1)) <= 0.5_DP*VerticalLength + 0.5_DP)) THEN

			OutOldArea = .FALSE.

		END IF
	END DO


	IF (OutOldArea) THEN

		EraseCounter = EraseCounter + 1

		ActiveMotorIdxOffset = ActiveMotorIdxOffset + AddedMotorNum(EraseCounter)	

	END IF


!---Checking if beads are near boundary-------------------------------

XCM=SUM(X(:,1))/DBLE(NumBeads)
YCM=SUM(Y(:,1))/DBLE(NumBeads)

!IF ((DABS((XCM-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) .OR. &			!v7
!	(DABS(-(XCM-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP)) THEN	!v7


NearBoundary = .FALSE.

DO JJ=1, NumBeads
	IF (DABS((X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.

	IF (DABS(-(X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.
END DO


IF (NearBoundary == .TRUE.) THEN

!---Generate New Motor Region-----------------------------------------

	AreaCounter = AreaCounter + 1


	AreaOriginX(AreaCounter) = XCM
	AreaOriginY(AreaCounter) = YCM
	AreaOriginUx(AreaCounter) = (X(1,1) - X(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))
	AreaOriginUy(AreaCounter) = (Y(1,1) - Y(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))


	AddedMotorCounter = 0
	DO IM=1, NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)

		UR1 = grnd()
		UR2 = grnd()

		XM_New = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
		YM_New = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)

		InNewArea = .TRUE.
		IF (AreaCounter == 1) THEN

			IF ((DABS((XM_New-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) <= 0.5_DP*HorizontalLength) .AND. &
			(DABS(-(XM_New-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) <= 0.5_DP*VerticalLength)) THEN

				InNewArea = .FALSE.

			END IF

		ELSE
			DO I_Area = EraseCounter+1, AreaCounter-1

				IF ((DABS((XM_New-AreaOriginX(I_Area))*AreaOriginUx(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUy(I_Area)) <= 0.5_DP*HorizontalLength) .AND. &
				(DABS(-(XM_New-AreaOriginX(I_Area))*AreaOriginUy(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUx(I_Area)) <= 0.5_DP*VerticalLength)) THEN

					InNewArea = .FALSE.

				END IF

			END DO
		END IF

		IF (InNewArea == .TRUE.) THEN

			AddedMotorCounter = AddedMotorCounter + 1

			XM(ActiveMotorIdxEnd + AddedMotorCounter) = XM_New
			YM(ActiveMotorIdxEnd + AddedMotorCounter) = YM_New
			ZM(ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP

			UR1 = grnd()
			IF (UR1 <= Type1Ratio) THEN

				MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 1
				UR2 = grnd()
				IF(UR2 <= 0.091) THEN
					ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = -1.0_DP
				ELSE
					ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
				END IF
			ELSE
				MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 2
				ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
			END IF

		END IF



	END DO

	AddedMotorNum(AreaCounter) = AddedMotorCounter
	ActiveMotorIdxEnd = ActiveMotorIdxEnd + AddedMotorCounter

END IF

END SUBROUTINE RenewMotorPopulation





SUBROUTINE Confinement(TempXCoordinate, TempYCoordinate, TempZCoordinate, &
		XCoordinate, YCoordinate, ZCoordinate, ConfinementStatus)


	USE PARAMETERS, ONLY : DP, HorizontalLength, VerticalLength


	REAL(KIND = DP), INTENT(INOUT) :: TempXCoordinate, TempYCoordinate, TempZCoordinate

	REAL(KIND = DP), INTENT(IN) :: XCoordinate, YCoordinate, ZCoordinate

!	REAL(KIND = DP) :: DXCoordinate, DYCoordinate, DZCoordinate

	LOGICAL, INTENT(INOUT) :: ConfinementStatus



!	DXCoordinate = 0.0_DP
!	DYCoordinate = 0.0_DP
!	DZCoordinate = 0.0_DP





!---ConfinemenT-------------------------------------------------------

	IF (TempZCoordinate < 0.0_DP) THEN
		ConfinementStatus = .FALSE.
		TempZCoordinate = 0.0_DP
	END IF





END SUBROUTINE Confinement


END MODULE PLANAR_SURFACE


!---------------------------------------------------------------------------------------------------


MODULE CHANNEL_TRACK

	USE PARAMETERS
	USE mtmod
	
	IMPLICIT NONE
	
	CONTAINS
	
	
	
!	SUBROUTINE OutputBoundary
	
	
!	*****
	
	
!	END SUBROUTINE OutputBoundary
	
	



!---Initial Motor Location----------------------------------------------------------------

	SUBROUTINE InitialMotorLocations(ActiveMotorIdxOffset, ActiveMotorIdxEnd, IniAngle, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
		USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
		USE mtmod
	
	
		INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)
	
		REAL(KIND = DP), INTENT(IN) ::  IniAngle
		
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM
	
		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState
	
		INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum
	
		INTEGER, INTENT(INOUT)	:: AreaCounter
	
		REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy
	
		INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd
	
	
	
		INTEGER(KIND = Range15):: IM, AddedMotorCounter
	
		INTEGER :: JJ, JJJ
	
		REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3
	
		LOGICAL :: NearBoundary, InNewArea, OutOldArea






		ActiveMotorIdxOffset = 0



		XCM=SUM(X(:,1))/DBLE(NumBeads)
		YCM=SUM(Y(:,1))/DBLE(NumBeads)
		
		AreaOriginUx(AreaCounter) = DCOS(IniAngle)
		AreaOriginUy(AreaCounter) = DSIN(IniAngle)
		
		AreaOriginX(AreaCounter) = XCM
		AreaOriginY(AreaCounter) = YCM
		
		
		
		DO IM=1, NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)
		
			UR1 = grnd()
			UR2 = grnd()
		
			XM(IM) = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
			YM(IM) = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)
			ZM(IM) = 0.0_DP
		
		
			UR1 = grnd()
			IF (UR1 <= Type1Ratio) THEN
				MotorType(IM) = 1
				UR2 = grnd()
				IF(UR2 <= 0.091)THEN
					ContactState(:,IM) = -1.0_DP
				ELSE
					ContactState(:,IM) = 0.0_DP
				END IF
			ELSE
				MotorType(IM) = 2
				ContactState(:,IM) = 0.0_DP
			END IF
		
		END DO
		
		ActiveMotorIdxEnd = ActiveMotorIdxEnd + NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)
		AddedMotorNum(AreaCounter) = NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)

	END SUBROUTINE InitialMotorLocations





		!---Subroutine RenewMotorPopulation-----------------------------------
	
	SUBROUTINE RenewMotorPopulation(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, EraseCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
		USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
		USE mtmod
	
	
		INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM
	
		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState
	
		INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum
	
		INTEGER, INTENT(INOUT)	:: AreaCounter, EraseCounter
	
		REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy
	
		INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd
	
	
	
		INTEGER(KIND = Range15):: IM, AddedMotorCounter
	
		INTEGER :: I_Area, JJ, JJJ
	
		REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3
	
		LOGICAL :: NearBoundary, InNewArea, OutOldArea
	
	
	
	!---Erase Old Motor Region--------------------------------------------
	
		OutOldArea = .TRUE.
	
		DO JJJ=1, NumBeads
			IF ((DABS((X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUx(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUy(EraseCounter+1)) <= 0.5_DP*HorizontalLength + 0.5_DP) .AND. &
			(DABS(-(X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUy(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUx(EraseCounter+1)) <= 0.5_DP*VerticalLength + 0.5_DP)) THEN
	
				OutOldArea = .FALSE.
	
			END IF
		END DO
	
	
		IF (OutOldArea) THEN
	
			EraseCounter = EraseCounter + 1

			ActiveMotorIdxOffset = ActiveMotorIdxOffset + AddedMotorNum(EraseCounter)	
	
		END IF
	
	
	!---Checking if beads are near boundary-------------------------------
	
	XCM=SUM(X(:,1))/DBLE(NumBeads)
	YCM=SUM(Y(:,1))/DBLE(NumBeads)
	
	!IF ((DABS((XCM-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) .OR. &			!v7
	!	(DABS(-(XCM-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP)) THEN	!v7
	
	
	NearBoundary = .FALSE.
	
	DO JJ=1, NumBeads
		IF (DABS((X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.
	
		IF (DABS(-(X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.
	END DO
	
	
	IF (NearBoundary == .TRUE.) THEN
	
	!---Generate New Motor Region-----------------------------------------
	
		AreaCounter = AreaCounter + 1
	
	
		AreaOriginX(AreaCounter) = XCM
		AreaOriginY(AreaCounter) = YCM
		AreaOriginUx(AreaCounter) = (X(1,1) - X(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))
		AreaOriginUy(AreaCounter) = (Y(1,1) - Y(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))
	
	
		AddedMotorCounter = 0
		DO IM=1, NINT(Motor_Density*HorizontalLength*VerticalLength, Range15)
	
			UR1 = grnd()
			UR2 = grnd()
	
			XM_New = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
			YM_New = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)
	
			InNewArea = .TRUE.
			IF (AreaCounter == 1) THEN
	
				IF ((DABS((XM_New-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) <= 0.5_DP*HorizontalLength) .AND. &
				(DABS(-(XM_New-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) <= 0.5_DP*VerticalLength)) THEN
	
					InNewArea = .FALSE.
	
				END IF
	
			ELSE
				DO I_Area = EraseCounter+1, AreaCounter-1
	
					IF ((DABS((XM_New-AreaOriginX(I_Area))*AreaOriginUx(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUy(I_Area)) <= 0.5_DP*HorizontalLength) .AND. &
					(DABS(-(XM_New-AreaOriginX(I_Area))*AreaOriginUy(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUx(I_Area)) <= 0.5_DP*VerticalLength)) THEN
	
						InNewArea = .FALSE.
	
					END IF
	
				END DO
			END IF
	
			IF (InNewArea == .TRUE.) THEN
	
				AddedMotorCounter = AddedMotorCounter + 1
	
				XM(ActiveMotorIdxEnd + AddedMotorCounter) = XM_New
				YM(ActiveMotorIdxEnd + AddedMotorCounter) = YM_New
				ZM(ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP

				UR1 = grnd()
				IF (UR1 <= Type1Ratio) THEN
	
					MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 1
					UR2 = grnd()
					IF(UR2 <= 0.091) THEN
						ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = -1.0_DP
					ELSE
						ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
					END IF
				ELSE
					MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 2
					ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
				END IF
	
			END IF
	
	
	
		END DO
	
		AddedMotorNum(AreaCounter) = AddedMotorCounter
		ActiveMotorIdxEnd = ActiveMotorIdxEnd + AddedMotorCounter
	
	END IF
	
	END SUBROUTINE RenewMotorPopulation


	
	
	
	SUBROUTINE Confinement(TempXCoordinate, TempYCoordinate, TempZCoordinate, &
			XCoordinate, YCoordinate, ZCoordinate, ConfinementStatus)
	
	
		USE PARAMETERS, ONLY : DP, HorizontalLength, VerticalLength
	
	
		REAL(KIND = DP), INTENT(INOUT) :: TempXCoordinate, TempYCoordinate, TempZCoordinate
	
		REAL(KIND = DP), INTENT(IN) :: XCoordinate, YCoordinate, ZCoordinate
	
	!	REAL(KIND = DP) :: DXCoordinate, DYCoordinate, DZCoordinate
	
		LOGICAL, INTENT(INOUT) :: ConfinementStatus
	
	
	
	!	DXCoordinate = 0.0_DP
	!	DYCoordinate = 0.0_DP
	!	DZCoordinate = 0.0_DP
	
	
	
	
	
	!---ConfinemenT-------------------------------------------------------
	
		IF (TempYCoordinate > 0.5_DP*ChannelWidth) THEN
			ConfinementStatus = .FALSE.
			TempYCoordinate = 0.5_DP*ChannelWidth
		END IF

		IF (TempYCoordinate < -0.5_DP*ChannelWidth) THEN
			ConfinementStatus = .FALSE.
			TempYCoordinate = -0.5_DP*ChannelWidth
		END IF

		IF (TempZCoordinate < 0.0_DP) THEN
			ConfinementStatus = .FALSE.
			TempZCoordinate = 0.0_DP
		END IF
	
	
	
	
	
	END SUBROUTINE Confinement
	
	
	END MODULE CHANNEL_TRACK
	
	
	!---------------------------------------------------------------------------------------------------


	MODULE PLANAR_SURFACE_yGRADIENT

		USE PARAMETERS
		USE mtmod
		
		IMPLICIT NONE
		
		CONTAINS
		
		
		
	!	SUBROUTINE OutputBoundary
		
		
	!	*****
		
		
	!	END SUBROUTINE OutputBoundary
		
		
	
	
	
	!---Initial Motor Location----------------------------------------------------------------
	
		SUBROUTINE InitialMotorLocations(ActiveMotorIdxOffset, ActiveMotorIdxEnd, IniAngle, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
		
		
			USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
			USE mtmod
		
		
			INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)
		
			REAL(KIND = DP), INTENT(IN) ::  IniAngle
			
			REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y
		
			REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM
		
			REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState
		
			INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum
		
			INTEGER, INTENT(INOUT)	:: AreaCounter
		
			REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy
		
			INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd
		
		
		
			INTEGER(KIND = Range15):: IM, AddedMotorCounter
		
			INTEGER :: JJ, JJJ
		
			REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3
		
			LOGICAL :: NearBoundary, InNewArea, OutOldArea
	
	
	
	
	
	
			ActiveMotorIdxOffset = 0
	
	
	
			XCM=SUM(X(:,1))/DBLE(NumBeads)
			YCM=SUM(Y(:,1))/DBLE(NumBeads)
			
			AreaOriginUx(AreaCounter) = DCOS(IniAngle)
			AreaOriginUy(AreaCounter) = DSIN(IniAngle)
			
			AreaOriginX(AreaCounter) = XCM
			AreaOriginY(AreaCounter) = YCM
			
			
			AddedMotorCounter = 0
			DO IM=1, NINT(Motor_Density_Upper*HorizontalLength*VerticalLength, Range15)
			
				UR1 = grnd()
				UR2 = grnd()
			
				XM_New = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
				YM_New = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)

				UR1 = grnd()
				IF (UR1 <= Prob_yLinearGrad(YM_New)) THEN
					AddedMotorCounter = AddedMotorCounter + 1
					XM(AddedMotorCounter) = XM_New
					YM(AddedMotorCounter) = YM_New
					ZM(AddedMotorCounter) = 0.0_DP
				
				
					UR1 = grnd()
					IF (UR1 <= Type1Ratio) THEN
						MotorType(AddedMotorCounter) = 1
						UR2 = grnd()
						IF(UR2 <= 0.091)THEN
							ContactState(:,AddedMotorCounter) = -1.0_DP
						ELSE
							ContactState(:,AddedMotorCounter) = 0.0_DP
						END IF
					ELSE
						MotorType(AddedMotorCounter) = 2
						ContactState(:,AddedMotorCounter) = 0.0_DP
					END IF

				END IF
			END DO
			
			ActiveMotorIdxEnd = ActiveMotorIdxEnd + AddedMotorCounter
			AddedMotorNum(AreaCounter) = AddedMotorCounter
	
		END SUBROUTINE InitialMotorLocations
	
	
	
	
	
			!---Subroutine RenewMotorPopulation-----------------------------------
		
		SUBROUTINE RenewMotorPopulation(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, EraseCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
		
		
			USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
			USE mtmod
		
		
			INTEGER, DIMENSION(MaxNumMotors), INTENT(INOUT) :: MotorType		! 2Motors	1=Myosin, 2=Dead Motor (or "Zombie" in Dan's email)
		
			REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y
		
			REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(INOUT) :: XM, YM, ZM
		
			REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState
		
			INTEGER(KIND = Range15), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AddedMotorNum
		
			INTEGER, INTENT(INOUT)	:: AreaCounter, EraseCounter
		
			REAL(KIND = DP), DIMENSION(MaxAreaNum), INTENT(INOUT) :: AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy
		
			INTEGER(KIND = Range15), INTENT(INOUT) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd
		
		
		
			INTEGER(KIND = Range15):: IM, AddedMotorCounter
		
			INTEGER :: I_Area, JJ, JJJ
		
			REAL(KIND = DP) :: XCM, YCM, XM_New, YM_New, UR1, UR2, UR3
		
			LOGICAL :: NearBoundary, InNewArea, OutOldArea
		
		
		
		!---Erase Old Motor Region--------------------------------------------
		
			OutOldArea = .TRUE.
		
			DO JJJ=1, NumBeads
				IF ((DABS((X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUx(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUy(EraseCounter+1)) <= 0.5_DP*HorizontalLength + 0.5_DP) .AND. &
				(DABS(-(X(JJJ,1)-AreaOriginX(EraseCounter+1))*AreaOriginUy(EraseCounter+1) + (Y(JJJ,1)-AreaOriginY(EraseCounter+1))*AreaOriginUx(EraseCounter+1)) <= 0.5_DP*VerticalLength + 0.5_DP)) THEN
		
					OutOldArea = .FALSE.
		
				END IF
			END DO
		
		
			IF (OutOldArea) THEN
		
				EraseCounter = EraseCounter + 1
	
				ActiveMotorIdxOffset = ActiveMotorIdxOffset + AddedMotorNum(EraseCounter)	
		
			END IF
		
		
		!---Checking if beads are near boundary-------------------------------
		
		XCM=SUM(X(:,1))/DBLE(NumBeads)
		YCM=SUM(Y(:,1))/DBLE(NumBeads)
		
		!IF ((DABS((XCM-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) .OR. &			!v7
		!	(DABS(-(XCM-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YCM-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP)) THEN	!v7
		
		
		NearBoundary = .FALSE.
		
		DO JJ=1, NumBeads
			IF (DABS((X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) >= 0.5_DP*HorizontalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.
		
			IF (DABS(-(X(JJ,1)-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (Y(JJ,1)-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) >= 0.5_DP*VerticalLength - 0.5_DP*DBLE(NumBeads-1)*BondLength - 1.0_DP) NearBoundary = .TRUE.
		END DO
		
		
		IF (NearBoundary == .TRUE.) THEN
		
		!---Generate New Motor Region-----------------------------------------
		
			AreaCounter = AreaCounter + 1
		
		
			AreaOriginX(AreaCounter) = XCM
			AreaOriginY(AreaCounter) = YCM
			AreaOriginUx(AreaCounter) = (X(1,1) - X(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))
			AreaOriginUy(AreaCounter) = (Y(1,1) - Y(2,1))/DSQRT((X(1,1) - X(2,1))*(X(1,1) - X(2,1)) + (Y(1,1) - Y(2,1))*(Y(1,1) - Y(2,1)))
		
		
			AddedMotorCounter = 0
			DO IM=1, NINT(Motor_Density_Upper*HorizontalLength*VerticalLength, Range15)
		
				UR1 = grnd()
				UR2 = grnd()
		
				XM_New = XCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUx(AreaCounter) - VerticalLength * (UR2 - 0.5_DP) * AreaOriginUy(AreaCounter)
				YM_New = YCM + HorizontalLength * (UR1 - 0.5_DP) * AreaOriginUy(AreaCounter) + VerticalLength * (UR2 - 0.5_DP) * AreaOriginUx(AreaCounter)

				IF (DABS(YM_New) > 0.5_DP*ChannelWidth) CYCLE
		
				InNewArea = .TRUE.
				IF (AreaCounter == 1) THEN
		
					IF ((DABS((XM_New-AreaOriginX(AreaCounter))*AreaOriginUx(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUy(AreaCounter)) <= 0.5_DP*HorizontalLength) .AND. &
					(DABS(-(XM_New-AreaOriginX(AreaCounter))*AreaOriginUy(AreaCounter) + (YM_New-AreaOriginY(AreaCounter))*AreaOriginUx(AreaCounter)) <= 0.5_DP*VerticalLength)) THEN
		
						InNewArea = .FALSE.
		
					END IF
		
				ELSE
					DO I_Area = EraseCounter+1, AreaCounter-1
		
						IF ((DABS((XM_New-AreaOriginX(I_Area))*AreaOriginUx(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUy(I_Area)) <= 0.5_DP*HorizontalLength) .AND. &
						(DABS(-(XM_New-AreaOriginX(I_Area))*AreaOriginUy(I_Area) + (YM_New-AreaOriginY(I_Area))*AreaOriginUx(I_Area)) <= 0.5_DP*VerticalLength)) THEN
		
							InNewArea = .FALSE.
		
						END IF
		
					END DO
				END IF
		
				UR1 = grnd()
				IF ((InNewArea == .TRUE.) .AND. (UR1 <= Prob_yLinearGrad(YM_New))) THEN
		
					AddedMotorCounter = AddedMotorCounter + 1
		
					XM(ActiveMotorIdxEnd + AddedMotorCounter) = XM_New
					YM(ActiveMotorIdxEnd + AddedMotorCounter) = YM_New
					ZM(ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
	
					UR1 = grnd()
					IF (UR1 <= Type1Ratio) THEN
		
						MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 1
						UR2 = grnd()
						IF(UR2 <= 0.091) THEN
							ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = -1.0_DP
						ELSE
							ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
						END IF
					ELSE
						MotorType(ActiveMotorIdxEnd + AddedMotorCounter) = 2
						ContactState(:,ActiveMotorIdxEnd + AddedMotorCounter) = 0.0_DP
					END IF
		
				END IF
		
		
		
			END DO
		
			AddedMotorNum(AreaCounter) = AddedMotorCounter
			ActiveMotorIdxEnd = ActiveMotorIdxEnd + AddedMotorCounter
		
		END IF
		
		END SUBROUTINE RenewMotorPopulation
	
	
		
		
		
		SUBROUTINE Confinement(TempXCoordinate, TempYCoordinate, TempZCoordinate, &
				XCoordinate, YCoordinate, ZCoordinate, ConfinementStatus)
		
		
			USE PARAMETERS, ONLY : DP, HorizontalLength, VerticalLength
		
		
			REAL(KIND = DP), INTENT(INOUT) :: TempXCoordinate, TempYCoordinate, TempZCoordinate
		
			REAL(KIND = DP), INTENT(IN) :: XCoordinate, YCoordinate, ZCoordinate
		
		!	REAL(KIND = DP) :: DXCoordinate, DYCoordinate, DZCoordinate
		
			LOGICAL, INTENT(INOUT) :: ConfinementStatus
		
		
		
		!	DXCoordinate = 0.0_DP
		!	DYCoordinate = 0.0_DP
		!	DZCoordinate = 0.0_DP
		
		
		
		
		
		!---ConfinemenT-------------------------------------------------------
	
			IF (TempZCoordinate < 0.0_DP) THEN
				ConfinementStatus = .FALSE.
				TempZCoordinate = 0.0_DP
			END IF
		
		
		
		
		
		END SUBROUTINE Confinement
		



		FUNCTION Prob_yLinearGrad(Coordinate)
	
	
			USE PARAMETERS, ONLY : DP, Motor_Density_Upper, Motor_Density_Lower, ChannelWidth
		
		
			REAL(KIND = DP) :: Prob_yLinearGrad
		
			REAL(KIND = DP), INTENT(IN) :: Coordinate
		
			
		
		
			Prob_yLinearGrad = 0.5_DP*(1.0 + Motor_Density_Lower/Motor_Density_Upper) + (1.0 - Motor_Density_Lower/Motor_Density_Upper)*Coordinate/ChannelWidth
		


		END FUNCTION Prob_yLinearGrad



		
		END MODULE PLANAR_SURFACE_yGRADIENT
		
		
		!---------------------------------------------------------------------------------------------------