% PLOT_READ_RUPTURES plots rupture front, process zone tail and healing
% from directly reading data
%
% SYNTAX	[Xrup,Xpz,Xhe,NT,DT] = plot_read_ruptures(Veps,Dc)
%
% INPUT 	name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				            The default is the first FltXX_sem2d.* found 
%				            in the current directory.
%		
% OUTPUTS	Xrup(:) rupture locations (for which V=Veps) at each time 
%			with quadratic location interpolation
%		    Xpz(:)  location of tail of process zone (for which D=Dc) 
%			at each time, with quadratic location interpolation
%		    Xhe(:) 	healing locations (for which V=Veps) at each time 
%			with quadratic location interpolation
%
function [Xrup,Xpz,Xhe,NT,DT] = plot_read_ruptures(Veps,Dc)

% assumes header file name is FltXX_sem2d.hdr
if ~exist('name','var')
  list = dir('Flt*.hdr');
  list = {list.name};
  if isempty(list)
    name = '';
  else
    name=list{1}(1:5);
  end
end

% Read parameters from header file
hdr = strcat(name,'_sem2d.hdr');
if ~exist(hdr,'file')
  data=[];
  warning(['File ' hdr ' not found'])
  return
end
[data.nx,ndat,data.nt,data.dt] = textread(hdr,'%n%n%n%n',1,'headerlines',1);
[data.x,data.z] = textread(hdr,'%f%f','headerlines',4);

Xrup = zeros(data.nt,1);
Xpz  = zeros(data.nt,1);
Xhe  = zeros(data.nt,1);
NT=data.nt;DT=data.dt;
% Veps=0.001;
% Dc=1.0;

dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 
fseek(fid,4,'bof');

for k=1:data.nt,
    D=fread(fid,data.nx,'single');
    fseek(fid,8,'cof');
    V=fread(fid,data.nx,'single');
    
 % rupture front
  m = find( V>Veps );
  if ~isempty(m)
    m = m(end); 
    if m<data.nx
      Xrup(k) = data.x(m+1) - (data.x(m+1)-data.x(m))*(Veps-V(m+1))/(V(m)-V(m+1));
    end
  end

 % end of process zone
  m = find( D>Dc);
  if ~isempty(m)
    m = m(end);
    if m<data.nx
    Xpz(k) = data.x(m+1) - (data.x(m+1)-data.x(m))*(Dc-D(m+1))/(D(m)-D(m+1)); 
    end
  end
  
  % healing
  m = find( V>Veps );
  if ~isempty(m)
    m = m(1); 
    if m>1
      Xhe(k) = data.x(m-1) + (data.x(m)-data.x(m-1))*(Veps-V(m-1))/(V(m)-V(m-1)); 
    else
      Xhe(k) = 0;
    end
  end
  
  fseek(fid,(data.nx*4+8)*3+8,'cof');
  
end

fclose(fid);





