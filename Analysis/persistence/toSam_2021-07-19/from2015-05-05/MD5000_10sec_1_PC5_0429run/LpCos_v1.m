clear all

DataMatrix=load('TipXY_A001.txt');

DtFile=0.01;

MaxLag=50;
StartFrame=1;
Skip=9;

GetFrame=StartFrame:(Skip+1):((floor((length(DataMatrix) - StartFrame)./(Skip+1))).*(Skip+1));

Xtip=DataMatrix(GetFrame,1);
Ytip=DataMatrix(GetFrame,2);

SkippedTipXY = [Xtip Ytip];

save SkippedTipXY_A001.txt SkippedTipXY -ascii

plot(Xtip,Ytip);

DXtip=diff(Xtip);
DYtip=diff(Ytip);

DD=sqrt(DXtip.^2+DYtip.^2);

DXtip=DXtip./DD;
DYtip=DYtip./DD;



for Lag=0:MaxLag
    Sum=0;
    for I=1:(length(DXtip)-Lag)
            Cos(I,(Lag+1))=DXtip(I).*DXtip(I+Lag)+DYtip(I).*DYtip(I+Lag);
            Sum=Sum+Cos(I,(Lag+1));
    end
    
    if (Lag ~= 0)
        for I=(length(DXtip)-Lag+1):length(DXtip)
            Cos(I,(Lag+1))=NaN;
        end
    end
    
     AveCos(Lag+1)=Sum./(length(DXtip)-Lag);
    
end

save Cos.txt Cos -ascii

AveCos=AveCos';
Dt=(0:MaxLag).*DtFile.*(Skip+1);
Dt=Dt';
OutputData=[Dt AveCos];
save AveCos.txt OutputData -ascii