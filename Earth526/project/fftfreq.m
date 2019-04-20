function [f]=fftfreq(npts,dt,alias_dt)
% purpose: returns a vector of the frequencies corresponding to the length
% of the signal and the time step.
% input: npts = number of signal elements (integer)
%        dt= sample spacing in time increments (s)
%        alias_dt(optional)i=
% specifying alias_dt > dt returns the frequencies that would
% result from subsampling the raw signal at alias_dt rather than
% dt. 
% Author: Marlon D. Ramos

    % if there is no third function input to s
    if (nargin < 3)
        alias_dt = dt;
    end

    fmin = -1/(2*dt);     % minimum frequency, [Hz]
    df = 1/(npts*dt);     % frequency sample size, [Hz]

    f0 = -fmin;

    alias_fmin = -1/(2*alias_dt);        % min frequency that will be aliased, [Hz]
    f0a = -alias_fmin;

    ff = mod(linspace(0, 2*f0-df, npts)+f0,  2*f0) - f0;
    fa = mod(ff+f0a, 2*f0a)- f0a;

    %  return the frequency time series
    f = fa;

end
