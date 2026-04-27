"""
MA303 Project: Euler's Method ODE Solver

This program approximates solutions to first-order differential equations
using Euler's Method.

It can also compare the numerical solution to an exact solution when provided.
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def parse_function(expr_text):
    """
    Convert a user-entered expression like 'x + y' into a callable f(x, y).
    """
    x, y = sp.symbols('x y')
    expr = sp.sympify(expr_text)
    f = sp.lambdify((x, y), expr, 'numpy')
    return f, expr


def parse_exact_solution(expr_text):
    """
    Convert a user-entered exact solution like 'exp(x)'
    into a callable y(x).
    """
    x = sp.symbols('x')
    expr = sp.sympify(expr_text)
    f = sp.lambdify(x, expr, 'numpy')
    return f, expr


def euler_method(f, x0, y0, h, xn):
    """
    Approximate the solution of y' = f(x,y), y(x0)=y0
    from x0 to xn using step size h.
    """
    x_values = np.arange(x0, xn + h, h)
    y_values = np.zeros(len(x_values))
    y_values[0] = y0

    for i in range(len(x_values) - 1):
        y_values[i + 1] = y_values[i] + h * f(x_values[i], y_values[i])

    return x_values, y_values


def cumulative_error(y_num, y_exact):
    """
    Return the cumulative absolute error.
    """
    return np.cumsum(np.abs(y_num - y_exact))


def print_table(x_vals, y_num, y_exact=None):
    print("\nEuler Method Results")
    print("-" * 78)

    if y_exact is None:
        print(f"{'x':>10} {'Approx y':>20}")
        print("-" * 78)
        for x, y in zip(x_vals, y_num):
            print(f"{x:>10.4f} {y:>20.8f}")
    else:
        print(f"{'x':>10} {'Approx y':>20} {'Exact y':>20} {'Abs Error':>15}")
        print("-" * 78)
        for x, yn, ye in zip(x_vals, y_num, y_exact):
            err = abs(yn - ye)
            print(f"{x:>10.4f} {yn:>20.8f} {ye:>20.8f} {err:>15.8f}")


def plot_results(x_vals, y_num, y_exact=None, filename="ode_plot.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_num, marker='o', linewidth=1.5, markersize=4, label="Euler Approximation")

    if y_exact is not None:
        plt.plot(x_vals, y_exact, linewidth=2, label="Exact Solution")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Euler Method Approximation")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    print(f"\nPlot saved as: {filename}")
    plt.show()


def run_demo():
    """
    Demo problem:
        y' = y
        y(0) = 1
        exact solution: y = e^x
    """
    print("\nRunning built-in demo problem...")
    ode_text = "y"
    exact_text = "exp(x)"
    x0, y0, h, xn = 0.0, 1.0, 0.2, 1.0

    f, _ = parse_function(ode_text)
    exact_f, _ = parse_exact_solution(exact_text)

    x_vals, y_euler = euler_method(f, x0, y0, h, xn)
    y_exact = exact_f(x_vals)
    cum_err = cumulative_error(y_euler, y_exact)

    print_table(x_vals, y_euler, y_exact)

    print("\nCumulative Absolute Error")
    print("-" * 40)
    print(f"{'x':>10} {'Cum Error':>20}")
    print("-" * 40)
    for x, ce in zip(x_vals, cum_err):
        print(f"{x:>10.4f} {ce:>20.8f}")

    plot_results(x_vals, y_euler, y_exact, filename="demo_plot.png")


def interactive_mode():
    print("\nEuler Method ODE Solver")
    print("Solve y' = f(x, y) using Euler's Method.")
    print("Use Python-style math. Example: x + y, y - x**2, -2*y")
    print()

    ode_text = input("Enter f(x, y) for y' = f(x, y): ").strip()
    x0 = float(input("Enter x0: "))
    y0 = float(input("Enter y0: "))
    h = float(input("Enter step size h: "))
    xn = float(input("Enter final x value xn: "))

    exact_choice = input("Do you have an exact solution? (y/n): ").strip().lower()
    f, _ = parse_function(ode_text)

    x_vals, y_euler = euler_method(f, x0, y0, h, xn)

    if exact_choice == 'y':
        exact_text = input("Enter exact solution y(x): ").strip()
        exact_f, _ = parse_exact_solution(exact_text)
        y_exact = exact_f(x_vals)
        cum_err = cumulative_error(y_euler, y_exact)

        print_table(x_vals, y_euler, y_exact)

        print("\nCumulative Absolute Error")
        print("-" * 40)
        print(f"{'x':>10} {'Cum Error':>20}")
        print("-" * 40)
        for x, ce in zip(x_vals, cum_err):
            print(f"{x:>10.4f} {ce:>20.8f}")

        plot_results(x_vals, y_euler, y_exact, filename="user_plot.png")
    else:
        print_table(x_vals, y_euler)
        plot_results(x_vals, y_euler, None, filename="user_plot.png")


def main():
    print("MA303 Coding Project: Euler's Method Tool")
    print("1. Run built-in demo")
    print("2. Enter your own problem")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        run_demo()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
