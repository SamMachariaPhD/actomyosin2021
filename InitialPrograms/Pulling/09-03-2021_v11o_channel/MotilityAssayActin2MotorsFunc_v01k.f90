MODULE FUNC

	USE PARAMETERS
	USE mtmod
	
	IMPLICIT NONE
	
	CONTAINS
	
	
	
	!---Subroutine NormRNDNum---------------------------------------------
	!Generate Normal Random Number
	!---------------------------------------------------------------------
	
	SUBROUTINE NormRNDNum(NRN)
	
		USE PARAMETERS, ONLY : DP
		USE mtmod, ONLY : grnd
	
		REAL(KIND = DP), INTENT(OUT) :: NRN
	
		REAL(KIND = DP) :: UR1, UR2
	
	
	
		UR1 = grnd()
		IF (UR1 == 0.0_DP) UR1 = grnd()
		UR2 = grnd()
	
		NRN = DSQRT(-2.0_DP*DLOG(UR1)) * DCOS(2.0_DP*pi*(UR2))
	
	
	END SUBROUTINE NormRNDNum
	
	
	
	!---Subroutine NormRNDVector-----------------------------------------
	!Generate N-Dimensinal Normal Random Vector
	!---------------------------------------------------------------------
	
	SUBROUTINE NormRNDVector(N_Dim, NRV)
	
		USE PARAMETERS, ONLY : DP
		USE mtmod, ONLY : grnd
	
		INTEGER, INTENT(IN) :: N_Dim

		REAL(KIND = DP), DIMENSION(N_Dim), INTENT(OUT) :: NRV
	
		INTEGER :: I

		REAL(KIND = DP) :: UR1, UR2, NR
	
	
	
		DO I=1, N_Dim
	
			UR1 = grnd()
			IF (UR1 == 0.0_DP) UR1 = grnd()
			UR2 = grnd()
	
			NR = DSQRT(-2.0_DP*DLOG(UR1)) * DCOS(2.0_DP*pi*(UR2))
	
			NRV(I) = NR
	
		END DO
	
	END SUBROUTINE NormRNDVector



!---Initial Motor Binding----------------------------------------------------------------
	
	SUBROUTINE InitialMotorBinding(ActiveMotorIdxOffset, ActiveMotorIdxEnd, ContactState, TempContact)
	
		USE PARAMETERS , ONLY : DP, NumFilament, NumBeads

	
		USE mtmod, ONLY : grnd
		
	
		INTEGER(KIND = Range15), INTENT(IN):: ActiveMotorIdxOffset, ActiveMotorIdxEnd

		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(INOUT) :: ContactState, TempContact
		
		INTEGER(KIND = Range15) :: IM
		
		INTEGER :: II

		REAL(KIND = DP) ::	UR
	
	
	
		DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
	
			DO II=1, NumFilament
		
				IF ((TempContact(II, IM) >= 1.0_DP) .AND. (TempContact(II, IM) <= DBLE(NumBeads))) THEN
		
					UR = grnd()
					IF(UR <= 0.1_DP) THEN		! Closer to steady state population of binding motors
						ContactState(II, IM) = TempContact(II, IM)
						TempContact(II, IM) = 0.0_DP
					END IF
		
				END IF
		
			END DO
		
		END DO
	
	
	END SUBROUTINE InitialMotorBinding



