% PLOT_PULSE_WIDTH plots pulse width from directly reading data 
%
% SYNTAX	data = plot_pulse_width(name)
%
% INPUT 	name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				            The default is the first FltXX_sem2d.* found 
%				            in the current directory.
%		
% OUTPUTS	data.pw  pulse width of slip 
%
function data = plot_pulse_width(name)

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

Pstart = zeros(data.nt,1);
Pend  = zeros(data.nt,1);
data.pw  = zeros(data.nt,1);

dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 
fseek(fid,4,'bof');

for k=1:data.nt,
    D=fread(fid,data.nx,'single');
    Dmax=max(D);
    
 % start of pulse
  m = find( D<(0.1*Dmax));
  if ~isempty(m)
    m = m(1);
    if m>1
    Pstart(k) = data.x(m) - (data.x(m)-data.x(m-1))*(0.1*Dmax-D(m))/(D(m-1)-D(m)); 
    end
  end

 % end of pulse
  m = find( D>(0.9*Dmax));
  %save '~/m.txt' m -ascii;
  %break;
  
  if ~isempty(m)
    m = m(end);
    if m<data.nx
    Pend(k) = data.x(m) + (data.x(m+1)-data.x(m))*(D(m)-0.9*Dmax)/(D(m)-D(m+1));
    %Pend(k) = data.x(m) - (data.x(m)-data.x(m-1))*(0.9*Dmax-D(m))/(D(m-1)-D(m));
    end
  end
  
 % calculate pulse width
 data.pw(k)=Pstart(k)-Pend(k);
 data.m=m;
  
  fseek(fid,(data.nx*4+8)*4+8,'cof');
  
end

fclose(fid);





