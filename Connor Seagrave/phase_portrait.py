#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def plot_phase_portrait(ode_system, x_range, y_range, title="Phase Portrait",
                        initial_conditions=None, num_ics=10, grid_density=20,
                        vector_color='lightblue', trajectory_color='red',
                        figsize=(8, 6)):

    # Create grid
    x = np.linspace(x_range[0], x_range[1], grid_density)
    y = np.linspace(y_range[0], y_range[1], grid_density)
    X, Y = np.meshgrid(x, y)

    # Compute vector field
    U = np.zeros(X.shape)
    V = np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            dx, dy = ode_system([X[i, j], Y[i, j]])
            U[i, j] = dx
            V[i, j] = dy

    # Plot setup
    plt.figure(figsize=figsize)
    # Vector field (normalised for better visibility)
    M = np.hypot(U, V)
    M[M == 0] = 1  # Avoid division by zero
    U_norm = U / M
    V_norm = V / M
    plt.quiver(X, Y, U_norm, V_norm, M, alpha=0.6,
               cmap='viridis', width=0.005)


    # Integrate and plot trajectories
    t = np.linspace(0, 20, 800)  # Time span
    x0  = input("Initial x Value? ")
    y0  = input("Initial y Value? ")
    sol_forward = euler_solve(ode_system, [x0, y0], t)
    xf, yf = sol_forward[:, 0], sol_forward[:, 1]
    plt.plot(xf, yf, color=trajectory_color, alpha=0.7, linewidth=1)

    # initial points
    #Forgot how to do this lwk
    
    plt.scatter(x0, y0, color='black', s=15, zorder=3, label='Initial points')

    # Axes, labels, grid
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def euler_solve(ode_system, y0, t):
   
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    dt = t[1] - t[0]
    
    for i in range(n-1):
        dy = np.array(ode_system(y[i]))  
        y[i+1] = y[i] + dy * dt  
    
    return y

def harmonic_oscillator(state):
    #Example: dx/dt = y, dy/dt = -x
    x, y = state
    return [y, -x]

def Predator_Prey(state):
    #Example: dx/dt = x(1-y), dy/dt = y(x-1) 
    x, y = state
    return [x * (1 - y), y * (x - 1)]

if __name__ == "__main__":
    
    answr = input("Oscillator(1) or Predator-Prey(2)? ")
    if answr == "1":  
        plot_phase_portrait(
            ode_system=harmonic_oscillator,
            x_range=(-3, 3),
            y_range=(-3, 3),
            title="Phase portrait: Simple harmonic oscillator",
            num_ics=12
        )

    if answr == "2":
        plot_phase_portrait(
            ode_system=Predator_Prey,
            x_range=(0, 4),
            y_range=(0, 4),
            title="Phase portrait: predator‑prey",
            num_ics=15
        )

