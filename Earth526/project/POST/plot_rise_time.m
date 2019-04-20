% PLOT_REST_TIME plots pulse rest time from directly reading data 
%
% SYNTAX	data = plot_rise_time(name)
%
% INPUT 	name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				            The default is the first FltXX_sem2d.* found 
%				            in the current directory.
%		
% OUTPUTS	data.rt  rest time of slip pulse 
%
function data = plot_rise_time(name)

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

Tstart = zeros(data.nx,1);
Tend  = zeros(data.nx,1);
data.rt  = zeros(data.nx,1);

dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 


for k=1:data.nx,
    fseek(fid,4*k,'bof');
    D=fread(fid,data.nt,'single',(data.nx*4+8)*5-4);
    Dmax=max(D);
    
 % start of pulse
  m = find( D<(0.1*Dmax));
  if ~isempty(m)
    m = m(end);
    if m<data.nt
    Tstart(k) = m*data.dt + data.dt*(0.1*Dmax-D(m))/(D(m+1)-D(m)); 
    end
  end

 % end of pulse
  m = find( D>(0.9*Dmax));
  %save '~/m.txt' m -ascii;
  %break;
  if ~isempty(m)
    m = m(1);
    if m>1
    Tend(k) = data.dt*m - data.dt*(D(m)-0.9*Dmax)/(D(m)-D(m-1));
    %Pend(k) = data.x(m) - (data.x(m)-data.x(m-1))*(0.9*Dmax-D(m))/(D(m-1)-D(m));
    end
  end
  
 % calculate rise time
 data.rt(k)=Tend(k)-Tstart(k);
 %data.m=m;
  
end

fclose(fid);





