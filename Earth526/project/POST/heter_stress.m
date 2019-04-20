% stress = heter_stress(L1,L2,H,N,DX,nr,auto,unify)
%
% PURPOSE	Heterogeneous 1D stress field:
%		random variables with normal (Gaussian) pdf,
%		von Karman auto-correlation function 
%               (power law spectrum truncated at large scales) 
%               and gaussian smoothing at short scales.
% 		The power spectrum (amplitude^2) is 
% 		  P(k) = 1/(K1^2 + k^2)^p  * exp(-(L2*k).^2)
%		where K1 = 1/L1 and p = 0.5+H
%
% INPUT		L1 	large scale cut-off length (power law spectrum)
%		L2 	short scale cut-off length (gaussian smoothing)
%		H  	Hurst exponent
%		N  	number of sampling points
%		DX 	sampling interval
%		nr	[1] number of realizations
%		auto	[0] compute instead the autocorrelation function
%		unify	[0] changes the pdf from normal to uniform
%
% OUTPUT	stress(1:N,1:nr)
%			heterogeneous field, normalized with mean=0 and std=1
%
% NOTES		. In euclidian dimension E: p=E/2+H  (in 2D: p=H+1)
% 		. Fractal dimension: D = E+1-H (p=4-D)
%		. The 1D autocorrelation function is
%			r^H*K_H(r) /(Gamma(H)*2^(H-1))  where r = x/L1. 
% 		. The spectral factor for gaussian smoothing is 
%			exp(-0.5*(L2*k).^2)
%                 so the spatial filter is proportional to
%			exp(-0.5*(x/L2).^2)
%                 (the tail < 1% beyond x=3*L2)
%  		. when L2>0, use unify=1 at your own risk:
%		  the short-scale Gaussian smoothing is not well preserved
%
% AUTHOR	Jean-Paul Ampuero 	ampuero@erdw.ethz.ch
%

% CHANGELOG 	02-Aug-2007	+ fixed major bug: the Gaussian filter was scratching 
%				  the von Karman field when L2>0
%				+ added factor 0.5 to the Gaussian argument 
%
%               21-Nov-2007	+ added "unify", reshuffling to get a uniform pdf
%
% TO DO		. fix Gaussian smoothing when unify=1
%		. introduce Cauchy and Levy variables

function stress = heter_stress(L1,L2,H,N,DX,nr,autocorr,unify)


%-- Parse inputs

% to avoid re-computations when multiple calls with same inputs:
% check that input parameters have not been used before
persistent PARS fw
parsin = [L1 L2 H N DX];
isnew = ~isequal(PARS,parsin);

if nargin<6, nr=1; end
if nargin<7, autocorr=0; end
if nargin<8, unify=0; end


%-- Compute amplitude spectrum

if isnew
  PARS = parsin;
 % wavenumbers
  dk = 2*pi/(N*DX) ;
  k = [ [0:N/2] [-N/2+1:-1] ]'*dk;
 % von Karman amplitude spectrum 
  halfP = (H+0.5)/2;
  K1 = 1/L1;
  fw = (1+ (k/K1).^2).^(-halfP); 
 % Gaussian filter
  if L2>0, fw = fw .* exp(-0.5*(L2*k).^2); end  
 % normalize to std=1
  fw = fw/ std( real(ifft(fw)) ); 
end

%-- Compute auto-correlation function
if autocorr
  fs = fw.^2 ;
  stress = real( ifft(fs) );
  stress=stress/max(stress);

%-- Compute stochastic stress fields
else

 % flat spectrum with random phase
  theta = rand(N/2-1,nr);
  ph = exp(1i*2*pi*theta);
  fs = [zeros(1,nr); ph; zeros(1,nr); conj(ph(end:-1:1,:)) ]; 
 % Note: zero amplitude at wavenumber=0 to produce the normalization mean=0
 % Note: spectral amplitude at Nyquist wavenumber must be real,
 %       here it is set to zero (but could instead be = +/- 1 with random sign)

 % Combine random phase and von Karman/Gaussian spectrum
  fs = fs.*repmat(fw,1,nr);
  stress = real(ifft(fs));
end

% from Martin Mai's LvsDepthModel.m
%%% make the distribution actually uniform; that changes things
%%% a little bit, but keeps the structure 
if unify
 for k=1:nr,
  [ss,ii] = sort(stress(:,k));                  %% sorting the original distribution
  bb  = unifrnd(min(ss),max(ss),N,1);           %% target distribution
  bb2 = sort(bb);                               %% sort target distribution
  stress(ii,k) = bb2;                           %% map target dist. into original dist.
                                                %% using the indices that preserve 'location'
 end
end
% Note: this shuffling trick seems to preserve well the von-Karman part of the spectrum
% but not the Gaussian smoothing part.
% Maybe the Gaussian smoothing should be applied after the shuffling trick?
