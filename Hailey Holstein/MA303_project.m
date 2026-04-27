clc;
clear;

% Input equation dy/dx = f(x,y)
eqn_str = input('Enter f(x): ', 's');

% Convert to function handle
f = str2func(['@(x,y) ' eqn_str]);

% Inputs
h = input('Enter step size: ');
x0 = input('Enter x0: ');
xf = input('Enter final x: ');
y0 = input('Enter y0: ');

x = x0:h:xf;
y = zeros(size(x));
y(1) = y0;

% Euler method
for i = 1:length(x)-1
    y(i+1) = y(i) + h * f(x(i), y(i));
end

% ode45 reference
[x_exact, y_exact] = ode45(f, [x0 xf], y0);

% Plot
figure;
plot(x, y, 'b--', 'LineWidth', 2); hold on;
plot(x_exact, y_exact, 'r', 'LineWidth', 1.5);

grid on;
legend('Euler', 'ode45');
xlabel('x'); ylabel('y');
title(['dy/dx = ', eqn_str]);