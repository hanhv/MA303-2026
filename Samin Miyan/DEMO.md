# Demo: MA303 Laplace Transform Calculator

This file shows a short demo that can be included in the GitHub repository. It explains how to run the project and gives example inputs and expected outputs.

## 1. Install the required package

Run this in the terminal inside the project folder:

```bash
pip3 install -r requirements.txt
```

## 2. Run the built-in demo

```bash
python3 laplace_calculator.py demo
```

The demo runs three examples:

1. A Laplace transform of a polynomial, sine function, and exponential-shifted polynomial.
2. An inverse Laplace transform involving powers of \((s-3)\), trig forms, and rational functions.
3. A Laplace transform using the Heaviside step function.

## 3. Example 1: Laplace transform

Command:

```bash
python3 laplace_calculator.py laplace "5*t**3 - sin(t) + t**2*exp(-t)"
```

Mathematical input:

\[
f(t)=5t^3-\sin(t)+t^2e^{-t}
\]

Expected result:

\[
F(s)=\frac{30}{s^4}-\frac{1}{s^2+1}+\frac{2}{(s+1)^3}
\]

This uses the table formulas:

\[
\mathcal{L}\{t^n\}=\frac{n!}{s^{n+1}}, \quad
\mathcal{L}\{\sin(t)\}=\frac{1}{s^2+1}, \quad
\mathcal{L}\{e^{-t}t^2\}=\frac{2}{(s+1)^3}
\]

## 4. Example 2: Inverse Laplace transform

Command:

```bash
python3 laplace_calculator.py inverse "7/s**2 + 6/(s-3)**4 + (s+1)/(s**2+9)"
```

Mathematical input:

\[
F(s)=\frac{7}{s^2}+\frac{6}{(s-3)^4}+\frac{s+1}{s^2+9}
\]

Expected result:

\[
f(t)=7t+t^3e^{3t}+\cos(3t)+\frac{1}{3}\sin(3t)
\]

This uses:

\[
\mathcal{L}^{-1}\left\{\frac{1}{s^2}\right\}=t
\]

\[
\mathcal{L}^{-1}\left\{\frac{6}{(s-3)^4}\right\}=t^3e^{3t}
\]

\[
\mathcal{L}^{-1}\left\{\frac{s}{s^2+9}\right\}=\cos(3t), \quad
\mathcal{L}^{-1}\left\{\frac{1}{s^2+9}\right\}=\frac{1}{3}\sin(3t)
\]

## 5. Example 3: Step function

Command:

```bash
python3 laplace_calculator.py laplace "Heaviside(t-1)*(t-1)"
```

Mathematical input:

\[
f(t)=u(t-1)(t-1)
\]

Expected result:

\[
F(s)=\frac{e^{-s}}{s^2}
\]

This uses the second shifting theorem:

\[
\mathcal{L}\{u(t-a)g(t-a)\}=e^{-as}G(s)
\]

Here, \(a=1\), \(g(t)=t\), and \(G(s)=\frac{1}{s^2}\), so:

\[
\mathcal{L}\{u(t-1)(t-1)\}=e^{-s}\frac{1}{s^2}
\]

## 6. What this demo proves

This demo shows that the calculator can handle:

- basic Laplace transform table functions
- linear combinations of functions
- exponential shifting
- inverse Laplace transforms
- trig transform forms
- Heaviside step functions

That connects directly to MA303 topics involving Laplace transforms, inverse Laplace transforms, and solving differential equations with transform methods.
