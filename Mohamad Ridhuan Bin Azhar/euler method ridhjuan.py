"""
Euler's Method Calculator for MA 303
------------------------------------
Euler's Method formula:
    y_next = y_current + h * f(x_current, y_current)

Example input for f(x, y):
    x + y
    x - y
    y - x**2
    math.sin(x) + y
"""

import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def euler_method_calculator():
    print("=================================")
    print(" MA 303 Euler's Method Calculator")
    print("=================================")
    print("Approximates solutions to dy/dx = f(x, y).")
    print()
    print("Example functions:  x + y  |  x - y  |  y - x**2  |  math.sin(x) + y")
    print()

    # ---------- user input ----------
    function_input = input("Enter dy/dx = f(x, y): ").strip()
    x0    = float(input("Enter initial x value, x0: "))
    y0    = float(input("Enter initial y value, y0: "))
    h     = float(input("Enter step size h: "))
    x_end = float(input("Enter final x value: "))

    # ---------- step count ----------
    number_of_steps = int(round((x_end - x0) / h))

    print()
    print(f"  x0={x0}, y0={y0}, h={h}, x_end={x_end}, steps={number_of_steps}")

    if number_of_steps <= 0:
        print()
        print("ERROR: 0 steps computed.")
        print("Make sure x_end > x0 and h is smaller than (x_end - x0).")
        return

    # ---------- storage ----------
    x_values = [x0]
    y_values = [y0]
    table    = []

    current_x = x0
    current_y = y0

    eval_namespace = {"math": math, "__builtins__": {}}

    # ---------- Euler loop ----------
    for step in range(1, number_of_steps + 1):
        eval_namespace["x"] = current_x
        eval_namespace["y"] = current_y

        slope  = eval(function_input, eval_namespace)
        next_y = current_y + h * slope
        next_x = x0 + step * h          # avoids floating-point drift

        table.append([step, current_x, current_y, slope, next_x, next_y])
        x_values.append(next_x)
        y_values.append(next_y)

        current_x = next_x
        current_y = next_y

    # ---------- print ----------
    print()
    print("Differential equation: dy/dx =", function_input)
    print("Formula: y_next = y_current + h * f(x_current, y_current)")
    print()

    col_w = 14
    header = (
        f"{'Step':<6}"
        f"{'x_n':>{col_w}}"
        f"{'y_n':>{col_w}}"
        f"{'slope':>{col_w}}"
        f"{'x_next':>{col_w}}"
        f"{'y_next':>{col_w}}"
    )
    sep = "-" * len(header)

    print("Table of Values:")
    print(sep)
    print(header)
    print(sep)

    for row in table:
        s, xn, yn, sl, xnx, ynx = row
        print(
            f"{s:<6}"
            f"{round(xn,  5):>{col_w}}"
            f"{round(yn,  5):>{col_w}}"
            f"{round(sl,  5):>{col_w}}"
            f"{round(xnx, 5):>{col_w}}"
            f"{round(ynx, 5):>{col_w}}"
        )

    print(sep)
    print()
    print(f"Approximate final answer:  y({x_end}) ≈ {round(current_y, 8)}")

    # ---------- graph ----------
    graph_euler_method(x_values, y_values)


def graph_euler_method(x_values, y_values):
    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, marker="o", label="Euler Approximation")
    plt.title("Euler's Method Approximation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()

    script_dir  = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "euler_graph.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Graph saved to: {output_path}")


euler_method_calculator()