% script to calculate frequency of the process zone 
clear; clc; 

v=0.25; 
sigma_n=130E6;   % MPa
MuS=0.6; 
MuD=0.5; 
strengthExcess=(MuS-MuD)*sigma_n;
G=30E9; 
dc_data=load('dc_fmt.txt');
% Dc=dc_data(:,2);    % along-fault distribution of Dc, [m]

x=dc_data(:,1);
x=linspace(0, 25000, 100); 
Dc=1.0*ones(size(x)); 
Vr=(15-10)/(9.5-6.8);    % km/s, average rupture velocity
Vr=Vr*1000;              % m/s
A=1.0;                   % technically a function of Vr
processZone_freq=(1-v)*strengthExcess*Vr./(G*Dc)*A;

f=figure(1); clf 
subplot(211)
plot(x/1000, processZone_freq, 'linewidth', 2); 
xlabel('x'); ylabel('f_{pz}'); title('homogeneous D_{c} model')
% xlim([0 50])
subplot(212)
plot(x/1000, Dc, 'linewidth', 2); 
xlabel('x (km)'); ylabel('D_{c} (m)');

set( findall( f, '-property', 'FontSize' ), 'FontSize', 16 );
set( findall( f, '-property', 'LineWidth' ), 'LineWidth', 1.6 );
print(f, '-dpng', '-r500', 'dc_fpz_homogeneous.png')

%% nucleation

function [L_nuc, Lo]=mode2_critical_crack_length(Dc, v, MuS, MuD, sigma_n, G, tau0)
% purpose: compute the minimum nucleation length for an unstable crack to
% spontaneously nucleate into an earthquake rupture. Valid only for an
% isotrpic, homogeneous medium. Note that the true numerical simulation
% length for Lnuc should be slightly larger than Lnuc calculated by this
% function. 
% input: Dc=critical slip-weakening distance (m)
%        v=Poisson's ratio
%        G = shear modulus [Pa]
%        MuS=static friction coefficient
%        MuD=dynamic friction coefficient
%        sigma_n=normal stress amplitude (Pa)
%        tau0=initial shear stress amplitude (Pa)
% 
% output: calculate the critical half-crack length for earthquake nucleation
% for a Mode II (in-plane) rupture
% Author: Marlon Ramos 
     
    % define fault strengths and relative stress levels 
    taus=MuS*sigma_n;       % static 
    taud=MuD*sigma_n;       % dynamic
    strengthExcess=taus-taud; 
    stressDrop=tau0-taud;     % dynamic stress drop, technically [Pa]
    
    Lo=(1/(1-v))* ((G/pi)*(strengthExcess))/(stressDrop^2) * Dc; % 9()
    L_nuc=2*Lo; 

end 

