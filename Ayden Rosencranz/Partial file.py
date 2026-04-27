
###
#"""
#
# Hello and welcome to my MA303 Project!

# For this project I chose to make a program that approximates solutions of differential equations using Euler’s method, the Improved Euler method, or the Runge–Kutta method.

# This will serve as the intorduction to my program and the beging of my demo Video. For the demo introduction I will scroll through the code then show it in opperation.

# -Ayden M. Rosencranz

#"""
####








### This code here is part of my first few itterations and the class examples that I used to model my code off of from the home work ###
# import numpy as np
# import ast
# import operator as op
# import math
# program=input("Please Choose A Program (1-3)")

# if program == "1":
#     x0 = float(input("Input x0: "))
#     y0 = float(input("Input y0: "))
#     # ---------- First run (h = 0.01) ----------
#     h1 = float(input("Input Step: "))
#     x = x0
#     y = y0
#     y1 = [y0]          # initialize list
#     for n in range(100):
#         y = y + h1*(y - 2)
#         y1.append(y)
#         x += h1
#     # ---------- Second run (h = 0.005) ----------
#     h2 = 0.005
#     x = x0
#     y = y0
#     y2 = [y0]
#     for n in range(200):
#         y = y + h2*(y - 2)
#         y2.append(y)
#         x += h2
#     # ---------- Exact values ----------
#     x_exact = np.arange(x0, x0 + 1.0001, 0.2)
#     ye = 2 - np.exp(x_exact)
#     # ---------- Sample matching points ----------
#     # For h=0.005, every 40th value corresponds to 0.2 spacing
#     ya = np.array(y2[::40])       # 0, 40, 80, ...
#     # For h=0.01, every 20th value corresponds to 0.2 spacing
#     y1_sample = np.array(y1[::20])
#     # ---------- Percent error ----------
#     err = 100 * (ye - ya) / ye
#     # ---------- Display table ----------
#     table = np.vstack((x_exact, y1_sample, ya, ye, err))
#     print(table)
# elif program == "2":
#     x0 = float(input("Input x0: "))
#     y0=int(input("Input y0: "))
#     #First Run
#     h1 = float(input("Input Step: "))
#     x = x0
#     y = y0
#     y1 = [y0]
#     for n in range(100):
#         u = y + h1*("f(x,y)")
#         y1.append(y)
#         x += h1

# yp = function(x,y)
# y-2
#^#^#^^^#^#^# (Old Itterations) #^#^#^^^#^#^#\

### Import Sections ###
import numpy as np
import operator as op
import math
import re
 
### Get inputed function Section ###
def get_user_function():
    #Gets the user's function expression once and returns a callable allowing their inputs to be used in calculations.
    #Print statments and user propts
    print("\nEnter your function in terms of x and y")
    print("Examples: y-2  or  x**2+y**2-3*x*y+5  or  sin(x)*y")
    print("Use * for multiplication, ** for powers")
    expr = input("f(x,y) = ")
 
    #This expression changes standard notations into python readable code.
    expr = expr.replace('^', '**')
 
    # Auto-insert * for implicit multiplication so users can type natural math notation.
    # Handles cases like: 0.8x -> 0.8*x, 2y -> 2*y, 3x**2 -> 3*x**2, 2(x+y) -> 2*(x+y)
    expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
    # Also handles cases like x( or y( -> x*( for expressions like sin(x)y
    expr = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr)
    # Undo any damage done to function names like sin*(x) -> sin(x)
    for fn in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs', 'pow']:
        expr = expr.replace(f'{fn}*(', f'{fn}(')
    
    def evaluate(x, y):
        # Create namespace with math functions and current x, y values
        namespace = {
            'x': x, 'y': y,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e,
            'abs': abs, 'pow': pow,
            '__builtins__': {}
        }
        try:
            return eval(expr, namespace)
        except Exception as e:
            print(f"Error evaluating function: {e}")
            return 0
    
    return evaluate
 
### Method for solving section ###
# depending on the method name one of these fucntions will be used to solve for the related type of problem.
def run_method(method_name, method_func, x0, y0, h, f, num_steps):
 
    #Run a numerical method and return results.
    x = x0
    y = y0
    results = {round(x0, 10): y0}
    
    for n in range(num_steps):
        y = method_func(f, x, y, h) #runs the named using method_func as a varriable name to avoid the use of if/or staments.
        x = x0 + (n + 1) * h  # Calculate x directly to avoid accumulation errors
        results[round(x, 10)] = y
    
    return results
 
def euler_step(f, x, y, h):
    #Single step of Euler's method
    return y + h * f(x, y)
 
def improved_euler_step(f, x, y, h):
    #Single step of Improved Euler's method
    k1 = f(x, y)
    u = y + h * k1
    k2 = f(x + h, u)
    return y + h * (k1 + k2) / 2
 
def rk4_step(f, x, y, h):
    #Single step of Runge-Kutta method
    k1 = f(x, y)
    k2 = f(x + h/2, y + h*k1/2)
    k3 = f(x + h/2, y + h*k2/2)
    k4 = f(x + h, y + h*k3)
    return y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
 
#manual input/had coded section: requires coding from user: to input the actuall solution if given
def get_actual_solution(x_val):
    # Optional: provide the known analytical solution for error comparison.
    # If no exact solution is known, return None and error column will be skipped.
    # Change this function body to match your ODE's actual solution, or return None to disable.
    try:
        return 3 + x_val - 2*math.exp(x_val)  # <-- update this for your specific ODE, or return None
    except:
        return None
 
