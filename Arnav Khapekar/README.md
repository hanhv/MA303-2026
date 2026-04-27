# MA303 Project: Autonomous System Phase Portrait Analyzer

## Project Overview
This project is a Python-based computational tool designed to analyze and visualize the stability of 2D autonomous systems of linear differential equations. The tool handles systems of the form:
$\dot{x} = ax + by$  
$\dot{y} = cx + dy$

## The Math
The core of this tool is based on the **Stability Theorem for Linear Systems**. 

### 1. Eigenvalue Calculation
The tool solves the characteristic equation:
$$\det(A - \lambda I) = 0 \implies \lambda^2 - Tr(A)\lambda + \det(A) = 0$$
where $Tr(A)$ is the trace and $\det(A)$ is the determinant of the system matrix.

### 2. Stability Classification
Using the **Discriminant** $\Delta = Tr(A)^2 - 4\det(A)$, the tool automatically classifies the equilibrium point at the origin:
* **Saddle Point:** $\det(A) < 0$
* **Spiral Sink/Source:** $\det(A) > 0$ and $\Delta < 0$
* **Node Sink/Source:** $\det(A) > 0$ and $\Delta > 0$

### 3. Nullclines
The tool overlays nullclines (where $\dot{x}=0$ or $\dot{y}=0$) to show where the flow of the system changes direction.

## 🛠 Technical Implementation
* **Language:** Python 3
* **Libraries:** NumPy (Matrix algebra) and Matplotlib (Streamplot visualization)
* **Visuals:** I used the `streamplot` function because it uses numerical integration to accurately trace the trajectories, providing a much higher-quality visual than standard vector arrows.

* ## Comprehensive Testing Suite

The tool was validated against every major stability classification in the MA303 curriculum. By calculating the Trace ($T$), Determinant ($D$), and Discriminant ($\Delta = T^2 - 4D$), the program accurately identifies and plots the following cases:

### 1. Test Case Matrix
| Stability Type | a, b | c, d | Eigenvalues | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Stable Node** | -3, 0 | 0, -1 | $-3, -1$ | Flow drains directly in. |
| **Unstable Node** | 3, 0 | 0, 1 | $3, 1$ | Flow pushes directly out. |
| **Stable Spiral** | -1, -2 | 2, -1 | $-1 \pm 2i$ | Inward swirling motion. |
| **Unstable Spiral** | 1, 2 | -2, 1 | $1 \pm 2i$ | Outward swirling motion. |
| **Saddle Point** | 1, 1 | 4, -2 | $2, -3$ | Attracted then repelled. |
| **Center** | 0, 2 | -2, 0 | $0 \pm 2i$ | Perfect orbital loops. |

---

### 2. Visual Gallery

#### Nodes (Real Eigenvalues)
| Stable Node | Unstable Node |
| :---: | :---: |
| ![Stable Node](stable_node.png) | ![Unstable Node](unstable_node.png) |

#### Spirals (Complex Eigenvalues)
| Stable Spiral | Unstable Spiral |
| :---: | :---: |
| ![Stable Spiral](stable_spiral.png) | ![Unstable Spiral](unstable_spiral.png) |

#### Critical Cases
| Saddle Point | Center |
| :---: | :---: |
| ![Saddle Point](saddle_point.png) | ![Center](center.png) |

---

## Math Summary
The tool maps these cases onto the **Poincaré Stability Diagram**. 
* **$D < 0$**: Saddle Point
* **$D > 0, \Delta > 0$**: Nodes (Sink if $T < 0$, Source if $T > 0$)
* **$D > 0, \Delta < 0$**: Spirals (Sink if $T < 0$, Source if $T > 0$)
* **$T = 0, D > 0$**: Center
