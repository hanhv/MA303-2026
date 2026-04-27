# The goal of this project was to develop a Python-based tool to approximate solutions for first-order Initial Value Problems (IVPs). By comparing a first-order method (Euler) with a second-order method (Improved Euler/Heun's), we can visualize how "corrector" steps significantly reduce cumulative error. For the problem, we use a first order differential equation, then apply Euler's methoid (uses tangent line to predict y from current point at the next step). Heun's method is also applied, and this method includes a predictor step (intermediate value is calculated using a standard Euler step) and a corrector step (slope is calculated at new predicted point and averaged with in initial slope). These methods were implemented through Python, using numpy for array handling, matplotlip for visual comparisons between approximations and analytical solution, and loop to ensure the the method's are compared over the exact same intervals. 

import numpy as np
import matplotlib.pyplot as plt

def solve_ode_study(f, exact_f, t0, y0, tn, h):
    # Comparison of the Euler and Improved Euler's Method
    steps = int((tn - t0) / h)
   
    # Linspace for precision between the intervals
    t_values = np.linspace(t0, tn, steps + 1)
   
    # Initialize the arrays before using them
    y_euler = np.zeros(len(t_values))
    y_improved = np.zeros(len(t_values))
   
    y_euler[0] = y0
    y_improved[0] = y0
   
    for i in range(steps):
        t = t_values[i]
       
        # Euler's Method
        y_euler[i+1] = y_euler[i] + h * f(t, y_euler[i])
       
        # Improved Euler's Method
        # Predictor Step
        k1 = f(t, y_improved[i])
        y_predict = y_improved[i] + h * k1
        # Corrector Step
        k2 = f(t + h, y_predict)
        y_improved[i+1] = y_improved[i] + (h/2) * (k1 + k2)
       
    # Exact Solution and Error Calculations
    y_exact = exact_f(t_values)
    err_euler = np.abs(y_exact - y_euler)
    err_improved = np.abs(y_exact - y_improved)
   
    # Display Results
    print(f"{'t':>5} | {'Exact':>10} | {'Euler Err':>10} | {'Imp Euler Err':>14}")
    print("-" * 55)
    for i in range(len(t_values)):
        print(f"{t_values[i]:5.2f} | {y_exact[i]:10.6f} | {err_euler[i]:10.6f} | {err_improved[i]:14.6f}")
       
    return t_values, y_euler, y_improved, y_exact

# Variables for the problem
diff_eq = lambda t, y: y - t**2 + 1
exact_sol = lambda t: (t + 1)**2 - 0.5 * np.exp(t)


t_axis, e_vals, ie_vals, actual = solve_ode_study(
    f=diff_eq,
    exact_f=exact_sol,
    t0=0,
    y0=0.5,
    tn=2,
    h=0.2
)

# Table/Plotting
plt.figure(figsize=(9, 5))
plt.plot(t_axis, actual, 'k-', label='Exact Solution', alpha=0.7)
plt.plot(t_axis, e_vals, 'ro--', label='Euler Method', markersize=4)
plt.plot(t_axis, ie_vals, 'bs-', label='Improved Euler', markersize=4)
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Numerical Approximation: Euler vs. Improved Euler')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()