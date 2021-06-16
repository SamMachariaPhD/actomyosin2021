clear all

Vmax = 7;           % Maximum gliding speed (um/s)
k = 300.0;          % Spring constant (pN/um)
fstall = 0.4;       % Stall force (pN)
frupt = 9.2;        % Rupture force (pN)

Tau1 = 0.025;               % Binding period (s). 1/k_a See Ishigure & Nitta 2015 IEEE Trans. Nanobiosci.
Tau2min = frupt/k/Vmax;

ActiveMotorRatioTemp = 0.01:0.01:0.99;

Tau = Tau1/Tau2min;
f = frupt/fstall;
Gamma = 1.0./ActiveMotorRatioTemp - 1.0;

GammaCritical = ((1.0 + Tau)^2)/2.0/f/Tau
ActiveMotorRatioCritical = 1.0/(GammaCritical + 1.0)

Fid=fopen('Summary.txt','w');
fprintf(Fid,'Critical gamma = %f; Critical ActiveMotorRatio = %f',GammaCritical,ActiveMotorRatioCritical);
fclose(Fid);

Counter = 0;
for I=1:length(Gamma)
    if ActiveMotorRatioTemp(I) > ActiveMotorRatioCritical
        Counter = Counter + 1;
        ActiveMotorRatio(Counter) = ActiveMotorRatioTemp(I);
        Vplus(Counter) = 0.5*Vmax/Tau*(Tau - 1.0 + sqrt((1.0 - Tau)^2 + 4.0*Tau - 2.0*f*Tau.*Gamma(I)));
        Vminus(Counter) = 0.5*Vmax/Tau*(Tau - 1.0 - sqrt((1.0 - Tau)^2 + 4.0*Tau - 2.0*f*Tau.*Gamma(I)));
    end
end



plot(ActiveMotorRatio,Vplus,'r-',ActiveMotorRatio,Vminus,'b.',ActiveMotorRatioCritical,0.0,'ro')
xlabel('Active motor ratio');ylabel('v (um/s)');
axis([0.0 1.0 0.0 8.0])
saveas(gcf,'r-vAll.fig');
saveas(gcf,'r-vAll.png');

figure
plot(ActiveMotorRatio,Vplus,'r-',ActiveMotorRatioCritical,0.0,'ro')
xlabel('Active motor ratio');ylabel('v (um/s)');
axis([0.0 1.0 0.0 8.0])
saveas(gcf,'r-v.fig');
saveas(gcf,'r-v.png');

OutputData = [ActiveMotorRatio;Vplus];
OutputData = OutputData.';
save('r-v.txt','OutputData','-ascii') 