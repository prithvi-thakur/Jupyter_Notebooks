function y=gaussian_weight(x,h)
y=exp(-x^2/2/h^2)/sqrt(2*pi*h^2);