!---Initial Motor Location----------------------------------------------------------------

	SUBROUTINE InitialMotorLocations(ActiveMotorIdxOffset, ActiveMotorIdxEnd, IniAngle, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
		USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
	
	
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


	
	!---Subroutine CheckMotorFilamentProximity-------------------------------------
	
	SUBROUTINE CheckMotorFilamentProximity(X, Y, Z, XM_IM, YM_IM, ZM_IM, ContactState_IM, TempContact_IM)
	
		USE PARAMETERS, ONLY : DP, MaxNumMotors, NumFilament, NumBeads, BondLength, CaptureRadius
	
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z
	
		REAL(KIND = DP), INTENT(IN) :: XM_IM, YM_IM, ZM_IM
	
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(IN) :: ContactState_IM

		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(OUT) :: TempContact_IM


	
		REAL(KIND = DP) :: Intercept, SqDistance
	
		INTEGER(KIND = Range15) :: IM
		
		INTEGER :: II, JJ
	
	
	
		Loop_Filament: DO II=1, NumFilament
	
			DO JJ=1, NumBeads-1

				Intercept = (XM_IM - X(JJ,1))*(X(JJ+1,1) - X(JJ,1)) + &
							(YM_IM - Y(JJ,1))*(Y(JJ+1,1) - Y(JJ,1)) + &
							(ZM_IM - Z(JJ,1))*(Z(JJ+1,1) - Z(JJ,1))
				Intercept = Intercept/BondLength
		
				SqDistance = (XM_IM - X(JJ,1))*(XM_IM - X(JJ,1)) + &
							(YM_IM - Y(JJ,1))*(YM_IM - Y(JJ,1)) + &
							(ZM_IM - Z(JJ,1))*(ZM_IM - Z(JJ,1)) - Intercept**2
		
				IF ((SqDistance <= CaptureRadius**2) .AND. (Intercept >= 0.0_DP) .AND. (Intercept <= BondLength)) THEN
					TempContact_IM(II) = DBLE(JJ) + Intercept/BondLength

				END IF

			END DO

		END DO Loop_Filament
	
	END SUBROUTINE CheckMotorFilamentProximity
	
	
	
	!--Motor Binding----------------------------------------------------------------
	
	SUBROUTINE MotorBinding(ContactState_IM, TempContact_IM, MotorStateUpdate_IM)
	
		USE PARAMETERS , ONLY : DP, NumFilament, dt, k_a
	
		USE mtmod, ONLY : grnd
		
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM, TempContact_IM
	
		LOGICAL, INTENT(OUT) :: MotorStateUpdate_IM
	
		REAL(KIND = DP) :: UR
				
		INTEGER :: II
	
	
	
		UR = grnd()
		
		Loop_Filament_ContactCheck: DO II=1, NumFilament

			IF ((TempContact_IM(II) >= 1.0_DP ) .AND. (NINT(ContactState_IM(II)) == 0)) THEN
	
				IF(UR > k_a*dt)THEN  
					TempContact_IM(II) = 0.0_DP
				ELSE
					MotorStateUpdate_IM = .TRUE.
				END IF

			END IF
	
		END DO Loop_Filament_ContactCheck
	
	END SUBROUTINE MotorBinding
	
	
	
	!--Motor Move-------------------------------------------------------------------
	
	SUBROUTINE MotorStep(ContactState_IM, TempContact_IM)
	
		USE PARAMETERS , ONLY : DP, NumFilament, dt, k_a
	
		USE mtmod, ONLY : grnd
	
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM, TempContact_IM
	
	
		INTEGER :: II
	
	
	
		Loop_Filament_ContactCheck: DO II=1, NumFilament
	
			IF (TempContact_IM(II) >= 1.0_DP )THEN
	
						   ContactState_IM(II) = TempContact_IM(II) + Stepsize/BondLength
	
			END IF
	
		END DO Loop_Filament_ContactCheck
	
	END SUBROUTINE MotorStep
	
	
	
	!--Motor Move-------------------------------------------------------------------
	
	SUBROUTINE MotorStuck(ContactState_IM, TempContact_IM)
	
		USE PARAMETERS , ONLY : DP, NumFilament, dt, k_a
	
		USE mtmod, ONLY : grnd
	
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM, TempContact_IM
	
	
		INTEGER :: II
	
	
	
		Loop_Filament_ContactCheck: DO II=1, NumFilament
	
			IF (TempContact_IM(II) >= 1.0_DP )THEN
	
						   ContactState_IM(II) = TempContact_IM(II)
	
			END IF
	
		END DO Loop_Filament_ContactCheck

	END SUBROUTINE MotorStuck
	
	
	
	!---Subroutine Calculate Force Actin on Motor-----------------------------------
	
	SUBROUTINE CalculateForceMotor(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, Z, XM, YM, ZM, ContactState, F_Motor_X, F_Motor_Y, F_Motor_Z, Elongation)
	
	
		USE PARAMETERS, ONLY : DP, MaxNumMotors, NumFilament, CaptureRadius, k
	
	
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(IN) :: XM, YM, ZM
	
		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(IN) :: ContactState
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(OUT) :: F_Motor_X, F_Motor_Y, F_Motor_Z
	
		INTEGER(KIND = Range15), INTENT(IN):: ActiveMotorIdxOffset, ActiveMotorIdxEnd
	
		REAL(KIND = DP) :: Intercept_Contact, X_Contact, Y_Contact, Z_Contact
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(OUT) :: Elongation
	
		INTEGER(KIND = Range15) :: IM
	
		INTEGER :: II, J_Contact
	
	
	
		F_Motor_X = 0.0_DP
		F_Motor_Y = 0.0_DP
		F_Motor_Z = 0.0_DP
	
	
	!$omp parallel
	!$omp do private(J_Contact,Intercept_Contact,X_Contact,Y_Contact,Z_Contact)
		DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
			IF (ContactState(1,IM) >= 1.0_DP) THEN
	
				J_Contact = INT(ContactState(1,IM))
				Intercept_Contact = ContactState(1,IM) - DBLE(J_Contact)
	
				IF (J_Contact >= NumBeads) THEN
					X_Contact = X(NumBeads,1) + Intercept_Contact * (X(NumBeads,1) - X(NumBeads-1,1))
					Y_Contact = Y(NumBeads,1) + Intercept_Contact * (Y(NumBeads,1) - Y(NumBeads-1,1))
					Z_Contact = Z(NumBeads,1) + Intercept_Contact * (Z(NumBeads,1) - Z(NumBeads-1,1))
				ELSE
					X_Contact = X(J_Contact,1) + Intercept_Contact * (X(J_Contact+1,1) - X(J_Contact,1))
					Y_Contact = Y(J_Contact,1) + Intercept_Contact * (Y(J_Contact+1,1) - Y(J_Contact,1))
					Z_Contact = Z(J_Contact,1) + Intercept_Contact * (Z(J_Contact+1,1) - Z(J_Contact,1))
				END IF
	
				Elongation(IM) = (XM(IM) - X_Contact)**2 + (YM(IM) - Y_Contact)**2 + (ZM(IM) - Z_Contact)**2
				Elongation(IM) = DSQRT(Elongation(IM))
	
				F_Motor_X(IM) = k * Elongation(IM) * (XM(IM) - X_Contact)/Elongation(IM)
				F_Motor_Y(IM) = k * Elongation(IM) * (YM(IM) - Y_Contact)/Elongation(IM)
				F_Motor_Z(IM) = k * Elongation(IM) * (ZM(IM) - Z_Contact)/Elongation(IM)
	
			END IF
		END DO
	!$omp end do
	!$omp end parallel
	
	END SUBROUTINE CalculateForceMotor
	
	
	
	!---Subroutine Forced Detachment of Motor---------------------------------------
	
	SUBROUTINE MotorForcedDetachment(F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM, ContactState_IM, Release_ADP_IM, Elongation_IM, MotorType_IM, MotorStateUpdate_IM)
	
	
		USE PARAMETERS, ONLY : DP, MaxNumMotors, NumFilament, k, F_Motor_Detach1, F_Motor_Detach2
	
	
        INTEGER, INTENT(IN) :: MotorType_IM
        
        INTEGER, INTENT(INOUT) :: Release_ADP_IM
		
		REAL(KIND = DP), INTENT(INOUT) :: F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM
	
        REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM
	
		REAL(KIND = DP), INTENT(IN) :: Elongation_IM

        LOGICAL, INTENT(OUT) :: MotorStateUpdate_IM
	
		INTEGER :: II
	
	
	
        SELECT CASE(MotorType_IM)

        CASE (1)

            IF (k*Elongation_IM >= F_Motor_Detach1) THEN
	
                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament1: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = -1.0_DP
                        Release_ADP_IM = 0
                        MotorStateUpdate_IM = .TRUE.
                    END IF
                END DO Scan_Contact_Filament1
        
            END IF

        CASE (2)

            IF (k*Elongation_IM >= F_Motor_Detach2) THEN

                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament2: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = 0.0_DP
                    END IF
                END DO Scan_Contact_Filament2

            END IF

		END SELECT
	
		
	END SUBROUTINE MotorForcedDetachment



		!---Subroutine Forced Detachment of Motor---------------------------------------
	
	SUBROUTINE MotorForcedDetachmentRate(F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM, ContactState_IM, Release_ADP_IM, Elongation_IM, MotorType_IM, MotorStateUpdate_IM)
	
		USE PARAMETERS, ONLY : DP, NumFilament, dt, k, kBT
	
		USE mtmod, ONLY : grnd
	
        	INTEGER, INTENT(IN) :: MotorType_IM
        
        	INTEGER, INTENT(INOUT) :: Release_ADP_IM
		
		REAL(KIND = DP), INTENT(INOUT) :: F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM
	
        	REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM
	
		REAL(KIND = DP), INTENT(IN) :: Elongation_IM

		LOGICAL, INTENT(OUT) :: MotorStateUpdate_IM
	
		INTEGER :: II

		REAL(KIND = DP) :: UR, ForcedDependentDissociationRate
	
	

	
		UR = grnd()
		
		! B. Guo, W. H. Guilford, Proc. Natl. Acad. Sci. U. S. A. 103, 9844–9849 (2006). Table 2
!		ForcedDependentDissociationRate = 15.0_DP*DEXP(k*Elongation_IM*0.0005_DP/kBT) + 150.0_DP*DEXP(-k*Elongation_IM*0.002_DP/kBT)

		! T. Nishizaka, R. Seo, H. Tadakuma, K. Kinosita, S. Ishiwata, Biophys. J. 79, 962–974 (2000). HMM
		ForcedDependentDissociationRate = (1.0_DP/62.0_DP)*DEXP(k*Elongation_IM*0.0027_DP/kBT) + (1.0_DP/950.0_DP)*DEXP(k*Elongation_IM*0.0014_DP/kBT)

        SELECT CASE(MotorType_IM)

        CASE (1)

            IF (UR < ForcedDependentDissociationRate*dt) THEN
	
                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament1: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = -1.0_DP
						Release_ADP_IM = 0
						MotorStateUpdate_IM = .TRUE.
                    END IF
                END DO Scan_Contact_Filament1
        
            END IF

        CASE (2)

            IF (UR < ForcedDependentDissociationRate*dt) THEN

                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament2: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = 0.0_DP
                    END IF
                END DO Scan_Contact_Filament2

            END IF

		END SELECT
		
	END SUBROUTINE MotorForcedDetachmentRate
	


		!---Subroutine Forced Detachment of Motor---------------------------------------
	
	SUBROUTINE MotorForcedDetachmentRateWithCheck(TS, F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM, ContactState_IM, Release_ADP_IM, Elongation_IM, MotorType_IM, MotorStateUpdate_IM)
	
		USE PARAMETERS, ONLY : DP, NumFilament, dt, k, kBT, AreaRenewDiv
	
		USE mtmod, ONLY : grnd
	
        	INTEGER, INTENT(IN) :: MotorType_IM

		INTEGER(KIND = Range15), INTENT(IN) :: TS
        
        	INTEGER, INTENT(INOUT) :: Release_ADP_IM
		
		REAL(KIND = DP), INTENT(INOUT) :: F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM
	
        	REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM
	
		REAL(KIND = DP), INTENT(IN) :: Elongation_IM

		LOGICAL, INTENT(OUT) :: MotorStateUpdate_IM
	
		INTEGER :: II

		REAL(KIND = DP) :: UR, ForcedDependentDissociationRate
	
	

	
		UR = grnd()
		
		! B. Guo, W. H. Guilford, Proc. Natl. Acad. Sci. U. S. A. 103, 9844–9849 (2006). Table 2
!		ForcedDependentDissociationRate = 15.0_DP*DEXP(k*Elongation_IM*0.0005_DP/kBT) + 150.0_DP*DEXP(-k*Elongation_IM*0.002_DP/kBT)

		! T. Nishizaka, R. Seo, H. Tadakuma, K. Kinosita, S. Ishiwata, Biophys. J. 79, 962–974 (2000). HMM
		ForcedDependentDissociationRate = (1.0_DP/62.0_DP)*DEXP(k*Elongation_IM*0.0027_DP/kBT) + (1.0_DP/950.0_DP)*DEXP(k*Elongation_IM*0.0014_DP/kBT)

        SELECT CASE(MotorType_IM)

        CASE (1)

            IF (UR < ForcedDependentDissociationRate*dt) THEN
	
                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament1: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = -1.0_DP
						Release_ADP_IM = 0
						MotorStateUpdate_IM = .TRUE.
                    END IF
                END DO Scan_Contact_Filament1
        
            END IF

        CASE (2)

            IF (UR < ForcedDependentDissociationRate*dt) THEN

                F_Motor_X_IM = 0.0_DP
                F_Motor_Y_IM = 0.0_DP
                F_Motor_Z_IM = 0.0_DP
        
                Scan_Contact_Filament2: DO II=1, NumFilament
                    IF (ContactState_IM(II) >= 1.0_DP) THEN
                        ContactState_IM(II) = 0.0_DP
                    END IF
                END DO Scan_Contact_Filament2

            END IF

		END SELECT

        IF (MOD(TS,AreaRenewDiv)==0) THEN
		    WRITE(20,'(I15, 2F15.5, I3)') TS, k*Elongation_IM, ForcedDependentDissociationRate, MotorType_IM		! Output for checking the program
	    END IF
		
	END SUBROUTINE MotorForcedDetachmentRateWithCheck


	
	!---Subroutine Calculating Force Acting on Bead---------------------------------
	
	SUBROUTINE CalculateForceBead(ActiveMotorIdxOffset, ActiveMotorIdxEnd, ContactState, Force_Bead_X, Force_Bead_Y, Force_Bead_Z, F_Motor_X, F_Motor_Y, F_Motor_Z)
	
		USE PARAMETERS, ONLY : DP, MaxNumMotors, NumFilament
	
	
		REAL(KIND = DP), DIMENSION(NumFilament, MaxNumMotors), INTENT(IN) :: ContactState
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(OUT) :: Force_Bead_X, Force_Bead_Y, Force_Bead_Z
	
		REAL(KIND = DP), DIMENSION(MaxNumMotors), INTENT(IN) :: F_Motor_X, F_Motor_Y, F_Motor_Z
	
		INTEGER(KIND = Range15), INTENT(IN):: ActiveMotorIdxOffset, ActiveMotorIdxEnd
	
		REAL(KIND = DP) :: Intercept_Contact
	
		INTEGER(KIND = Range15) :: IM
	
		INTEGER :: II, J_Contact
	
	
	
		Force_Bead_X = 0.0_DP
		Force_Bead_Y = 0.0_DP
		Force_Bead_Z = 0.0_DP
	
		DO IM=ActiveMotorIdxOffset+1, ActiveMotorIdxEnd
	
			Scan_Contact_Filament: DO II=1, NumFilament
	
				IF (ContactState(II,IM) >= 1.0_DP) THEN
	
					J_Contact = INT(ContactState(II,IM))
					Intercept_Contact = ContactState(II,IM) - DBLE(J_Contact)
	
					IF (J_Contact >= NumBeads) THEN
	
						Force_Bead_X(NumBeads,II) = Force_Bead_X(NumBeads,II) + F_Motor_X(IM)
						Force_Bead_Y(NumBeads,II) = Force_Bead_Y(NumBeads,II) + F_Motor_Y(IM)
						Force_Bead_Z(NumBeads,II) = Force_Bead_Z(NumBeads,II) + F_Motor_Z(IM)
	
					ELSE
	
						Force_Bead_X(J_Contact,II) = Force_Bead_X(J_Contact,II) + (1.0_DP - Intercept_Contact)*F_Motor_X(IM)
						Force_Bead_Y(J_Contact,II) = Force_Bead_Y(J_Contact,II) + (1.0_DP - Intercept_Contact)*F_Motor_Y(IM)
						Force_Bead_Z(J_Contact,II) = Force_Bead_Z(J_Contact,II) + (1.0_DP - Intercept_Contact)*F_Motor_Z(IM)
	
						Force_Bead_X(J_Contact+1,II) = Force_Bead_X(J_Contact+1,II) + Intercept_Contact*F_Motor_X(IM)
						Force_Bead_Y(J_Contact+1,II) = Force_Bead_Y(J_Contact+1,II) + Intercept_Contact*F_Motor_Y(IM)
						Force_Bead_Z(J_Contact+1,II) = Force_Bead_Z(J_Contact+1,II) + Intercept_Contact*F_Motor_Z(IM)
	
					END IF
	
				END IF
	
			END DO Scan_Contact_Filament
	
		END DO
	
	END SUBROUTINE CalculateForceBead
	
	
	
	!---Constraint--------------------------------------------------------
	
	SUBROUTINE Constraint(XItempJ0, YItempJ0, ZItempJ0, XItempJ1, YItempJ1, ZItempJ1, XIJ0, YIJ0, ZIJ0, XIJ1, YIJ1, ZIJ1, StateConstraint)
	
	
		USE PARAMETERS, ONLY : DP, Tol, BondLength
	
	
	
		REAL(KIND = DP), INTENT(INOUT) :: XItempJ0, XItempJ1, YItempJ0, YItempJ1, ZItempJ0, ZItempJ1
	
		REAL(KIND = DP), INTENT(IN) :: XIJ0, XIJ1, YIJ0, YIJ1, ZIJ0, ZIJ1
	
		LOGICAL, INTENT(INOUT) :: StateConstraint
	
		REAL(KIND = DP) :: XI_tempAB, YI_tempAB, ZI_tempAB, XIAB, YIAB, ZIAB, BeadsDisSq, DiffSq, gAB, DX, DY, DZ
	
	
	
		XI_tempAB = XItempJ1 - XItempJ0
		YI_tempAB = YItempJ1 - YItempJ0
		ZI_tempAB = ZItempJ1 - ZItempJ0
	
		XIAB = XIJ1 - XIJ0
		YIAB = YIJ1 - YIJ0
		ZIAB = ZIJ1 - ZIJ0
	
		BeadsDisSq = XI_tempAB**2 + YI_tempAB**2 + ZI_tempAB**2
		DiffSq = BondLength**2 - BeadsDisSq
	
	
		IF (DABS(DiffSq) > 2.0_DP*Tol*BondLength**2) THEN
	
			StateConstraint = .FALSE.
	
			gAB = DiffSq / 4.0_DP / (XI_tempAB*XIAB + YI_tempAB*YIAB + ZI_tempAB*ZIAB)
	
			DX = gAB*XIAB
			DY = gAB*YIAB
			DZ = gAB*ZIAB
	
			XItempJ0 = XItempJ0 - DX
			YItempJ0 = YItempJ0 - DY
			ZItempJ0 = ZItempJ0 - DZ
	
			XItempJ1 = XItempJ1 + DX
			YItempJ1 = YItempJ1 + DY
			ZItempJ1 = ZItempJ1 + DZ
	
		END IF
	
	END SUBROUTINE Constraint

	
	
	!---Subroutine RenewMotorPopulation-----------------------------------
	
	SUBROUTINE RenewMotorPopulation(ActiveMotorIdxOffset, ActiveMotorIdxEnd, X, Y, XM, YM, ZM, ContactState, AddedMotorNum, AreaCounter, EraseCounter, AreaOriginX, AreaOriginY, AreaOriginUx, AreaOriginUy, MotorType)
	
	
		USE PARAMETERS, ONLY : Range15, DP, MaxNumMotors, NumFilament, NumBeads, BondLength, HorizontalLength, VerticalLength, Motor_Density, Type1Ratio
	
	
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
	
	
	
	!---Motor State Conversion------------------------------------------------------
	
	SUBROUTINE MotorStateConv(X, Y, Z, F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM, ContactState_IM, Release_ADP_IM)
	
		USE PARAMETERS
		USE mtmod, ONLY : grnd
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: X, Y, Z
	
		INTEGER, INTENT(INOUT) :: Release_ADP_IM
	
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(INOUT) :: ContactState_IM
	
		REAL(KIND = DP), DIMENSION(NumFilament), INTENT(IN) :: F_Motor_X_IM, F_Motor_Y_IM, F_Motor_Z_IM
	
		REAL(KIND = DP) :: UR, F_Motor_Tangent, k_d
	
		INTEGER(KIND = Range15) :: IM
	
		INTEGER :: II, J_Contact
	
	
	
		DO II=1, NumFilament
	
			J_Contact = INT(ContactState_IM(II))
	
			UR = grnd()
	
			SELECT CASE(J_Contact)
	
			CASE (-1)
	
				IF(UR <= k_hp*dt)THEN
					ContactState_IM(II) = 0.0_DP
				END IF
	
			CASE (0)
	
				IF(UR <= k_hm*dt)THEN
					ContactState_IM(II) = -1.0_DP
				END IF
	
			CASE (1:)
	
				IF (Release_ADP_IM == 0) THEN
	
					IF (J_Contact >= NumBeads) THEN
						F_Motor_Tangent = (F_Motor_X_IM(II)*(X(J_Contact,II) - X(J_Contact-1,II))+ &
							F_Motor_Y_IM(II)*(Y(J_Contact,II) - Y(J_Contact-1,II))+ &
							F_Motor_Z_IM(II)*(Z(J_Contact,II) - Z(J_Contact-1,II)))/BondLength
					ELSE
						F_Motor_Tangent = (F_Motor_X_IM(II)*(X(J_Contact+1,II) - X(J_Contact,II))+ &
							F_Motor_Y_IM(II)*(Y(J_Contact+1,II) - Y(J_Contact,II))+ &
							F_Motor_Z_IM(II)*(Z(J_Contact+1,II) - Z(J_Contact,II)))/BondLength
					END IF
	
					k_d = k_d0*DEXP(-F_Motor_Tangent*delta_x/KBT)
	
					IF(UR <= k_d*dt)THEN
						Release_ADP_IM = 1
					END IF
	
				ELSE
	
					IF(UR <= k_t*ATP*dt)THEN 
						Release_ADP_IM = 0
						ContactState_IM(II) = -1.0_DP
					END IF
	
				END IF
	
			END SELECT
	
		END DO
	
	END SUBROUTINE MotorStateConv
	
	
	
	!---Bending Force Calculation-----------------------------------------
	
	FUNCTION Force_Bending(Coordinate)
	
	
		USE PARAMETERS, ONLY : DP, NumFilament, NumBeads, BondLength, EI
	
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament) :: Force_Bending
	
		REAL(KIND = DP), DIMENSION(NumBeads, NumFilament), INTENT(IN) :: Coordinate
	
		INTEGER :: I, J
	
		REAL(KIND = DP) :: F
	
	
		Force_Bending = 0.0_DP
	
		DO I=1, NumFilament
			DO J=2, NumBeads-1
	
				F = Coordinate(J+1,I) - 2.0_DP*Coordinate(J,I) + Coordinate(J-1,I)
	
				Force_Bending(J-1,I) = Force_Bending(J-1,I) + (-1.0_DP)*F
				Force_Bending(J,I) = Force_Bending(J,I) + 2.0_DP*F
				Force_Bending(J+1,I) = Force_Bending(J+1,I) + (-1.0_DP)*F
	
			END DO
		END DO
	
		Force_Bending = Force_Bending*EI/(BondLength**3)
	
	END FUNCTION Force_Bending
	
	

	END MODULE FUNC
	
