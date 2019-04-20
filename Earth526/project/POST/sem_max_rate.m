% sem_max_rate reads peak slip rate with spacefrom SEM2DPACK
%
% SYNTAX	data = plot_peak_slip_rate(name)
%
% INPUT		name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				The default is the first FltXX_sem2d.* found 
%				in the current directory.
%
% OUTPUT	peakv       peak slip rate with space
%
function [X,peakv] = plot_peak_slip_rate(name)

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
[NX,DX,NT,DT] = textread(hdr,'%n%n%n%n',1,'headerlines',1);
[X,Z] = textread(hdr,'%f%f','headerlines',4);

% calculate peak slip rate
peakv=zeros(NX,1);
dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 

for k=1:NX
    fseek(fid,NX*4+8+4*k,'bof');
    V=fread(fid,NT,'single',(NX*4+8)*5-4);
    peakv(k)=max(V);
end

fclose(fid);
