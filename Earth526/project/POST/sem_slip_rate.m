% SEM_SLIP_RATE read space, time, slip and slip rate from data
%
% SYNTAX	[X,DT,NT,D,V] = sem_slip_rate(name)
%
% INPUT 	name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				            The default is the first FltXX_sem2d.* found 
%				            in the current directory.
%		
% OUTPUTS	X(:) space
%		    D(NX,NT) slip
%		    V(NX,NT) slip rate
%

%function [X,DT,NT,D,V] = sem_slip_rate(name)
function [X,DT,NT,V] = sem_slip_rate(name)

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
[NX,ND,NT,DT] = textread(hdr,'%n%n%n%n',1,'headerlines',1);
[X,Z] = textread(hdr,'%f%f','headerlines',4);

% D=zeros(NX,NT);
V=zeros(NX,NT);

dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 
fseek(fid,4,'bof');

for k=1:NT,
%     d=fread(fid,NX,'single');
%     fseek(fid,8,'cof');
    fseek(fid,NX*4+8,'cof');
    v=fread(fid,NX,'single');
    fseek(fid,(NX*4+8)*3+8,'cof');
%     D(:,k)=d; 
    V(:,k)=v;
end

fclose(fid);
