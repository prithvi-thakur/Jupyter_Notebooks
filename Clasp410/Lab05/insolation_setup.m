function insolation=insolation_setup(solar_constant,lats)
%
% Input 
    % num_lat_zones : Number of latitude zones
    % solar_constant : solar constant (1370 for Earth)
    % lats : vector of points giving latitudes
%    
% Output
    % insolation : average insolation for each latitude band

num_lat_zones = length(lats);       % Number of latitude zones

% adjustable parameters
max_tilt = 23.5;                    % tilt of earth in degrees
days_in_year = 365.0;               % averaging interval and period for insolation
hours_in_day= 24.0;                 % probably obvious
zonal_degrees = 360.0;              

%--------------------------------------------------------------------------
%  daily rotation of earth reduces solar constant by distributing the sun
%  energy all along a zonal band
dlong = 0.01; % Use 1/100 of a degree in summing over latitudes
total_solar = 0.0;
for hour = 1:hours_in_day
    hour_angle = zonal_degrees * hour / hours_in_day;
    for longitude = 1:dlong:zonal_degrees
        sun_angle = longitude - hour_angle;
        total_solar = total_solar + solar_constant ...
            * max (0.0, cos (pi/180.0*sun_angle));
    end
end

solar_constant = total_solar /(hours_in_day * zonal_degrees/dlong);

%--------------------------------------------------------------------------

% initialize insolation to zero

insolation(1:num_lat_zones) = 0.0;

% accumulate normalized insolation through a year
for day = 1:days_in_year
    tilt = max_tilt * cos (2.0*pi*day/days_in_year);
    for j = 1:num_lat_zones
        zenith = min (lats(j)+ tilt,90.0);
        insolation(j) = insolation (j) + cos (zenith*pi/180.);
    end
end

% average unnormalized insolation over one year
% this is the quantity S_i in our class notes and what you want
% to plug into the temperature equation
insolation = solar_constant * insolation / days_in_year;

