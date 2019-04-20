% Matlab tools for plot visualization
addpath ../POST

% and add a nice colormap 
%batlow=load('~/ScientificColourMaps5/batlow/batlow.mat');

% read data
data3 = sem2d_read_seis;

% create the time-series
time = (1:data3.nt)*data3.dt;

figure();
plot(time, data3.ux, 'linewidth', 2);
figure(gcf)

% plot sliprate