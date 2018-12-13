
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                    %
%  Matlab program for one-dimensinal finite element method for       %
%                                                                    %
%    -(k(x)u_x)_x + c(x) u_x + b(x) u(x) = f(x)                      %
%                                                                    %
%  with different boundary condition at x =0, and x = l              %
%                                                                    %
%--------------------------------------------------------------------%

	function [x,u,gk]= fem1d

   clear
%  Preprocessor:

   global nnode nelem 
   global gk gf
   global xi  w

%%%%%%%%% Start the program %%%%%%%%%

   [xi,w] = setint;   % Get Gaussian points and weights.

%  Preprocessor:
   [x,kbc,vbc,kind,nint,nodes] = propset;	      % Input data

    formkf(kind,nint,nodes,x,xi,w);   % Form the discrete system

    aplybc(kbc,vbc);
	gk
	gf

      
    u = gk\gf;	                % Solve the linear system.


    for i=1:nnode,
      e(i) = u(i) - uxeact(x(i));
    end
    figure(1); plot(x,u)
    figure(2); plot(x,e)


