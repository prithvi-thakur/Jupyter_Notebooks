
x0=0.5; y0=2; xfinal=3; n1=20;
[x1,y1] = euler_simple_f(x0,y0,xfinal,n1,'f3');

plot(x1,y1,'o')
hold
[x1,y1] = euler_simple_f(x0,y0,xfinal,160,'f3');
plot(x1,y1)

