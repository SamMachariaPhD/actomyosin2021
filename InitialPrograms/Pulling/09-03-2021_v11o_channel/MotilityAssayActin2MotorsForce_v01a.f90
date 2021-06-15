MODULE UNIFORM_FORCE_X

USE PARAMETERS

IMPLICIT NONE

CONTAINS


!---External Force Calculation (X-coordinate)-------------------------

FUNCTION ExtF_X(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_X

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

	INTEGER :: I, J

!	REAL(KIND = DP) :: F


	ExtF_X = 0.0_DP

	IF (TS >= TimeForceON) THEN
		DO I=1, NumFilament
			ExtF_X(1,I) = 0.5_DP * ExtForceDensity0*BondLength
			DO J=2, NumBeads-1
				ExtF_X(J,I) = ExtForceDensity0 * BondLength
			END DO
			ExtF_X(NumBeads,I) = 0.5_DP * ExtForceDensity0 * BondLength
		END DO
	END IF

END FUNCTION ExtF_X


!---External Force Calculation (Y-coordinate)-------------------------

FUNCTION ExtF_Y(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_Y

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

	INTEGER :: I, J

!	REAL(KIND = DP) :: F


	ExtF_Y = 0.0_DP


END FUNCTION ExtF_Y


!---External Force Calculation (Z-coordinate)-------------------------

FUNCTION ExtF_Z(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_Z

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

	INTEGER :: I, J

!	REAL(KIND = DP) :: F


	ExtF_Z = 0.0_DP


END FUNCTION ExtF_Z



END MODULE UNIFORM_FORCE_X


!---------------------------------------------------------------------------------------------------


MODULE END_DRAG

USE PARAMETERS

IMPLICIT NONE

CONTAINS


!---External Force Calculation (X-coordinate)-------------------------

FUNCTION ExtF_X(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON, ExtForceMag


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_X

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

!	INTEGER :: I, J

!	REAL(KIND = DP) :: F
	REAL(KIND = DP) :: Mag

	ExtF_X = 0.0_DP

	Mag = sqrt((X(NumBeads,1)-X(NumBeads-1,1))**2+(Y(NumBeads,1)-Y(NumBeads-1,1))**2)
	ExtF_X(NumBeads,1) = (ExtForceMag/Mag)*(X(NumBeads,1)-X(NumBeads-1,1))
	

END FUNCTION ExtF_X


!---External Force Calculation (Y-coordinate)-------------------------

FUNCTION ExtF_Y(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON, ExtForceMag


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_Y

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

!	INTEGER :: I, J

!	REAL(KIND = DP) :: F
	REAL(KIND = DP) :: Mag


	ExtF_Y = 0.0_DP

	Mag = sqrt( (X(NumBeads,1)-X(NumBeads-1,1))**2+(Y(NumBeads,1)-Y(NumBeads-1,1))**2)
	ExtF_Y(NumBeads,1) = (ExtForceMag/Mag)*(Y(NumBeads,1)-Y(NumBeads-1,1))

END FUNCTION ExtF_Y


!---External Force Calculation (Z-coordinate)-------------------------

FUNCTION ExtF_Z(TS, X, Y, Z)


	USE PARAMETERS, ONLY : DP, Range15, NumFilament, NumBeads, BondLength, ExtForceDensity0, TimeForceON


	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: ExtF_Z

	REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

	INTEGER(KIND = Range15), INTENT(IN) :: TS

	INTEGER :: I, J

!	REAL(KIND = DP) :: F


	ExtF_Z = 0.0_DP


END FUNCTION ExtF_Z



END MODULE END_DRAG


!---------------------------------------------------------------------------------------------------



