import math as m
eu = 0
imp = 0
rk = 0

def eulers():
    x = 0
    y = y0
    while (x < end):
        y += h*eval(yprime)
        x += h
    return y

def improved():
    x = 0
    y = y0
    while (x < end):
        k1 = eval(yprime)
        store = y
        y += h * k1
        x += h
        k2 = eval(yprime)
        y = store + h * 0.5 * (k1 + k2)

    return y

def rungekutta():
    x = 0
    y = y0
    while (x < end):
        k1 = eval(yprime)
        storex = x
        storey = y
        x += 0.5 * h
        y = storey + 0.5 * h * k1
        k2 = eval(yprime)
        y = storey + 0.5 * h * k2
        k3 = eval(yprime)
        x = storex + h
        y = storey + h * k3
        k4 = eval(yprime)
        y = storey + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y 

def error(calc, exp):
    n = ((calc - exp) / exp) * 100
    return n
    
print("Three Euler Method Solver:")
print("For equations, use x and y as variables and follow python math formatting (math is imported as m)")
actual = input("Enter the actual equation: ")
yprime = input("Enter y prime: ")
y0 = float(input("Enter y0: "))
h = float(input("Enter step size: "))
end = float(input("Enter end of range: "))


print("")
eu = eulers()
print(f"The Euler's approximation of this function = {eu:.5f}")
imp = improved()
print(f"The Improved Euler's approximation of this function = {imp:.5f}")
rk = rungekutta()
print(f"The Runge-Kutta method approximation of this function = {rk:.5f}")
x = end
calc = eval(actual)
print(f"The actual value of the function = {calc:.5f}")

#Percent Errors
print("")
p_error = error(eu, calc)
print(f"Error for Euler: {p_error:.5f}%")
p_error = error(imp, calc)
print(f"Error for Improved Euler: {p_error:.5f}%")
p_error = error(rk, calc)
print(f"Error for Runge-Kutta method: {p_error:.5f}%")
print("")
input("Press enter to exit.")