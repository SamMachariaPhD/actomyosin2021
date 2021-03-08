

MODULE PLANAR_TRACK_CONFINEMENT

USE PARAMETERS

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


END MODULE PLANAR_TRACK_CONFINEMENT


!---------------------------------------------------------------------------------------------------