def find_closest_y(results, x_val, h):
    # Finds the closest stored result to a given x value within one step size tolerance.
    closest_key = min(results.keys(), key=lambda k: abs(k - x_val))
    if abs(closest_key - x_val) <= h / 2 + 0.0001:
        return results[closest_key]
    return None  # outside acceptable range, mark as missing in the table
 
### Main Program Section ###
#run programs, AND OPTION MENUE OUTPUTS
print("=" * 50)
print("DIFFERENTIAL EQUATION SOLVER")
print("=" * 50)
print("1 - Euler's Method")
print("2 - Improved Euler's Method (Heun's Method)")
print("3 - Runge-Kutta Method (RK4)")
print("=" * 50)
#USER INPUT TO DETERMIN METHOD
program = input("Please Choose A Program (1-3): ")
 
if program in ["1", "2", "3"]:
    #WHERE user input to determin method of solving IS APPLIED for our code, intial values GATHERED, and step size GATHERED, AND where the more accurate step size is gathered.
    print(f"\n--- METHOD SELECTED ---")
    x0 = float(input("Input x0: "))
    y0 = float(input("Input y0: "))
    h1 = float(input("Input first step size h1: "))
    h2 = float(input("Input second step size h2 (smaller for more accuracy): "))
 
    # Allow user to define a custom target range instead of hardcoding 1.0
    target_range = float(input("Input target range (e.g. 1.0 to go from x0 to x0+1): "))
 
    # Allow user to define the display increment instead of hardcoding 0.2
    display_step = float(input("Input display increment (e.g. 0.2 to show results every 0.2): "))
 
    # Determine which is more accurate (smaller step)
    h_accurate = min(h1, h2)
    h_coarse = max(h1, h2)
    
    # Calculate number of steps to reach x = x0 + target_range
    # Using round to avoid floating point edge cases cutting off the last step
    num_steps_h1 = round(target_range / h1)
    num_steps_h2 = round(target_range / h2)
 
    f = get_user_function()
    
    # Select method via if and elif staments from the earlier user input.
    if program == "1":
        method_name = "EULER'S METHOD"
        method_func = euler_step
    elif program == "2":
        method_name = "IMPROVED EULER'S METHOD"
        method_func = improved_euler_step
    else:
        method_name = "RUNGE-KUTTA METHOD (RK4)"
        method_func = rk4_step
    
    print(f"\n--- {method_name} ---")
    print(f"Running with h1={h1} and h2={h2}")
    
    # Run both calculations
    results_h1 = run_method(method_name, method_func, x0, y0, h1, f, num_steps_h1)
    results_h2 = run_method(method_name, method_func, x0, y0, h2, f, num_steps_h2)
    
    # Generate x values at user-defined display increments across the target range
    x_values = []
    x = x0
    while x <= x0 + target_range + 0.0001:
        x_values.append(round(x, 10))
        x += display_step
 
    # Check whether an actual solution is available to decide table layout
    has_actual = get_actual_solution(x0) is not None
 
    #table of ouputs
    print(f"\n--- RESULTS AT x = MULTIPLES OF {display_step} ---")
    if has_actual:
        print(f"{'x':<12} {f'y(h1={h1})':<15} {f'y(h2={h2})':<15} {'y(actual)':<15} {'% Error':<12}")
    else:
        print(f"{'x':<12} {f'y(h1={h1})':<15} {f'y(h2={h2})':<15}")
    print("-" * 75)
    
    for x_val in x_values:
        #makes sure values stay within tolerance
        y_h1 = find_closest_y(results_h1, x_val, h1)
        y_h2 = find_closest_y(results_h2, x_val, h2)
 
        # If BOTH results are missing for this x value, skip the row entirely.
        # If only one is missing (e.g. coarse h1 doesn't land here), show '---' for that column
        # so rows driven by the finer h2 still appear.
        if y_h1 is None and y_h2 is None:
            continue
 
        # Format each column — use '---' placeholder when a step size misses this x value
        col_h1 = f"{y_h1:<15.6f}" if y_h1 is not None else f"{'---':<15}"
        col_h2 = f"{y_h2:<15.6f}" if y_h2 is not None else f"{'---':<15}"
 
        if has_actual:
            y_actual = get_actual_solution(x_val)
 
            # Use more accurate approximation (smaller h) for error calculation
            #PRECENT ERROR CALCULATIONS
            y_accurate = y_h2 if h2 < h1 else y_h1
            if y_accurate is not None and y_actual != 0:
                percent_error = 100 * (y_actual - y_accurate) / y_actual
                col_err = f"{percent_error:<12.6f}"
            else:
                col_err = f"{'---':<12}"
 
            print(f"{x_val:<12.6f} {col_h1} {col_h2} {y_actual:<15.6f} {col_err}")
        else:
            # No actual solution provided — print approximations only
            print(f"{x_val:<12.6f} {col_h1} {col_h2}")
    
    print(f"\nNote: % Error calculated using more accurate approximation (h={h_accurate})")
 
else:
    #FAIL OUTPUT OPTION
    print("Invalid program selection. Please choose 1, 2, or 3.")



    # please note that to use a exact solution you must add that by hard coding it to the actual solution function.