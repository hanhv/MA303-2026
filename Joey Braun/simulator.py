import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm, colors
from sympy import symbols, lambdify, sin, cos, pi, exp, sympify
import tkinter as tk
from tkinter import messagebox

def run_simulation():
    try:
        def parse_val(val):
            return float(sympify(val))

        # --- 1. GET INPUTS ---
        L = parse_val(entry_L.get())
        alpha = parse_val(entry_alpha.get())
        b_type = var_boundary.get()
        
        f_raw_str = entry_f.get()
        f_str = f_raw_str.replace('^', '**')
        
        # --- 2. SETUP MATH  ---
        x_sym = symbols('x') 

        f_func = lambdify(x_sym, f_str, modules=['numpy', {'sin': np.sin, 'cos': np.cos, 'pi': np.pi, 'exp': np.exp}])
        
        # Calculate stabilization time
        T_steady = (7 * L**2) / (alpha * np.pi**2)
        
        # Discretization
        nx = 75
        dx = L / (nx - 1)
        dt = (0.2 * dx**2) / alpha 
        nt = int(T_steady / dt)
        r = alpha * dt / (dx**2)
        
        x_vals = np.linspace(0, L, nx)
        u = f_func(x_vals)
        
        if np.any(np.iscomplex(u)):
            raise ValueError("The initial condition resulted in complex numbers.")

        save_interval = max(1, nt // 500) #lower num quicker animation
        history = [u.copy()]
        time_points = [0]

        # --- 3. SIMULATION ENGINE ---
        for n in range(1, nt + 1):
            u_next = u.copy()
            u_next[1:-1] = u[1:-1] + r * (u[2:] - 2*u[1:-1] + u[0:-2])
            
            if b_type == "Dirichlet (u=0)":
                u_next[0], u_next[-1] = 0, 0
            else:
                u_next[0], u_next[-1] = u_next[1], u_next[-2]
            
            u = u_next
            if n % save_interval == 0:
                history.append(u.copy())
                time_points.append(n * dt)

        # --- VISUALIZATION SETUP ---
        plt.close('all')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        initial_min, initial_max = np.min(history[0]), np.max(history[0])
        norm = colors.Normalize(vmin=min(0, initial_min), vmax=max(0, initial_max))
        cmap = cm.coolwarm 
        
        line, = ax.plot(x_vals, history[0], lw=3)
        time_text = ax.text(0.05, 0.92, '', transform=ax.transAxes, fontsize=12, fontweight='bold')
        
        padding = (initial_max - initial_min) * 0.1
        ax.set_ylim(initial_min - padding, initial_max + padding)
        ax.set_title(f"Normalized Simulation\n$f(x) = {f_str}$", fontsize=14)
        
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        fig.colorbar(sm, ax=ax, label="Temperature")

        def update(frame):
            curr_u = history[frame]
            line.set_ydata(curr_u)
            
            # Color based on the current "energy" (max absolute value)
            current_peak = np.max(np.abs(curr_u))
            line.set_color(cmap(norm(current_peak)))
            
            # Display the PHYSICAL time, even though the REAL time is 10s
            time_text.set_text(f'Time (t): {time_points[frame]:.4f}s')
            return line, time_text

        ani = FuncAnimation(fig, update, frames=len(history), interval=50, repeat=False, blit=True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Computation failed.\n{e}")

# --- GUI SETUP ---
root = tk.Tk()
root.title("MA303: Auto-Stabilizing Heat Simulator")
root.geometry("450x400")

tk.Label(root, text="MA303 1D Heat Equation Visualizer", font=('Helvetica', 12, 'bold')).pack(pady=10)

fields = [("Length of Rod (L):", "pi"), ("Diffusivity (k):", "1.0"), ("Initial Condition u(x):", "4*sin(2*x)")]
entries = {}
for text, default in fields:
    frame = tk.Frame(root); frame.pack(fill=tk.X, padx=20, pady=5)
    tk.Label(frame, text=text, width=20, anchor='w').pack(side=tk.LEFT)
    ent = tk.Entry(frame); ent.insert(0, default); ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries[text] = ent

entry_L, entry_alpha, entry_f = [entries[f[0]] for f in fields]

var_boundary = tk.StringVar(root); var_boundary.set("Dirichlet (u=0)")
tk.OptionMenu(root, var_boundary, "Dirichlet (u=0)", "Neumann (Insulated)").pack(pady=10)

tk.Button(root, text="Run Demo", command=run_simulation, bg="#08b3e7", fg="white", font=('bold')).pack(pady=20)

root.mainloop()
