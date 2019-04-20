% script to visualize results of a rupture simulation including
% slip-rate(x,t), rupture front, seismograms, cohesion zone (process zone)
% Author: MDR
% 

clear; clc; 
datadir = './test2/';          % path to data  

% Matlab tools for plot visualization
addpath ./POST
addpath ./test2/

% and add a nice colormap 
%batlow=load('~/ScientificColourMaps5/batlow/batlow.mat');

% read data
data = sem2d_read_seis('./test2');

% create the time-series
time3 = (1:data.nt)*data.dt;

%%
% read in fault information
f3 = sem2d_read_fault;               
TAU0=f3.st0;                          % initial shear stress  [Pa]
x3=f3.x;                               % x-coordinates of fault nodes [m]
z3=f3.z; 
normalStress = f3.sn0;                % normal stress [Pa]
mu_static = 0.7;                     % static friction coefficient 
mu_dynamic = 0.6;                    % dynamic friction coefficient
TAUS= mu_static .* normalStress;     % static shear strength [Pa]
TAUD= mu_dynamic .* normalStress;    % dynamic shear strength [Pa]
delta_TAUE=abs(TAUS)-TAU0;           % strength excess (as defined in Galis et al., 2015)
TAUO_nucleate=abs(TAUS) + (0.005*delta_TAUE);
slipRate3 = f3.v;                      % fault slip-rate [m/s]
finalSlip3 = f3.d(:,end);              % final slip profile at t=tfinal
scale = 1.0E6;                       % convert Pa to MPa

numTimeSteps3 = f3.nt; 
dt3 = f3.dt;                        % [s]
time3 = (1:numTimeSteps3)*dt3;  % time [s]

%% 
close all 
h= figure('color', 'w');
p1=plot(x3, TAU0/scale); hold on; grid on; 
p2=plot(x3, -normalStress/scale, 'b-');
p3=plot(x3, -TAUS/scale, '--'); p4=plot(x3, -TAUD/scale, '-');
legend([p1, p2, p3, p4],'$$ \tau_{o} $$ ', '$$ \sigma_{n} $$ ', ...
                            '$$ \tau_{s} $$ ','$$ \tau_{d} $$ ');
                             % \tau^{nucleate}_{o}')
xlabel('x [m]'); ylabel('stress amplitude [MPa]'); 
ylim([70 150]); 
ax=gca; ax.GridLineStyle=':'; 
set( findall( h, '-property', 'Interpreter' ), 'Interpreter' , 'latex' );
set( findall( h, '-property', 'LineWidth' ), 'LineWidth' , 2.5 );
set( findall( h, '-property', 'FontSize' ), 'FontSize' , 16);
% print(h, '-dpng', '-r400','asperity_example.png') 

%% 

%% 
h = figure(1); clf 
imagesc( x3, time3, slipRate3'); axis xy % slipRate (time, distance) 
% ylim([0 max(time)]);  % zlim ([-0.5 6])
ylim([min(time3) max(time3)]); 
xlim([min(x3) max(x3)]);
%colormap(batlow.batlow)
t = colorbar; caxis([0  3])  % [m/s]
set(t,'position',[0.91 .119 .03 .24], 'Color', 'k'); 
ylabel(t,'slip-rate (m/s)', 'Color', 'k','fontsize', 13)
xlabel('x (m)'); ylabel('T (s)'); % zlabel('slip-rate (m/s)')
title('spatiotemporal rupture slip-rate')
set( findall( h, '-property', 'LineWidth' ), 'LineWidth' , 2.0 );
set( findall( h, '-property', 'FontWeight' ), 'FontWeight' , 'bold');
set( findall( h, '-property', 'FontSize' ), 'FontSize' , 14);
h.Position=[918 323 833 610]; 
h.Color='w'; 
%print(h, '-dpng', '-r400','results_slipRate_history.png')
%% plot seismograms
% Read seismogram outputs from SEM2DPACK
data = sem2d_read_seis(); 
delta_t = data.dt;                        % [s]
t = (1:data.nt)*delta_t;  % time [s]

%% 
h=figure(2); clf 
subplot(2,2, [1,3])
plot(data.x, data.z, 'k<', 'markersize', 18); grid on; 
xlabel('x (m)'); ylabel('z (m)'); title('seismometers')
xlim([0 max(data.x)+10]); ylim([0 max(data.z)+10])
subplot(222)
uz=data.uz; 
plot(t, uz, '-'); grid on; 
title('v_{z}(x,t)'); ylabel('amplitude (m/s)')
xlim([0 max(t)])
legend('near', 'intermediate', 'far')

subplot(224)
ux=data.ux; 
plot(t, ux, '-'); grid on; 
title('v_{x}(x,t)')
xlim([0 max(t)])
legend('near', 'intermediate', 'far')
xlabel('time (s)'); ylabel('amplitude (m/s)')
set( findall( h, '-property', 'LineWidth' ), 'LineWidth' , 1.5 );
set( findall( h, '-property', 'FontWeight' ), 'FontWeight' , 'bold');
set( findall( h, '-property', 'FontSize' ), 'FontSize' , 14);
h.Position=[660 432 1129 575]; h.Color='w'; 
print(h, '-dpng', '-r400','waveform_results.png')