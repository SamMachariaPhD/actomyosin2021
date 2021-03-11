MODULE OUTPUT

	USE PARAMETERS
	
	IMPLICIT NONE
	


	CONTAINS


	!---Output Filament Conformation in txt Format--------------------------------

	SUBROUTINE OutputConformation(UnitNumConformation,TS,X,Y,Z)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads
	
	
		INTEGER, INTENT(IN) :: UnitNumConformation
	
		INTEGER(KIND = Range15), INTENT(IN) :: TS

		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

		INTEGER :: I, J



		DO J=1, NumBeads
	
			WRITE(UnitNumConformation,'(I10)', ADVANCE = "NO") TS
		
			DO I=1, NumFilament-1
				WRITE(UnitNumConformation,'(3F25.15)', ADVANCE = "NO") X(J,I), Y(J,I), Z(J,I)
			END DO
			WRITE(UnitNumConformation,'(3F25.15)') X(J,NumFilament), Y(J,NumFilament), Z(J,NumFilament)
		END DO


	END SUBROUTINE OutputConformation



	!---Output Leading Tip (Minus End) X- and Y-Coordinates in txt Format--------------------------------

	SUBROUTINE OutputTipXY(UnitNumTipXY,TS,X,Y)


		USE PARAMETERS, ONLY : DP, NumFilament
	
	
		INTEGER, INTENT(IN) :: UnitNumTipXY
		
		INTEGER(KIND = Range15), INTENT(IN) :: TS

		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y
	
		INTEGER :: I



		DO I=1, NumFilament-1
			WRITE(UnitNumTipXY,'(I10, 2F14.6)', ADVANCE = "NO") TS, X(1,I), Y(1,I)
		END DO
		WRITE(UnitNumTipXY,'(I10, 2F14.6)') TS, X(1,NumFilament), Y(1,NumFilament)


	END SUBROUTINE OutputTipXY

	

	!---Output States of Motors in txt Format--------------------------------

	SUBROUTINE OutputMotorStates(UnitNumMotorStates, TS, ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, F_Motor_X, F_Motor_Y, F_Motor_Z, ContactState, MotorType)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads

	
		INTEGER, INTENT(IN) :: UnitNumMotorStates
		
		INTEGER(KIND = Range15), INTENT(IN) :: TS, ActiveMotorIdxOffset, ActiveMotorIdxEnd

		INTEGER, DIMENSION(MaxNumMotors), INTENT(IN) :: MotorType

		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z

		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(IN) :: XM, YM, ZM, F_Motor_X, F_Motor_Y, F_Motor_Z

		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(IN) :: ContactState
	
		INTEGER :: J_Contact

		INTEGER(KIND = Range15) :: IM

		REAL(KIND = DP) ::	Intercept_Contact, X_Contact, Y_Contact, Z_Contact



		DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
	
			IF (ContactState(1,IM) >= 1.0_DP) THEN
		
				J_Contact = INT(ContactState(1,IM))
				Intercept_Contact = ContactState(1,IM) - DBLE(J_Contact)
		
				IF (J_Contact >= NumBeads) THEN
		
					X_Contact = X(J_Contact,1) + Intercept_Contact * (X(J_Contact,1) - X(J_Contact-1,1))
					Y_Contact = Y(J_Contact,1) + Intercept_Contact * (Y(J_Contact,1) - Y(J_Contact-1,1))
					Z_Contact = Z(J_Contact,1) + Intercept_Contact * (Z(J_Contact,1) - Z(J_Contact-1,1))
		
				ELSE
		
					X_Contact = X(J_Contact,1) + Intercept_Contact * (X(J_Contact+1,1) - X(J_Contact,1))
					Y_Contact = Y(J_Contact,1) + Intercept_Contact * (Y(J_Contact+1,1) - Y(J_Contact,1))
					Z_Contact = Z(J_Contact,1) + Intercept_Contact * (Z(J_Contact+1,1) - Z(J_Contact,1))
		
				END IF
		
				WRITE(UnitNumMotorStates,'(2I10, I2, 10F14.6)') TS, IM, MotorType(IM), ContactState(1,IM), X_Contact, Y_Contact, Z_Contact, XM(IM), YM(IM), ZM(IM), F_Motor_X(IM), F_Motor_Y(IM), F_Motor_Z(IM)
		
			END IF
		
		END DO


	END SUBROUTINE OutputMotorStates



	!---Output Conformation of Filaments in vtk Format--------------------------------

	SUBROUTINE OutputFilamentVTK(I_Assay, OutputfileCounter, X, Y, Z)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads
	
	
		INTEGER, INTENT(IN) :: I_Assay, OutputfileCounter

		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z
	
		INTEGER :: I, J

		CHARACTER(LEN=30) :: OutFileName



		WRITE(OutFileName,'(A,I3.3,A,I7.7,A)') 'Filament_A', I_Assay, 'T', OutputfileCounter, '.vtk'
	
		OPEN(33,FILE=OutFileName)
	
		WRITE(33,'(A)') "# vtk DataFile Version 2.0"
		WRITE(33,'(A, I7)') "Filament: OutputfileCounter = ", OutputfileCounter
		WRITE(33,'(A)') "ASCII"
		WRITE(33,'(A)') "DATASET UNSTRUCTURED_GRID"
		WRITE(33,'(A, I10, A)') "POINTS", NumFilament*NumBeads, " float"
	
		DO I=1, NumFilament
			DO J=1, NumBeads
				WRITE(33,'(3F10.5)') X(J,I), Y(J,I), Z(J,I)
			END DO
		END DO
	
		WRITE(33,'(A, I10, I10)') "CELLS", NumFilament, (1+NumBeads)*NumFilament
		DO I=1, NumFilament
			!WRITE(33,'(I3, I10)') NumBeads, (J*I-1, J=1, NumBeads)
			WRITE(33,*) NumBeads, (J+(I-1)*NumBeads-1, J=1, NumBeads)
		END DO
	
		WRITE(33,'(A, I10)') "CELL_TYPES ", NumFilament
		DO I=1, NumFilament
			WRITE(33,'(I3)') 4
		END DO
	
	
		CLOSE(33)


	END SUBROUTINE OutputFilamentVTK



	!---Output Position of Filament Plus Ends in vtk Format--------------------------------

	SUBROUTINE OutputFilamentPlusEndVTK(I_Assay, OutputfileCounter, X, Y, Z)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads
	
	
		INTEGER, INTENT(IN) :: I_Assay, OutputfileCounter

		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z
	
		INTEGER :: I, J

		CHARACTER(LEN=50) :: OutFileName
		


		WRITE(OutFileName,'(A,I3.3,A,I7.7,A)') 'FilamentPlusEnd_A', I_Assay, 'T', OutputfileCounter, '.vtk'
	
		OPEN(33,FILE=OutFileName)
	
		WRITE(33,'(A)') "# vtk DataFile Version 2.0"
		WRITE(33,'(A, I7)') "Filament Plus Ends: OutputfileCounter = ", OutputfileCounter
		WRITE(33,'(A)') "ASCII"
		WRITE(33,'(A)') "DATASET UNSTRUCTURED_GRID"
		WRITE(33,'(A, I10, A)') "POINTS", NumFilament, " float"
	
		DO I=1, NumFilament
			WRITE(33,'(3F10.5)') X(NumBeads,I), Y(NumBeads,I), Z(NumBeads,I)
		END DO
	
		WRITE(33,'(A, I10, I10)') "CELLS", NumFilament, 2*NumFilament
	
		DO I=1, NumFilament
			WRITE(33,'(I3, I10)') 1, I-1
		END DO
	
		WRITE(33,'(A, I10)') "CELL_TYPES ", NumFilament
		DO I=1, NumFilament
			WRITE(33,'(I3)') 1
		END DO
	
	
		CLOSE(33)


	END SUBROUTINE OutputFilamentPlusEndVTK



	!---Output Contact States in txt Format--------------------------------

	SUBROUTINE OutputContactState(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads

		
	
		INTEGER, INTENT(IN) :: I_Assay, OutputfileCounter	
		
		INTEGER(KIND = Range15), INTENT(IN) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd

		INTEGER, DIMENSION(MaxNumMotors), INTENT(IN) :: MotorType

		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(IN) :: ContactState

		INTEGER(KIND = Range15) :: IM

		CHARACTER(LEN=30) :: OutFileName



		WRITE(OutFileName,'(A,I3.3,A,I7.7,A)') 'ContactStates_A', I_Assay, 'T', OutputfileCounter, '.txt'
	
		OPEN(33,FILE=OutFileName)
	
		DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
			WRITE(33,'(I7.7,I3.1,F10.5)', ADVANCE = "YES") IM, MotorType(IM), ContactState(1,IM)
		END DO
	
		CLOSE(33)


	END SUBROUTINE OutputContactState



	!---Output Motors Interacting with Filaments in vtk Format for Each Type---------------------------

	SUBROUTINE OutputIntMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, ContactState, XM, YM, ZM)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads, NumType


		INTEGER, INTENT(IN) :: I_Assay, OutputfileCounter

		INTEGER(KIND = Range15), INTENT(IN) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd

		INTEGER, DIMENSION(MaxNumMotors), INTENT(IN) :: MotorType

		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(IN) :: ContactState
		
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(IN) :: XM, YM, ZM

		INTEGER :: IType, CounterBuffer

		INTEGER(KIND = Range15) :: IM

		REAL(KIND = DP), DIMENSION(MaxNumMotors) :: XMBuffer, YMBuffer, ZMBuffer

		CHARACTER(LEN=30) :: OutFileName



		DO IType = 1, NumType
	
			WRITE(OutFileName,'(A,I1.1,A,I3.3,A,I7.7,A)') 'IntSpecie', IType, '_A', I_Assay, 'T', OutputfileCounter, '.vtk'
	
			OPEN(33,FILE=OutFileName)
	
			CounterBuffer = 0
			DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
	
				IF ((MotorType(IM)==IType) .AND. (SUM(ContactState(:,IM))>1)) THEN
					CounterBuffer = CounterBuffer + 1
					XMBuffer(CounterBuffer) = XM(IM)
					YMBuffer(CounterBuffer) = YM(IM)
					ZMBuffer(CounterBuffer) = ZM(IM)
				END IF
	
			END DO
	
			WRITE(33,'(A)') "# vtk DataFile Version 2.0"
			WRITE(33,'(A, I7)') "Motor: OutputfileCounter = ", OutputfileCounter
			WRITE(33,'(A)') "ASCII"
			WRITE(33,'(A)') "DATASET UNSTRUCTURED_GRID"
			WRITE(33,'(A, I10, A)') "POINTS", CounterBuffer, " float"
	
			DO IM=1, CounterBuffer
				WRITE(33,'(3F10.5)') XMBuffer(IM), YMBuffer(IM), ZMBuffer(IM)
			END DO
	
			WRITE(33,'(A, I10, I10)') "CELLS", CounterBuffer, 2*CounterBuffer
	
			DO IM=1, CounterBuffer
				WRITE(33,'(I3, I10)') 1, IM-1
			END DO
	
			WRITE(33,'(A, I10)') "CELL_TYPES ", CounterBuffer
			DO IM=1, CounterBuffer
				WRITE(33,'(I3)') 1
			END DO
	
			CLOSE(33)
	
		END DO


	END SUBROUTINE OutputIntMotorsVTK



	!---Output Motors in vtk Format for Each Type--------------------------------

	SUBROUTINE OutputMotorsVTK(I_Assay, OutputfileCounter, ActiveMotorIdxOffset, ActiveMotorIdxEnd, MotorType, XM, YM, ZM)


		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads, NumType


		INTEGER, INTENT(IN) :: I_Assay, OutputfileCounter

		INTEGER(KIND = Range15), INTENT(IN) :: ActiveMotorIdxOffset, ActiveMotorIdxEnd

		INTEGER, DIMENSION(MaxNumMotors), INTENT(IN) :: MotorType
		
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(IN) :: XM, YM, ZM

		INTEGER :: IType, CounterBuffer

		INTEGER(KIND = Range15) :: IM

		REAL(KIND = DP), DIMENSION(MaxNumMotors) :: XMBuffer, YMBuffer, ZMBuffer

		CHARACTER(LEN=30) :: OutFileName



		DO IType = 1, NumType
	
			WRITE(OutFileName,'(A,I1.1,A,I3.3,A,I7.7,A)') 'MotorSpecie', IType, '_A', I_Assay, 'T', OutputfileCounter, '.vtk'
	
			OPEN(33,FILE=OutFileName)
	
			CounterBuffer = 0
			DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
	
				IF (MotorType(IM)==IType) THEN
					CounterBuffer = CounterBuffer + 1
					XMBuffer(CounterBuffer) = XM(IM)
					YMBuffer(CounterBuffer) = YM(IM)
					ZMBuffer(CounterBuffer) = ZM(IM)
				END IF
	
			END DO
	
			WRITE(33,'(A)') "# vtk DataFile Version 2.0"
			WRITE(33,'(A, I7)') "Motor: OutputfileCounter = ", OutputfileCounter
			WRITE(33,'(A)') "ASCII"
			WRITE(33,'(A)') "DATASET UNSTRUCTURED_GRID"
			WRITE(33,'(A, I10, A)') "POINTS", CounterBuffer, " float"
	
			DO IM=1, CounterBuffer
				WRITE(33,'(3F10.5)') XMBuffer(IM), YMBuffer(IM), ZMBuffer(IM)
			END DO
	
			WRITE(33,'(A, I10, I10)') "CELLS", CounterBuffer, 2*CounterBuffer
	
			DO IM=1, CounterBuffer
				WRITE(33,'(I3, I10)') 1, IM-1
			END DO
	
			WRITE(33,'(A, I10)') "CELL_TYPES ", CounterBuffer
			DO IM=1, CounterBuffer
				WRITE(33,'(I3)') 1
			END DO
	
	
			CLOSE(33)
	
		END DO


	END SUBROUTINE OutputMotorsVTK



	END MODULE OUTPUT
	
