# SpringMassSimulator_PartialDifferentialEquations


An interactive browser-based simulator for the spring-mass-damper system — one of the most fundamental models in mechanical engineering. The tool visualizes the system's behavior in real time: phase portraits, displacement over time, and steady-state frequency response under sinusoidal forcing. All of it updates live as parameters change.

The connection to MA303 is direct. The governing equation is a second-order linear ODE, and the simulator lets you see — not just compute — what damping ratio, natural frequency, and resonance actually mean physically.

Open `index.html` in any browser. No installation required.

---

## Background and Motivation

The spring-mass-damper system shows up constantly in mechanical engineering — vehicle suspension, structural dynamics, vibration isolation, control systems. The math behind it is exactly what MA303 covers: second-order linear ODEs, characteristic equations, and forced response. Building this simulator was a way to connect the coursework to something concrete and to develop a better intuition for how the parameters interact.

---

## The Mathematics

### Governing Equation

Applying Newton's second law to a mass m on a spring (k) with a damper (c) and external forcing F(t):

$$m\ddot{y} + c\dot{y} + ky = F(t)$$

Dividing through by m gives the standard form:

$$\ddot{y} + 2\zeta\omega_n\dot{y} + \omega_n^2 y = \frac{F(t)}{m}$$

Two parameters govern the behavior entirely:

- **Natural frequency:** $\omega_n = \sqrt{k/m}$ — the frequency at which the system oscillates freely
- **Damping ratio:** $\zeta = c / (2\sqrt{mk})$ — how quickly oscillations decay

---

### Free Vibration (F = 0)

Substituting $y = e^{st}$ gives the characteristic equation:

$$ms^2 + cs + k = 0 \implies s = -\zeta\omega_n \pm \omega_n\sqrt{\zeta^2 - 1}$$

Three cases depending on zeta:

**Underdamped (zeta < 1):** Complex roots; the system oscillates with decaying amplitude.

$$y(t) = e^{-\zeta\omega_n t}\left(A\cos(\omega_d t) + B\sin(\omega_d t)\right), \quad \omega_d = \omega_n\sqrt{1-\zeta^2}$$

**Critically damped (zeta = 1):** Repeated real root; fastest return to equilibrium without oscillation.

$$y(t) = (A + Bt)e^{-\omega_n t}$$

**Overdamped (zeta > 1):** Two distinct negative real roots; slow, non-oscillatory decay.

$$y(t) = Ae^{s_1 t} + Be^{s_2 t}$$

On the phase portrait (y, y-dot), these three regimes look visually distinct — an inward spiral, a curved path into the origin, and a slow creep along the dominant eigenvector, respectively.

---

### Forced Vibration and Resonance

With F(t) = F0*cos(omega*t), the particular solution in steady state is:

$$y_p(t) = |Y|\cos(\omega t - \phi)$$

where the amplitude is:

$$|Y| = \frac{F_0/k}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}, \quad r = \frac{\omega}{\omega_n}$$

As r approaches 1 (driving frequency approaches natural frequency), the denominator shrinks and the amplitude grows sharply — this is **resonance**. For small zeta, the amplitude peak can be many times the static deflection F0/k. This is why resonance is a central design concern in any vibrating mechanical system.

---

### Numerical Integration

The ODE is rewritten as a first-order system and integrated using **fourth-order Runge-Kutta (RK4)**:

$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

with step size h = 0.008 s. RK4 achieves global error O(h^4), which is sufficient for smooth real-time animation.

---

### Phase Portraits

The phase portrait plots y-dot against y, tracing the system's path through state space — no time axis, just the relationship between position and velocity. The shape of the trajectory immediately identifies the damping regime:

| Regime | Phase portrait |
|---|---|
| Underdamped | Inward spiral (stable focus) |
| Critically damped | Curved path directly into origin |
| Overdamped | Slow approach along dominant eigenvector |
| Undamped | Closed ellipse (energy conserved) |

---

## Features

| Tab | What it shows |
|---|---|
| Motion & Phase | Animated mass on spring, live phase portrait, displacement time series |
| Forced Vibration | Frequency response curve, resonance peak, current operating point |
| The Math | Exact characteristic roots and solution form for current parameter values |

All sliders (m, c, k, y0, F0, omega) update every panel in real time.

---

## Usage

1. Open `index.html` in any modern browser
2. Adjust m, c, k — watch the damping regime badge and phase portrait change
3. Drag c from low to high to move through underdamped → critically damped → overdamped
4. Switch to **Forced Vibration**, set F0 > 0, and sweep omega slowly toward omega_n to see resonance build
5. Check **The Math** tab for the exact solution at any parameter combination

---

## Files

```
/
├── index.html    — full simulator, self-contained
└── README.md     — this file
```

No build step, no dependencies, no frameworks.

---

## Physical Context

| Parameter | Physical meaning |
|---|---|
| m | Mass of object (kg) |
| k | Spring stiffness (N/m) |
| c | Damping coefficient (N·s/m) |
| zeta | Damping ratio (dimensionless) |
| omega_n | Natural frequency (rad/s) |
| omega | Driving frequency (rad/s) |

Car suspensions are typically tuned to zeta ~ 0.3–0.5 — underdamped enough to respond quickly, damped enough not to bounce repeatedly. Setting zeta = 1 in the simulator shows what critically damped looks like: the fastest possible return to rest with no overshoot.

---

## References
- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*
- Rao, S.S., *Mechanical Vibrations*
- MA303 Course Notes

