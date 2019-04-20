% PLOT_RUPTURES plots rupture front, process zone tail and healing
%
% SYNTAX	[Xrup,Xpz,Xhe] = plot_ruptures(V,Veps,D,Dc,X,DT)
%
% INPUTS	V(:,:)	space-time slip velocity data
%		Veps	slip velocty threshold to define rupture front
%		D(:,:)	space-time slip data
%		Dc	slip threshold to define the tail of process zone
%		X(:)	positions of slip and velocity data
%		DT	timestep of slip and velocity data
%		
% OUTPUTS	Xrup(:) rupture locations (for which V=Veps) at each time 
%			with quadratic location interpolation
%		Xpz(:)  location of tail of process zone (for which D=Dc) 
%			at each time, with quadratic location interpolation
%		Xhe(:) 	healing locations (for which V=Veps) at each time 
%			with quadratic location interpolation
%
function [Xrup,Xpz,Xhe] = plot_ruptures(V,Veps,D,Dc,X,DT)

%		T(:)	times of slip and velocity data

NX = length(X);
[N1,N2] = size(V);
if N1==NX
  NT=N2;
elseif N2==NX
  V = V';
  D = D';
  NT=N1;
else
  error('Size mismatch (V/D/X)')
end

Xrup = zeros(NT,1);
Xpz  = zeros(NT,1);
Xhe  = zeros(NT,1);

% force V(1,:)=0 at X=0
%if nnz(V(1,:))
%  V = [zeros(NX,1) V];
%  D = [zeros(NX,1) D];
%end

for k=1:NT,

 % rupture front
  m = find( V(:,k)>Veps );
  if ~isempty(m)
    m = m(end); 
    if m<NX
      Xrup(k) = X(m+1) - (X(m+1)-X(m))*(Veps-V(m+1,k))/(V(m,k)-V(m+1,k));
    end
  end

 % end of process zone
  m = find( D(:,k)>Dc);
  if ~isempty(m)
    m = m(end);
    if m<NX
    Xpz(k) = X(m+1) - (X(m+1)-X(m))*(Dc-D(m+1,k))/(D(m,k)-D(m+1,k)); 
    end
  end
  
  % healing
  m = find( V(:,k)>Veps );
  if ~isempty(m)
    m = m(1); 
    if m>1
      Xhe(k) = X(m-1) + (X(m)-X(m-1))*(Veps-V(m-1,k))/(V(m,k)-V(m-1,k)); 
    else
      Xhe(k) = 0;
    end
  end

end


