clear all

% See AnalyticalModel_MotilityAssayWithDefectiveMotors_2020-05-22.pdf

% Parameters
Vmax = 7;           % Maximum gliding speed (um/s)
k = 300.0;          % Spring constant (pN/um)
fstall = -0.4;      % Stall force (pN)
frupt = -9.2;       % Rupture force (pN)
Tau1 = 0.025;       % Binding period (s). 1/k_a See Ishigure & Nitta 2015 IEEE Trans. Nanobiosci.


% Values of active motor ratio investigated
ActiveMotorRatio = [0.8 0.853721 0.9 0.95];

% Gliding speed
V = 0.0:0.1:Vmax;

% f-V relation
fV = fstall*(1.0 - V/Vmax);

% V-fimp relation
fFric = zeros(length(ActiveMotorRatio),length(V));
for I=1:length(ActiveMotorRatio)
    fFric(I,:) = (1/ActiveMotorRatio(I) - 1.0)*0.5*frupt*frupt/k/Tau1./(frupt/k/Tau1 - V);
end

% Plot
plot(fV,V,'b-');hold on
for I=1:length(ActiveMotorRatio)
plot(fFric(I,:),V,'r-')
end
hold off
xlabel('f (pN)');ylabel('v (um/s)');axis([-1.2 0.0 0.0 7.0]);
