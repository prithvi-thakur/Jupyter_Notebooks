% PLOT_MODEL plots velocity and density model

grid = sem2d_read_specgrid();

figure;
subplot(311)
cp = sem2d_snapshot_read('Cp');
sem2d_snapshot_plot(cp,grid,[0 inf]);
box on
title('Cp (m/s)')
% xlim([0 inf]);ylim([0 5]);
colorbar

subplot(312)
cs = sem2d_snapshot_read('Cs');
sem2d_snapshot_plot(cs,grid,[0 inf]);
box on
title('Cs (m/s)')
xlim([0 inf]);ylim([0 5])
colorbar

subplot(313)
rho = sem2d_snapshot_read('Rho');
sem2d_snapshot_plot(rho,grid,[0 inf]);
box on
title('density (kg/m^3)')
xlim([0 inf]);ylim([0 5])
colorbar

