% SEM_SLIP_RATE_STRESS read space, time, slip, slip rate and stress from data
%
% SYNTAX	data = sem_slip_rate_stress(name)
%
% INPUT 	name	[Flt*] 	prefix of header and data files (name_sem2d.*) 
%				            The default is the first FltXX_sem2d.* found 
%				            in the current directory.
%		
% OUTPUTS	data.x(:) space
%		data.d(NX,NT) slip
%		data.v(NX,NT) slip rate
%               data.st(NX,NT) stress
%               data.sn        normal stress
%               data.mu        friction coefficient
%
function data = sem_slip_rate_stress(name)

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

%%data.d=zeros(data.nx,data.nt);
data.v=zeros(data.nx,data.nt);
data.st=zeros(data.nx,data.nt);
%%data.sn=zeros(data.nx,data.nt);
data.mu=zeros(data.nx,data.nt);

dat  = strcat(name,'_sem2d.dat');
fid=fopen(dat); 
fseek(fid,4,'bof');

for k=1:data.nt,
%%    d=fread(fid,data.nx,'single');
%%    fseek(fid,8,'cof');
    fseek(fid,data.nx*4+8,'cof');
    v=fread(fid,data.nx,'single');
    fseek(fid,8,'cof');
    st=fread(fid,data.nx,'single');
%%    fseek(fid,(NX*4+8)*2+8,'cof');
%%    fseek(fid,8,'cof');
%%    sn=fread(fid,data.nx,'single');
%%    fseek(fid,8,'cof');
    fseek(fid,data.nx*4+8+8,'cof');
    mu=fread(fid,data.nx,'single');
    fseek(fid,8,'cof');
    data.v(:,k)=v; data.st(:,k)=st; data.mu(:,k)=mu;
end

fclose(fid);
