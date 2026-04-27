import os
import subprocess
import sys

# --- AUTO-INSTALLER SECTION ---
# This ensures the libraries exist before the math starts
def install_and_import():
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        return np, plt
    except ImportError:
        print("Required libraries not found. Installing numpy and matplotlib...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "matplotlib"])
        import numpy as np
        import matplotlib.pyplot as plt
        return np, plt

# Initialize the libraries
np, plt = install_and_import()

# ==========================================================
# 1. PARAMETER INPUT
# ==========================================================
# System: x' = ax + by, y' = cx + dy
a, b = 0, 2
c, d = -2, 0  # Change these numbers for different output diagrams

def generate_phase_portrait_project(a, b, c, d):
    # --- STEP 1: MATHEMATICAL COMPUTATION ---
    A = np.array([[a, b], [c, d]])
    eigenvalues = np.linalg.eigvals(A)
    trace = np.trace(A)
    det = np.linalg.det(A)
    discriminant = trace**2 - 4*det
    
    # --- STEP 2: STABILITY CLASSIFICATION ---
    if det < 0:
        stability = "Saddle Point (Unstable)"
    elif det > 0:
        if discriminant < 0:
            if trace < 0: stability = "Stable Spiral (Sink)"
            elif trace > 0: stability = "Unstable Spiral (Source)"
            else: stability = "Center (Stable/Neutral)"
        else:
            if trace < 0: stability = "Stable Node (Sink)"
            else: stability = "Unstable Node (Source)"
    else:
        stability = "Degenerate Critical Point"

    # --- STEP 3: CONSOLE REPORT ---
    print("\n" + "="*50)
    print("      MA303 PROJECT: PHASE PORTRAIT ANALYSIS")
    print("="*50)
    print(f"System Equations: x' = {a}x + {b}y")
    print(f"                  y' = {c}x + {d}y")
    print("-" * 50)
    print(f"Eigenvalues: {eigenvalues[0]:.3f}, {eigenvalues[1]:.3f}")
    print(f"Trace (T): {trace} | Determinant (D): {det:.2f}")
    print(f"Stability Type: {stability}")
    print("="*50 + "\n")

    # --- STEP 4: PLOTTING ---
    w = 5
    x = np.linspace(-w, w, 30)
    y = np.linspace(-w, w, 30)
    X, Y = np.meshgrid(x, y)

    DX = a*X + b*Y
    DY = c*X + d*Y

    plt.figure(figsize=(9, 7))
    
    # Professional Streamlines
    plt.streamplot(X, Y, DX, DY, color='royalblue', linewidth=1.2, 
                   density=1.4, arrowstyle='->', arrowsize=1.2)

    # Nullclines
    if b != 0:
        plt.plot(x, -(a/b)*x, color='red', linestyle='--', alpha=0.3, label='x-nullcline (dx/dt=0)')
    if d != 0:
        plt.plot(x, -(c/d)*x, color='green', linestyle='--', alpha=0.3, label='y-nullcline (dy/dt=0)')

    plt.axhline(0, color='black', lw=1.5)
    plt.axvline(0, color='black', lw=1.5)
    plt.title(f"Phase Portrait: {stability}", fontsize=14)
    plt.xlabel("x(t)")
    plt.ylabel("y(t)")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xlim([-w, w])
    plt.ylim([-w, w])
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_phase_portrait_project(a, b, c, d)
