% PLOT_PEAK_SLIP_RATE reads peak slip rate with spacefrom SEM2DPACK
%
% SYNTAX	data = plot_peak_slip_rate(name)
%
% INPUT		name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				The default is the first FltXX_sem2d.* found 
%				in the current directory.
%
% OUTPUT	data.peakv       peak slip rate with space
%
function data = plot_peak_slip_rate(name)

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

% calculate peak slip rate
data.peakv=zeros(data.nx,1);
dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 

for k=1:data.nx,
    fseek(fid,data.nx*4+8+4*k,'bof');
    V=fread(fid,data.nt,'single',(data.nx*4+8)*5-4);
    data.peakv(k)=max(V);
end

fclose(fid);


