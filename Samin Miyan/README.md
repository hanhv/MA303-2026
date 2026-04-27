# MA303 Laplace Transform Calculator

## Project overview
This project is a Python tool that computes **Laplace transforms** and **inverse Laplace transforms** for many standard symbolic expressions from differential equations. It was made for an MA303 coding project.

The calculator allows a user to:
- enter a function of `t` and compute its Laplace transform `F(s)`
- enter an expression of `s` and compute its inverse Laplace transform `f(t)`
- test the tool on built-in examples commonly seen in class

This project focuses on the mathematics behind Laplace transforms and shows how symbolic computation can help solve problems from differential equations.

## Why I chose this project
Laplace transforms are one of the main techniques used in MA303 to solve initial value problems, handle piecewise functions, and work with step functions and impulses. I chose this project because it connects directly to the course and is both mathematically meaningful and practical.

## Mathematics behind the project
The Laplace transform of a function `f(t)` is

\[
\mathcal{L}\{f(t)\} = F(s) = \int_0^{\infty} e^{-st} f(t)\,dt
\]

It converts a function of time `t` into a function of `s`. This is useful because differential equations in `t` can often be turned into algebraic equations in `s`.

The inverse Laplace transform reverses this process:

\[
\mathcal{L}^{-1}\{F(s)\} = f(t)
\]

This project can handle many standard forms from class, including:
- polynomials like `t^n`
- exponentials like `e^(at)`
- trigonometric functions like `sin(bt)` and `cos(bt)`
- hyperbolic functions
- shifted functions involving `Heaviside(t-a)`
- rational expressions whose inverse transforms are standard or can be simplified symbolically

## Files in this repository
- `laplace_calculator.py` — main Python program
- `requirements.txt` — dependency list
- `README.md` — explanation of the project, mathematics, and usage

## Installation
Clone the repository and install the dependency:

```bash
pip install -r requirements.txt
```

## How to run
### 1. Compute a Laplace transform
```bash
python laplace_calculator.py laplace "5*t**3 - sin(t) + t**2*exp(-t)"
```

### 2. Compute an inverse Laplace transform
```bash
python laplace_calculator.py inverse "7/s**2 + 6/(s-3)**4 + (s+1)/(s**2+9)"
```

### 3. Run the built-in demo
```bash
python laplace_calculator.py demo
```

## Example results
### Example 1: Laplace transform
Input:

\[
f(t)=5t^3-\sin t+t^2e^{-t}
\]

Output:

\[
F(s)=\frac{30}{s^4}-\frac{1}{s^2+1}+\frac{2}{(s+1)^3}
\]

### Example 2: Inverse Laplace transform
Input:

\[
F(s)=\frac{7}{s^2}+\frac{6}{(s-3)^4}+\frac{s+1}{s^2+9}
\]

Output:

\[
f(t)=7t+t^3 e^{3t}+\cos(3t)+\frac{1}{3}\sin(3t)
\]

## How I tested the tool
I tested the calculator on several standard transform pairs from the Laplace transform table used in differential equations, including:
- `t^n`
- `e^{-t}`
- `sin(t)` and `cos(t)`
- combinations of multiple terms
- shifted functions using the step function `Heaviside`
- inverse transforms of rational functions

For each test, I compared the output with known Laplace transform formulas from class.

## Limitations
This tool does **not** guarantee a result for every possible symbolic expression. It works best on standard expressions typically covered in MA303. Very complicated expressions may fail or return results in a different but equivalent symbolic form.

## Why this is a meaningful MA303 project
This project is not just a calculator. It demonstrates understanding of:
- what a Laplace transform is
- why inverse Laplace transforms matter
- how transform tables are used in practice
- how symbolic computation connects to the differential equations methods learned in class

It also shows actual implementation, testing, and mathematical explanation, which makes it appropriate for a coding project and class presentation.

## Demo File

A separate demo walkthrough is included in `DEMO.md`. It gives commands, mathematical inputs, expected outputs, and explanations of the Laplace transform rules used.
