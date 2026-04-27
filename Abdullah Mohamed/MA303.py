"""
MA303 Interactive Math Dashboard
==================================
Covers: Phase Portraits, ODE Numerical Methods, Laplace Transforms
Run with: python ma303_dashboard.py
Requires: pip install numpy matplotlib scipy
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import odeint
import warnings
warnings.filterwarnings("ignore")

# ─── Color Palette ───────────────────────────────────────────────────────────
BG       = "#0a0e1a"
PANEL    = "#111827"
ACCENT1  = "#00d4ff"
ACCENT2  = "#7c3aed"
ACCENT3  = "#f97316"
TEXT     = "#e2e8f0"
SUBTEXT  = "#94a3b8"
BORDER   = "#1e293b"
ENTRY_BG = "#1e293b"
BTN_HOV  = "#2563eb"
SUCCESS  = "#10b981"
ERROR    = "#ef4444"

FONT_HEAD  = ("Courier New", 13, "bold")
FONT_LABEL = ("Courier New", 10)
FONT_SMALL = ("Courier New", 9)
FONT_MONO  = ("Courier New", 10)

def styled_frame(parent, **kw):
    return tk.Frame(parent, bg=PANEL, relief="flat", **kw)

def styled_label(parent, text, font=FONT_LABEL, color=TEXT, **kw):
    return tk.Label(parent, text=text, font=font, fg=color, bg=PANEL, **kw)

def styled_entry(parent, width=12, **kw):
    return tk.Entry(parent, width=width, font=FONT_MONO,
                    bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT1,
                    relief="flat", bd=4, **kw)

def styled_button(parent, text, command, color="#1d4ed8", **kw):
    return tk.Button(parent, text=text, command=command,
                     font=("Courier New", 10, "bold"),
                     bg=color, fg="white", activebackground=BTN_HOV,
                     activeforeground="white", relief="flat", bd=0,
                     padx=14, pady=7, cursor="hand2", **kw)

def section_header(parent, text, accent=ACCENT1):
    f = tk.Frame(parent, bg=PANEL)
    tk.Label(f, text="▸ " + text, font=FONT_HEAD, fg=accent, bg=PANEL).pack(side="left")
    tk.Frame(f, bg=accent, height=2, width=200).pack(side="left", padx=8, pady=6)
    return f

def apply_dark_theme(fig, ax_list):
    fig.patch.set_facecolor("#0d1117")
    for ax in ax_list:
        ax.set_facecolor("#0d1117")
        ax.tick_params(colors=SUBTEXT, labelsize=8)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(ACCENT1)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)

def preset_btn(parent, name, callback):
    tk.Button(parent, text=name, command=callback,
              font=FONT_SMALL, bg=ENTRY_BG, fg=SUBTEXT,
              activebackground=BORDER, activeforeground=TEXT,
              relief="flat", bd=0, padx=8, pady=4,
              cursor="hand2", anchor="w").pack(fill="x", pady=1)


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — PHASE PORTRAIT
# ════════════════════════════════════════════════════════════════════════════
class PhasePortraitTab:
    def __init__(self, parent):
        self.frame = styled_frame(parent)
        self.build()

    def build(self):
        f = self.frame
        ctrl = styled_frame(f)
        ctrl.pack(side="left", fill="y", padx=16, pady=16)

        section_header(ctrl, "PHASE PORTRAIT", ACCENT1).pack(anchor="w", pady=(0,12))
        styled_label(ctrl, "System:  x' = ax + by", color=ACCENT1).pack(anchor="w")
        styled_label(ctrl, "         y' = cx + dy", color=ACCENT1).pack(anchor="w", pady=(0,12))

        mat = tk.Frame(ctrl, bg=PANEL); mat.pack(anchor="w", pady=4)
        tk.Label(mat, text="A = [", font=FONT_MONO, fg=SUBTEXT, bg=PANEL).grid(row=0, rowspan=2, column=0, padx=(0,4))
        for col, (lbl, val, attr) in enumerate([("a:", "1", "ea"), ("b:", "-2", "eb")]):
            tk.Label(mat, text=lbl, font=FONT_SMALL, fg=SUBTEXT, bg=PANEL).grid(row=0, column=1+col*2, sticky="e")
            e = styled_entry(mat, width=6); e.grid(row=0, column=2+col*2, padx=3, pady=2)
            e.insert(0, val); setattr(self, attr, e)
        for col, (lbl, val, attr) in enumerate([("c:", "1", "ec"), ("d:", "-1", "ed")]):
            tk.Label(mat, text=lbl, font=FONT_SMALL, fg=SUBTEXT, bg=PANEL).grid(row=1, column=1+col*2, sticky="e")
            e = styled_entry(mat, width=6); e.grid(row=1, column=2+col*2, padx=3, pady=2)
            e.insert(0, val); setattr(self, attr, e)
        tk.Label(mat, text="]", font=FONT_MONO, fg=SUBTEXT, bg=PANEL).grid(row=0, rowspan=2, column=5, padx=(4,0))

        r_frame = tk.Frame(ctrl, bg=PANEL); r_frame.pack(anchor="w", pady=8)
        tk.Label(r_frame, text="Plot range: ±", font=FONT_SMALL, fg=SUBTEXT, bg=PANEL).pack(side="left")
        self.e_range = styled_entry(r_frame, width=5); self.e_range.pack(side="left")
        self.e_range.insert(0, "4")

        n_frame = tk.Frame(ctrl, bg=PANEL); n_frame.pack(anchor="w", pady=4)
        tk.Label(n_frame, text="# Trajectories:", font=FONT_SMALL, fg=SUBTEXT, bg=PANEL).pack(side="left")
        self.e_traj = styled_entry(n_frame, width=5); self.e_traj.pack(side="left")
        self.e_traj.insert(0, "14")

        styled_button(ctrl, "▶  PLOT PHASE PORTRAIT", self.plot, color=ACCENT2).pack(pady=12, fill="x")

        self.info_var = tk.StringVar(value="Enter matrix and click Plot.")
        tk.Label(ctrl, textvariable=self.info_var, font=FONT_SMALL,
                 fg=ACCENT3, bg="#0f172a", justify="left",
                 wraplength=240, padx=8, pady=8).pack(fill="x", pady=4)

        section_header(ctrl, "PRESETS", ACCENT3).pack(anchor="w", pady=(16,6))
        presets = [
            ("Saddle Point",    "1", "-2", "1", "-1"),
            ("Stable Spiral",   "-1", "-2", "1", "-1"),
            ("Center",          "0", "-3", "3", "0"),
            ("Unstable Node",   "2", "1", "0", "3"),
            ("Stable Node",     "-2", "0", "1", "-3"),
            ("Repeated λ",      "-2", "1", "0", "-2"),
        ]
        for name, a, b, c, d in presets:
            def make_cb(a=a, b=b, c=c, d=d):
                def cb():
                    for e, v in [(self.ea, a), (self.eb, b), (self.ec, c), (self.ed, d)]:
                        e.delete(0, "end"); e.insert(0, v)
                    self.plot()
                return cb
            preset_btn(ctrl, name, make_cb())

        plot_frame = styled_frame(f)
        plot_frame.pack(side="left", fill="both", expand=True, padx=(0,16), pady=16)
        self.fig = Figure(figsize=(6.5, 6), dpi=100)
        self.ax  = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.plot()

    def plot(self):
        try:
            a = float(self.ea.get()); b = float(self.eb.get())
            c = float(self.ec.get()); d = float(self.ed.get())
            R = float(self.e_range.get())
            n_traj = int(self.e_traj.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid numbers."); return

        A = np.array([[a, b], [c, d]])
        eigvals, eigvecs = np.linalg.eig(A)
        tr = a + d; det = a*d - b*c

        if det < 0:
            kind, color = "Saddle Point", ACCENT3
        elif abs(np.imag(eigvals[0])) > 1e-8:
            if abs(np.real(eigvals[0])) < 1e-8:
                kind, color = "Center", ACCENT1
            elif np.real(eigvals[0]) < 0:
                kind, color = "Stable Spiral", SUCCESS
            else:
                kind, color = "Unstable Spiral", ERROR
        elif np.real(eigvals[0]) < 0 and np.real(eigvals[1]) < 0:
            kind, color = "Stable Node", SUCCESS
        elif np.real(eigvals[0]) > 0 and np.real(eigvals[1]) > 0:
            kind, color = "Unstable Node", ERROR
        else:
            kind, color = "Saddle Point", ACCENT3

        def fmt(z):
            r, i = np.real(z), np.imag(z)
            return f"{r:.3f}" if abs(i) < 1e-9 else f"{r:.3f} {'+' if i >= 0 else '-'} {abs(i):.3f}i"

        self.info_var.set(
            f"Classification: {kind}\n"
            f"λ₁ = {fmt(eigvals[0])}\n"
            f"λ₂ = {fmt(eigvals[1])}\n"
            f"tr(A) = {tr:.3f}   det(A) = {det:.3f}"
        )

        self.ax.clear()
        apply_dark_theme(self.fig, [self.ax])

        x = np.linspace(-R, R, 22); y = np.linspace(-R, R, 22)
        X, Y = np.meshgrid(x, y)
        U = a*X + b*Y; V = c*X + d*Y
        speed = np.sqrt(U**2 + V**2); speed[speed == 0] = 1e-10
        self.ax.streamplot(X, Y, U/speed, V/speed,
                           color=speed, cmap="cool", linewidth=0.8,
                           density=1.1, arrowsize=1.2)

        t = np.linspace(0, 12, 800)
        for ang in np.linspace(0, 2*np.pi, n_traj, endpoint=False):
            x0, y0 = R*0.7*np.cos(ang), R*0.7*np.sin(ang)
            sol = odeint(lambda s, t, A=A: A @ s, [x0, y0], t)
            xs, ys = sol[:, 0], sol[:, 1]
            mask = (np.abs(xs) < R*1.5) & (np.abs(ys) < R*1.5)
            self.ax.plot(xs[mask], ys[mask], color=color, alpha=0.65, linewidth=1.2)

        for ev in eigvecs.T:
            if abs(np.imag(ev[0])) < 1e-8:
                ev = np.real(ev)
                for sign in [1, -1]:
                    self.ax.annotate("", xy=(sign*ev[0]*R*0.9, sign*ev[1]*R*0.9),
                                     xytext=(0, 0),
                                     arrowprops=dict(arrowstyle="->", color=ACCENT3,
                                                     lw=2, mutation_scale=15))

        self.ax.axhline(0, color=BORDER, lw=0.8)
        self.ax.axvline(0, color=BORDER, lw=0.8)
        self.ax.plot(0, 0, 'o', color=ACCENT1, markersize=7, zorder=5)
        self.ax.set_xlim(-R, R); self.ax.set_ylim(-R, R)
        self.ax.set_xlabel("x"); self.ax.set_ylabel("y")
        self.ax.set_title(f"Phase Portrait — {kind}", fontsize=11)
        self.ax.set_aspect("equal")
        self.fig.tight_layout()
        self.canvas.draw()


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — NUMERICAL ODE SOLVER
# ════════════════════════════════════════════════════════════════════════════
class NumericalSolverTab:
    def __init__(self, parent):
        self.frame = styled_frame(parent)
        self.build()

    def build(self):
        f = self.frame
        ctrl = styled_frame(f); ctrl.pack(side="left", fill="y", padx=16, pady=16)

        section_header(ctrl, "NUMERICAL ODE SOLVER", ACCENT1).pack(anchor="w", pady=(0,12))
        styled_label(ctrl, "Solve:  y' = f(t, y)", color=ACCENT1).pack(anchor="w")

        for lbl, attr, default, w in [
            ("f(t,y) =",     "e_f",     "-2*y + t",                      18),
            ("y_exact(t) =", "e_exact", "t/2 - 1/4 + (5/4)*exp(-2*t)",  18),
        ]:
            row = tk.Frame(ctrl, bg=PANEL); row.pack(anchor="w", pady=4)
            tk.Label(row, text=lbl, font=FONT_MONO, fg=SUBTEXT, bg=PANEL).pack(side="left")
            e = styled_entry(row, width=w); e.pack(side="left", padx=6)
            e.insert(0, default); setattr(self, attr, e)
        styled_label(ctrl, "  (leave blank if unknown)", FONT_SMALL, SUBTEXT).pack(anchor="w")

        row3 = tk.Frame(ctrl, bg=PANEL); row3.pack(anchor="w", pady=6)
        for lbl, attr, val in [("t₀=","e_t0","0"), ("y₀=","e_y0","1"), ("t_end=","e_tend","3")]:
            tk.Label(row3, text=lbl, font=FONT_MONO, fg=SUBTEXT, bg=PANEL).pack(side="left", padx=(6,0))
            e = styled_entry(row3, width=5); e.pack(side="left", padx=2)
            e.insert(0, val); setattr(self, attr, e)

        row4 = tk.Frame(ctrl, bg=PANEL); row4.pack(anchor="w", pady=4)
        tk.Label(row4, text="Step h =", font=FONT_MONO, fg=SUBTEXT, bg=PANEL).pack(side="left")
        self.e_h = styled_entry(row4, width=7); self.e_h.pack(side="left", padx=4)
        self.e_h.insert(0, "0.2")

        styled_label(ctrl, "Methods to show:", FONT_SMALL, SUBTEXT).pack(anchor="w", pady=(8,2))
        self.v_euler    = tk.BooleanVar(value=True)
        self.v_improved = tk.BooleanVar(value=True)
        self.v_rk4      = tk.BooleanVar(value=True)
        for var, name, col in [
            (self.v_euler,    "Euler",          ERROR),
            (self.v_improved, "Improved Euler", ACCENT3),
            (self.v_rk4,      "Runge-Kutta 4",  ACCENT1),
        ]:
            tk.Checkbutton(ctrl, text=name, variable=var,
                           font=FONT_SMALL, fg=col, bg=PANEL,
                           selectcolor=ENTRY_BG, activebackground=PANEL,
                           activeforeground=col).pack(anchor="w")

        styled_button(ctrl, "▶  SOLVE & COMPARE", self.solve, color=ACCENT2).pack(pady=12, fill="x")

        self.err_var = tk.StringVar(value="")
        tk.Label(ctrl, textvariable=self.err_var, font=FONT_SMALL,
                 fg=ACCENT3, bg="#0f172a", justify="left",
                 wraplength=240, padx=8, pady=8).pack(fill="x")

        section_header(ctrl, "PRESETS", ACCENT3).pack(anchor="w", pady=(12,6))
        presets = [
            ("y' = -2y + t",  "-2*y + t",  "t/2 - 1/4 + (5/4)*exp(-2*t)", "0","1","3","0.2"),
            ("y' = y",        "y",          "exp(t)",                       "0","1","2","0.2"),
            ("y' = -y²",      "-y**2",      "1/(1+t)",                      "0","1","4","0.25"),
            ("y' = cos(t)",   "cos(t)",     "sin(t)",                       "0","0","6","0.3"),
            ("y' = t² - y",   "t**2 - y",   "",                             "0","0","5","0.25"),
        ]
        for name, fn, ex, t0, y0, te, h in presets:
            def make_cb(fn=fn, ex=ex, t0=t0, y0=y0, te=te, h=h):
                def cb():
                    for e, v in [(self.e_f, fn), (self.e_exact, ex), (self.e_t0, t0),
                                 (self.e_y0, y0), (self.e_tend, te), (self.e_h, h)]:
                        e.delete(0, "end"); e.insert(0, v)
                    self.solve()
                return cb
            preset_btn(ctrl, name, make_cb())

        plot_frame = styled_frame(f)
        plot_frame.pack(side="left", fill="both", expand=True, padx=(0,16), pady=16)
        self.fig = Figure(figsize=(6.5, 6), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.solve()

    def _ns(self):
        return {"exp": np.exp, "sin": np.sin, "cos": np.cos,
                "log": np.log, "sqrt": np.sqrt, "pi": np.pi,
                "tan": np.tan, "abs": np.abs, "np": np}

    def euler(self, f, t0, y0, h, n):
        t, y = [t0], [y0]
        for _ in range(n):
            y.append(y[-1] + h * f(t[-1], y[-1])); t.append(t[-1] + h)
        return np.array(t), np.array(y)

    def improved_euler(self, f, t0, y0, h, n):
        t, y = [t0], [y0]
        for _ in range(n):
            k1 = f(t[-1], y[-1]); k2 = f(t[-1]+h, y[-1]+h*k1)
            y.append(y[-1] + h*(k1+k2)/2); t.append(t[-1]+h)
        return np.array(t), np.array(y)

    def rk4(self, f, t0, y0, h, n):
        t, y = [t0], [y0]
        for _ in range(n):
            k1 = f(t[-1],     y[-1])
            k2 = f(t[-1]+h/2, y[-1]+h*k1/2)
            k3 = f(t[-1]+h/2, y[-1]+h*k2/2)
            k4 = f(t[-1]+h,   y[-1]+h*k3)
            y.append(y[-1] + h*(k1+2*k2+2*k3+k4)/6); t.append(t[-1]+h)
        return np.array(t), np.array(y)

    def solve(self):
        try:
            t0 = float(self.e_t0.get()); y0 = float(self.e_y0.get())
            t_end = float(self.e_tend.get()); h = float(self.e_h.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid numbers."); return

        n = max(1, int(round((t_end - t0) / h)))
        ns = self._ns()

        try:
            f_str = self.e_f.get().strip()
            f = lambda t, y, _s=f_str, _ns=ns: eval(_s, _ns, {"t": t, "y": y})
            f(t0, y0)
        except Exception as e:
            messagebox.showerror("f(t,y) Error", str(e)); return

        ex_str = self.e_exact.get().strip()
        has_exact = bool(ex_str)
        exact_fn = None
        if has_exact:
            try:
                exact_fn = lambda t_val, _s=ex_str, _ns=ns: eval(_s, _ns, {"t": t_val})
                exact_fn(t0)
            except Exception:
                has_exact = False

        self.ax1.clear(); self.ax2.clear()
        apply_dark_theme(self.fig, [self.ax1, self.ax2])

        methods = []
        if self.v_euler.get():    methods.append(("Euler",          self.euler,         ERROR))
        if self.v_improved.get(): methods.append(("Improved Euler", self.improved_euler, ACCENT3))
        if self.v_rk4.get():      methods.append(("RK4",            self.rk4,           ACCENT1))

        results = {}; err_lines = []
        for name, method, col in methods:
            t_arr, y_arr = method(f, t0, y0, h, n)
            results[name] = (t_arr, y_arr)
            self.ax1.plot(t_arr, y_arr, 'o-', color=col, linewidth=1.5,
                          markersize=4, label=name, alpha=0.9)

        if has_exact:
            t_fine = np.linspace(t0, t_end, 500)
            y_exact = np.array([exact_fn(ti) for ti in t_fine])
            self.ax1.plot(t_fine, y_exact, color="white", linewidth=2,
                          linestyle="--", label="Exact", zorder=5)
            for name, method, col in methods:
                t_arr, y_arr = results[name]
                y_ex = np.array([exact_fn(ti) for ti in t_arr])
                err = np.abs(y_arr - y_ex)
                self.ax2.semilogy(t_arr, err+1e-15, 'o-', color=col,
                                  linewidth=1.5, markersize=3, label=name)
                err_lines.append(f"{name:>16s}: final={err[-1]:.2e}  cum={np.sum(err):.2e}")
            self.ax2.set_title("Absolute Error (log scale)", fontsize=10)
            self.ax2.set_xlabel("t"); self.ax2.set_ylabel("|approx - exact|")
            self.ax2.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
        else:
            self.ax2.text(0.5, 0.5, "No exact solution provided\n(error plot unavailable)",
                         ha="center", va="center", color=SUBTEXT, fontsize=10,
                         transform=self.ax2.transAxes)

        self.ax1.set_title(f"y' = {self.e_f.get()},  y({t0})={y0},  h={h}", fontsize=9)
        self.ax1.set_xlabel("t"); self.ax1.set_ylabel("y")
        self.ax1.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
        self.fig.tight_layout(pad=2)
        self.canvas.draw()
        self.err_var.set("\n".join(err_lines) if err_lines else "")


# ════════════════════════════════════════════════════════════════════════════
# LAPLACE TRANSFORM TABLE  (pure numpy — no sympy)
# Each entry: name, f_fn(t), F_fn(s), f_label, F_label, steps text
# ════════════════════════════════════════════════════════════════════════════
LAPLACE_TABLE = [
    {
        "name": "1  (constant)",
        "f_fn": lambda t: np.ones_like(t),
        "F_fn": lambda s: 1.0/s,
        "f_label": "f(t) = 1",
        "F_label": "F(s) = 1/s",
        "steps": (
            "ℒ{1} — Direct integration\n\n"
            "  ℒ{1} = ∫₀^∞ e^(-st)·1 dt\n"
            "        = [-e^(-st)/s]₀^∞\n"
            "        = 0 - (-1/s)\n\n"
            "  F(s) = 1/s     (s > 0)\n"
        )
    },
    {
        "name": "t  (ramp)",
        "f_fn": lambda t: t,
        "F_fn": lambda s: 1.0/s**2,
        "f_label": "f(t) = t",
        "F_label": "F(s) = 1/s²",
        "steps": (
            "ℒ{t} — Power rule\n\n"
            "  ℒ{tⁿ} = n! / s^(n+1)\n\n"
            "  For n=1:\n"
            "  ℒ{t} = 1!/s² = 1/s²\n\n"
            "  F(s) = 1/s²     (s > 0)\n"
        )
    },
    {
        "name": "t²",
        "f_fn": lambda t: t**2,
        "F_fn": lambda s: 2.0/s**3,
        "f_label": "f(t) = t²",
        "F_label": "F(s) = 2/s³",
        "steps": (
            "ℒ{t²} — Power rule\n\n"
            "  ℒ{tⁿ} = n! / s^(n+1)\n\n"
            "  For n=2:\n"
            "  ℒ{t²} = 2!/s³ = 2/s³\n\n"
            "  F(s) = 2/s³     (s > 0)\n"
        )
    },
    {
        "name": "t³",
        "f_fn": lambda t: t**3,
        "F_fn": lambda s: 6.0/s**4,
        "f_label": "f(t) = t³",
        "F_label": "F(s) = 6/s⁴",
        "steps": (
            "ℒ{t³} — Power rule\n\n"
            "  ℒ{tⁿ} = n! / s^(n+1)\n\n"
            "  For n=3:\n"
            "  ℒ{t³} = 3!/s⁴ = 6/s⁴\n\n"
            "  F(s) = 6/s⁴     (s > 0)\n"
        )
    },
    {
        "name": "e^(2t)",
        "f_fn": lambda t: np.exp(2*t),
        "F_fn": lambda s: 1.0/(s-2),
        "f_label": "f(t) = e^(2t)",
        "F_label": "F(s) = 1/(s-2)",
        "steps": (
            "ℒ{e^(at)} — Exponential\n\n"
            "  ℒ{e^(at)} = ∫₀^∞ e^(-st)·e^(at) dt\n"
            "             = ∫₀^∞ e^(-(s-a)t) dt\n"
            "             = 1/(s-a)   (s > a)\n\n"
            "  Here a=2:\n"
            "  F(s) = 1/(s-2)     (s > 2)\n"
        )
    },
    {
        "name": "e^(-3t)",
        "f_fn": lambda t: np.exp(-3*t),
        "F_fn": lambda s: 1.0/(s+3),
        "f_label": "f(t) = e^(-3t)",
        "F_label": "F(s) = 1/(s+3)",
        "steps": (
            "ℒ{e^(-3t)} — Exponential decay\n\n"
            "  ℒ{e^(at)} = 1/(s-a)\n\n"
            "  Here a = -3:\n"
            "  ℒ{e^(-3t)} = 1/(s-(-3)) = 1/(s+3)\n\n"
            "  F(s) = 1/(s+3)     (s > -3)\n"
        )
    },
    {
        "name": "sin(2t)",
        "f_fn": lambda t: np.sin(2*t),
        "F_fn": lambda s: 2.0/(s**2+4),
        "f_label": "f(t) = sin(2t)",
        "F_label": "F(s) = 2/(s²+4)",
        "steps": (
            "ℒ{sin(bt)} — Sine transform\n\n"
            "  ℒ{sin(bt)} = b / (s²+b²)\n\n"
            "  Here b=2:\n"
            "  ℒ{sin(2t)} = 2/(s²+4)\n\n"
            "  Derived via Euler's formula:\n"
            "    sin(bt) = (e^(ibt) - e^(-ibt))/(2i)\n\n"
            "  F(s) = 2/(s²+4)     (s > 0)\n"
        )
    },
    {
        "name": "cos(3t)",
        "f_fn": lambda t: np.cos(3*t),
        "F_fn": lambda s: s/(s**2+9),
        "f_label": "f(t) = cos(3t)",
        "F_label": "F(s) = s/(s²+9)",
        "steps": (
            "ℒ{cos(bt)} — Cosine transform\n\n"
            "  ℒ{cos(bt)} = s / (s²+b²)\n\n"
            "  Here b=3:\n"
            "  ℒ{cos(3t)} = s/(s²+9)\n\n"
            "  F(s) = s/(s²+9)     (s > 0)\n"
        )
    },
    {
        "name": "e^(-t)·sin(2t)  [1st shift]",
        "f_fn": lambda t: np.exp(-t)*np.sin(2*t),
        "F_fn": lambda s: 2.0/((s+1)**2+4),
        "f_label": "f(t) = e^(-t)·sin(2t)",
        "F_label": "F(s) = 2/((s+1)²+4)",
        "steps": (
            "ℒ{e^(at)·f(t)} — First Shift Theorem\n\n"
            "  If ℒ{f(t)} = F(s),\n"
            "  then ℒ{e^(at)·f(t)} = F(s-a)\n\n"
            "  Here: f(t)=sin(2t), a=-1\n"
            "  ℒ{sin(2t)} = 2/(s²+4)\n\n"
            "  Replace s → s-(-1) = s+1:\n"
            "  F(s) = 2/((s+1)²+4)     (s > -1)\n"
        )
    },
    {
        "name": "e^(2t)·cos(t)  [1st shift]",
        "f_fn": lambda t: np.exp(2*t)*np.cos(t),
        "F_fn": lambda s: (s-2)/((s-2)**2+1),
        "f_label": "f(t) = e^(2t)·cos(t)",
        "F_label": "F(s) = (s-2)/((s-2)²+1)",
        "steps": (
            "ℒ{e^(2t)·cos(t)} — First Shift Theorem\n\n"
            "  ℒ{cos(bt)} = s/(s²+b²)\n\n"
            "  Here b=1, a=2. Replace s → s-2:\n"
            "  F(s) = (s-2)/((s-2)²+1)\n\n"
            "  F(s) = (s-2)/((s-2)²+1)     (s > 2)\n"
        )
    },
    {
        "name": "t·e^(-t)  [s-derivative rule]",
        "f_fn": lambda t: t*np.exp(-t),
        "F_fn": lambda s: 1.0/(s+1)**2,
        "f_label": "f(t) = t·e^(-t)",
        "F_label": "F(s) = 1/(s+1)²",
        "steps": (
            "ℒ{t·f(t)} = -d/ds[F(s)]\n\n"
            "  ℒ{e^(-t)} = 1/(s+1)\n\n"
            "  -d/ds[1/(s+1)] = 1/(s+1)²\n\n"
            "  F(s) = 1/(s+1)²     (s > -1)\n"
        )
    },
    {
        "name": "t²·e^(-2t)",
        "f_fn": lambda t: t**2*np.exp(-2*t),
        "F_fn": lambda s: 2.0/(s+2)**3,
        "f_label": "f(t) = t²·e^(-2t)",
        "F_label": "F(s) = 2/(s+2)³",
        "steps": (
            "ℒ{tⁿ·e^(at)} — Combined rule\n\n"
            "  ℒ{tⁿ·e^(at)} = n! / (s-a)^(n+1)\n\n"
            "  Here n=2, a=-2:\n"
            "  ℒ{t²·e^(-2t)} = 2!/(s+2)³ = 2/(s+2)³\n\n"
            "  F(s) = 2/(s+2)³     (s > -2)\n"
        )
    },
    {
        "name": "u(t-2)  [Heaviside]",
        "f_fn": lambda t: np.where(t >= 2, 1.0, 0.0),
        "F_fn": lambda s: np.exp(-2*s)/s,
        "f_label": "f(t) = u(t-2)",
        "F_label": "F(s) = e^(-2s)/s",
        "steps": (
            "ℒ{u(t-a)} — Unit Step function\n\n"
            "  u(t-a) = 0 for t < a\n"
            "           1 for t >= a\n\n"
            "  ℒ{u(t-a)} = ∫_a^∞ e^(-st) dt\n"
            "             = e^(-as)/s\n\n"
            "  Here a=2:\n"
            "  F(s) = e^(-2s)/s     (s > 0)\n"
        )
    },
    {
        "name": "u(t-1)·(t-1)²  [2nd shift]",
        "f_fn": lambda t: np.where(t >= 1, (t-1)**2, 0.0),
        "F_fn": lambda s: 2*np.exp(-s)/s**3,
        "f_label": "f(t) = u(t-1)·(t-1)²",
        "F_label": "F(s) = 2e^(-s)/s³",
        "steps": (
            "Second Shift Theorem\n\n"
            "  If ℒ{f(t)} = F(s),\n"
            "  then ℒ{u(t-a)·f(t-a)} = e^(-as)·F(s)\n\n"
            "  Here f(t)=t², a=1\n"
            "  ℒ{t²} = 2/s³\n\n"
            "  ℒ{u(t-1)·(t-1)²} = e^(-s)·(2/s³)\n\n"
            "  F(s) = 2e^(-s)/s³\n"
        )
    },
    {
        "name": "sin²(t)  [trig identity]",
        "f_fn": lambda t: np.sin(t)**2,
        "F_fn": lambda s: 2.0/(s*(s**2+4)),
        "f_label": "f(t) = sin²(t)",
        "F_label": "F(s) = 2/(s(s²+4))",
        "steps": (
            "ℒ{sin²(t)} — Trig identity + linearity\n\n"
            "  Identity: sin²(t) = (1 - cos(2t))/2\n\n"
            "  ℒ{sin²(t)} = ½ℒ{1} - ½ℒ{cos(2t)}\n"
            "              = 1/(2s) - s/(2(s²+4))\n\n"
            "  Common denom s(s²+4):\n"
            "  = (s²+4 - s²) / (2s(s²+4))\n"
            "  = 4 / (2s(s²+4))\n"
            "  = 2 / (s(s²+4))\n\n"
            "  F(s) = 2/(s(s²+4))\n"
        )
    },
]

INVERSE_TABLE = [
    {
        "name": "1/s",
        "f_fn": lambda t: np.ones_like(t),
        "F_fn": lambda s: 1.0/s,
        "f_label": "f(t) = 1",
        "F_label": "F(s) = 1/s",
        "steps": (
            "ℒ⁻¹{1/s}\n\n"
            "  Standard pair: ℒ{1} = 1/s\n\n"
            "  ℒ⁻¹{1/s} = 1  (unit step u(t))\n"
        )
    },
    {
        "name": "1/s²",
        "f_fn": lambda t: t,
        "F_fn": lambda s: 1.0/s**2,
        "f_label": "f(t) = t",
        "F_label": "F(s) = 1/s²",
        "steps": (
            "ℒ⁻¹{1/s²}\n\n"
            "  ℒ⁻¹{n!/s^(n+1)} = tⁿ\n"
            "  n=1: ℒ⁻¹{1/s²} = t\n"
        )
    },
    {
        "name": "2/s³",
        "f_fn": lambda t: t**2,
        "F_fn": lambda s: 2.0/s**3,
        "f_label": "f(t) = t²",
        "F_label": "F(s) = 2/s³",
        "steps": (
            "ℒ⁻¹{2/s³}\n\n"
            "  2/s³ = 2!/s³  →  n=2\n\n"
            "  ℒ⁻¹{2/s³} = t²\n"
        )
    },
    {
        "name": "1/(s+3)",
        "f_fn": lambda t: np.exp(-3*t),
        "F_fn": lambda s: 1.0/(s+3),
        "f_label": "f(t) = e^(-3t)",
        "F_label": "F(s) = 1/(s+3)",
        "steps": (
            "ℒ⁻¹{1/(s+3)}\n\n"
            "  ℒ{e^(at)} = 1/(s-a)  →  a=-3\n\n"
            "  ℒ⁻¹{1/(s+3)} = e^(-3t)\n"
        )
    },
    {
        "name": "3/(s²+9)",
        "f_fn": lambda t: np.sin(3*t),
        "F_fn": lambda s: 3.0/(s**2+9),
        "f_label": "f(t) = sin(3t)",
        "F_label": "F(s) = 3/(s²+9)",
        "steps": (
            "ℒ⁻¹{3/(s²+9)}\n\n"
            "  ℒ{sin(bt)} = b/(s²+b²)  →  b=3\n\n"
            "  ℒ⁻¹{3/(s²+9)} = sin(3t)\n"
        )
    },
    {
        "name": "s/(s²+4)",
        "f_fn": lambda t: np.cos(2*t),
        "F_fn": lambda s: s/(s**2+4),
        "f_label": "f(t) = cos(2t)",
        "F_label": "F(s) = s/(s²+4)",
        "steps": (
            "ℒ⁻¹{s/(s²+4)}\n\n"
            "  ℒ{cos(bt)} = s/(s²+b²)  →  b=2\n\n"
            "  ℒ⁻¹{s/(s²+4)} = cos(2t)\n"
        )
    },
    {
        "name": "1/(s+1)²  [repeated root]",
        "f_fn": lambda t: t*np.exp(-t),
        "F_fn": lambda s: 1.0/(s+1)**2,
        "f_label": "f(t) = t·e^(-t)",
        "F_label": "F(s) = 1/(s+1)²",
        "steps": (
            "ℒ⁻¹{1/(s+1)²}\n\n"
            "  ℒ{tⁿ·e^(at)} = n!/(s-a)^(n+1)\n"
            "  n=1, a=-1:\n"
            "  ℒ{t·e^(-t)} = 1/(s+1)²\n\n"
            "  ℒ⁻¹{1/(s+1)²} = t·e^(-t)\n"
        )
    },
    {
        "name": "4/((s+1)²+4)  [shift+sin]",
        "f_fn": lambda t: 2*np.exp(-t)*np.sin(2*t),
        "F_fn": lambda s: 4.0/((s+1)**2+4),
        "f_label": "f(t) = 2e^(-t)·sin(2t)",
        "F_label": "F(s) = 4/((s+1)²+4)",
        "steps": (
            "ℒ⁻¹{4/((s+1)²+4)}\n\n"
            "  Recognize: (s+1)²+4 = (s+1)²+2²\n\n"
            "  ℒ⁻¹{b/((s-a)²+b²)} = e^(at)·sin(bt)\n\n"
            "  a=-1, b=2:\n"
            "  4/((s+1)²+4) = 2·[2/((s+1)²+4)]\n\n"
            "  ℒ⁻¹ = 2·e^(-t)·sin(2t)\n"
        )
    },
    {
        "name": "(2s+5)/(s²+4s+13)  [complete sq]",
        "f_fn": lambda t: np.exp(-2*t)*(2*np.cos(3*t) + (1/3)*np.sin(3*t)),
        "F_fn": lambda s: (2*s+5)/(s**2+4*s+13),
        "f_label": "f(t) = e^(-2t)(2cos3t + sin3t/3)",
        "F_label": "F(s) = (2s+5)/(s²+4s+13)",
        "steps": (
            "ℒ⁻¹{(2s+5)/(s²+4s+13)}\n\n"
            "Step 1 — Complete the square:\n"
            "  s²+4s+13 = (s+2)²+9\n\n"
            "Step 2 — Rewrite numerator:\n"
            "  2s+5 = 2(s+2) + 1\n\n"
            "Step 3 — Split fraction:\n"
            "  = 2(s+2)/((s+2)²+9)\n"
            "  + 1/((s+2)²+9)\n\n"
            "Step 4 — Apply pairs (a=-2, b=3):\n"
            "  → 2e^(-2t)cos(3t)\n"
            "  + (1/3)e^(-2t)sin(3t)\n\n"
            "  f(t) = e^(-2t)(2cos3t + sin3t/3)\n"
        )
    },
    {
        "name": "1/(s(s+2))  [partial fractions]",
        "f_fn": lambda t: 0.5*(1 - np.exp(-2*t)),
        "F_fn": lambda s: 1.0/(s*(s+2)),
        "f_label": "f(t) = (1-e^(-2t))/2",
        "F_label": "F(s) = 1/(s(s+2))",
        "steps": (
            "ℒ⁻¹{1/(s(s+2))} — Partial Fractions\n\n"
            "  1/(s(s+2)) = A/s + B/(s+2)\n\n"
            "  1 = A(s+2) + B·s\n\n"
            "  s=0:  1=2A  →  A=1/2\n"
            "  s=-2: 1=-2B  →  B=-1/2\n\n"
            "  = (1/2)/s - (1/2)/(s+2)\n\n"
            "  ℒ⁻¹ = (1 - e^(-2t))/2\n"
        )
    },
    {
        "name": "(s+3)/(s²+2s-3)  [partial frac]",
        "f_fn": lambda t: np.exp(t),
        "F_fn": lambda s: (s+3)/(s**2+2*s-3),
        "f_label": "f(t) = e^t",
        "F_label": "F(s) = (s+3)/(s²+2s-3)",
        "steps": (
            "ℒ⁻¹{(s+3)/(s²+2s-3)}\n\n"
            "Step 1 — Factor denominator:\n"
            "  s²+2s-3 = (s+3)(s-1)\n\n"
            "Step 2 — Note cancellation:\n"
            "  (s+3)/((s+3)(s-1)) = 1/(s-1)\n\n"
            "Step 3 — Standard pair:\n"
            "  ℒ⁻¹{1/(s-1)} = e^t\n"
        )
    },
    {
        "name": "e^(-2s)/s  [2nd shift]",
        "f_fn": lambda t: np.where(t >= 2, 1.0, 0.0),
        "F_fn": lambda s: np.exp(-2*s)/s,
        "f_label": "f(t) = u(t-2)",
        "F_label": "F(s) = e^(-2s)/s",
        "steps": (
            "ℒ⁻¹{e^(-2s)/s} — Second Shift Theorem\n\n"
            "  ℒ⁻¹{e^(-as)F(s)} = u(t-a)·f(t-a)\n\n"
            "  Here a=2, F(s)=1/s  →  f(t)=1\n\n"
            "  ℒ⁻¹{e^(-2s)/s} = u(t-2)\n"
            "                  [step at t=2]\n"
        )
    },
    {
        "name": "2e^(-s)/s³  [2nd shift + t²]",
        "f_fn": lambda t: np.where(t >= 1, (t-1)**2, 0.0),
        "F_fn": lambda s: 2*np.exp(-s)/s**3,
        "f_label": "f(t) = u(t-1)·(t-1)²",
        "F_label": "F(s) = 2e^(-s)/s³",
        "steps": (
            "ℒ⁻¹{2e^(-s)/s³}\n\n"
            "  ℒ⁻¹{e^(-as)F(s)} = u(t-a)f(t-a)\n\n"
            "  F(s) = 2/s³ = ℒ{t²}  (a=1)\n\n"
            "  ℒ⁻¹{2e^(-s)/s³} = u(t-1)·(t-1)²\n"
        )
    },
]


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — LAPLACE TRANSFORMS
# ════════════════════════════════════════════════════════════════════════════
class LaplaceTab:
    def __init__(self, parent):
        self.frame = styled_frame(parent)
        self.build()

    def build(self):
        f = self.frame

        # Scrollable left panel
        left_outer = tk.Frame(f, bg=PANEL, width=320)
        left_outer.pack(side="left", fill="y")
        left_outer.pack_propagate(False)

        canvas_scroll = tk.Canvas(left_outer, bg=PANEL, highlightthickness=0)
        sb = tk.Scrollbar(left_outer, orient="vertical", command=canvas_scroll.yview)
        sf = tk.Frame(canvas_scroll, bg=PANEL)
        sf.bind("<Configure>",
                lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.create_window((0,0), window=sf, anchor="nw")
        canvas_scroll.configure(yscrollcommand=sb.set)
        canvas_scroll.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        pad = {"padx": 12}

        section_header(sf, "LAPLACE TRANSFORMS", ACCENT1).pack(anchor="w", pady=(12,8), **pad)

        # Mode
        mode_f = tk.Frame(sf, bg=PANEL); mode_f.pack(anchor="w", pady=6, **pad)
        self.v_mode = tk.StringVar(value="forward")
        for val, lbl, col in [("forward","ℒ{ f(t) }",ACCENT1),("inverse","ℒ⁻¹{ F(s) }",ACCENT2)]:
            tk.Radiobutton(mode_f, text=lbl, variable=self.v_mode, value=val,
                           font=("Courier New", 10, "bold"), fg=col, bg=PANEL,
                           selectcolor=ENTRY_BG, activebackground=PANEL,
                           activeforeground=col,
                           command=self._on_mode_change).pack(side="left", padx=4)

        tk.Label(sf, text="Select a transform pair:", font=FONT_SMALL,
                 fg=SUBTEXT, bg=PANEL).pack(anchor="w", pady=(6,2), **pad)

        lb_frame = tk.Frame(sf, bg=PANEL); lb_frame.pack(fill="x", **pad)
        self.listbox = tk.Listbox(lb_frame, font=FONT_SMALL, bg=ENTRY_BG, fg=TEXT,
                                  selectbackground=ACCENT2, selectforeground="white",
                                  relief="flat", bd=0, height=10, activestyle="none")
        self.listbox.pack(side="left", fill="x", expand=True)
        lb_sb = tk.Scrollbar(lb_frame, orient="vertical", command=self.listbox.yview)
        lb_sb.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=lb_sb.set)

        styled_button(sf, "▶  SHOW THIS TRANSFORM", self._show_selected, color=ACCENT2
                      ).pack(pady=8, fill="x", **pad)

        tk.Frame(sf, bg=BORDER, height=1).pack(fill="x", pady=6, **pad)

        section_header(sf, "RESULT", SUCCESS).pack(anchor="w", pady=(4,4), **pad)
        self.result_var = tk.StringVar(value="Select a pair and click Show.")
        tk.Label(sf, textvariable=self.result_var,
                 font=("Courier New", 10, "bold"), fg=SUCCESS, bg="#0f172a",
                 justify="left", wraplength=280, padx=10, pady=8
                 ).pack(fill="x", **pad)

        section_header(sf, "STEP-BY-STEP", SUBTEXT).pack(anchor="w", pady=(8,4), **pad)
        self.steps_text = tk.Text(sf, font=FONT_SMALL, bg="#0f172a", fg=TEXT,
                                  relief="flat", width=34, height=15,
                                  insertbackground=ACCENT1, wrap="word")
        self.steps_text.pack(fill="x", **pad)
        self.steps_text.config(state="disabled")

        section_header(sf, "QUICK REFERENCE", ACCENT3).pack(anchor="w", pady=(10,4), **pad)
        ref = (
            "FORWARD:\n"
            "  ℒ{1}        = 1/s\n"
            "  ℒ{tⁿ}       = n!/s^(n+1)\n"
            "  ℒ{e^(at)}   = 1/(s-a)\n"
            "  ℒ{sin(bt)}  = b/(s²+b²)\n"
            "  ℒ{cos(bt)}  = s/(s²+b²)\n"
            "  ℒ{e^(at)f}  = F(s-a)  [1st shift]\n"
            "  ℒ{u(t-a)f}  = e^(-as)F(s) [2nd]\n"
            "  ℒ{t·f(t)}   = -F'(s)\n\n"
            "INVERSE STRATEGIES:\n"
            "  • Match standard pairs directly\n"
            "  • Complete the square\n"
            "  • Partial fractions\n"
            "  • e^(-as)F(s) → u(t-a)f(t-a)\n\n"
            "LINEARITY:\n"
            "  ℒ{af+bg} = aF(s)+bG(s)\n"
        )
        tk.Label(sf, text=ref, font=("Courier New", 8),
                 fg=SUBTEXT, bg="#0f172a", justify="left",
                 padx=8, pady=8).pack(fill="x", **pad, pady=(0,12))

        # Right: plots
        plot_frame = styled_frame(f)
        plot_frame.pack(side="left", fill="both", expand=True, padx=(0,16), pady=16)
        self.fig = Figure(figsize=(6.5, 6.2), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._populate_listbox()
        self.listbox.selection_set(0)
        self._show_selected()

    def _on_mode_change(self):
        self._populate_listbox()
        self.listbox.selection_set(0)
        self._show_selected()

    def _populate_listbox(self):
        self.listbox.delete(0, "end")
        table = LAPLACE_TABLE if self.v_mode.get() == "forward" else INVERSE_TABLE
        for entry in table:
            self.listbox.insert("end", "  " + entry["name"])

    def _show_selected(self):
        sel = self.listbox.curselection()
        idx = sel[0] if sel else 0
        table = LAPLACE_TABLE if self.v_mode.get() == "forward" else INVERSE_TABLE
        entry = table[idx]

        if self.v_mode.get() == "forward":
            self.result_var.set(f"{entry['f_label']}\n  ↓  ℒ{{}}\n{entry['F_label']}")
        else:
            self.result_var.set(f"{entry['F_label']}\n  ↓  ℒ⁻¹{{}}\n{entry['f_label']}")

        self.steps_text.config(state="normal")
        self.steps_text.delete("1.0", "end")
        self.steps_text.insert("end", entry["steps"])
        self.steps_text.config(state="disabled")

        self._draw(entry)

    def _draw(self, entry):
        self.ax1.clear(); self.ax2.clear()
        apply_dark_theme(self.fig, [self.ax1, self.ax2])

        t_arr = np.linspace(0, 6, 600)
        try:
            y = np.clip(np.real(entry["f_fn"](t_arr)), -30, 30)
            self.ax1.plot(t_arr, y, color=ACCENT1, linewidth=2)
            self.ax1.fill_between(t_arr, 0, y, alpha=0.12, color=ACCENT1)
        except Exception:
            self.ax1.text(0.5, 0.5, "cannot plot", ha="center", va="center",
                         color=SUBTEXT, transform=self.ax1.transAxes)
        self.ax1.set_title(entry["f_label"], fontsize=9)
        self.ax1.set_xlabel("t"); self.ax1.set_ylabel("f(t)")
        self.ax1.axhline(0, color=BORDER, lw=0.8)

        s_arr = np.linspace(0.15, 8, 600)
        try:
            Fs = np.clip(np.real(entry["F_fn"](s_arr)), -30, 30)
            self.ax2.plot(s_arr, Fs, color=ACCENT2, linewidth=2)
            self.ax2.fill_between(s_arr, 0, Fs, alpha=0.12, color=ACCENT2)
        except Exception:
            self.ax2.text(0.5, 0.5, "cannot plot", ha="center", va="center",
                         color=SUBTEXT, transform=self.ax2.transAxes)
        self.ax2.set_title(entry["F_label"], fontsize=9)
        self.ax2.set_xlabel("s"); self.ax2.set_ylabel("F(s)")
        self.ax2.axhline(0, color=BORDER, lw=0.8)

        self.fig.tight_layout(pad=2)
        self.canvas.draw()


# ════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════════════════════════════════════
class App:
    def __init__(self, root):
        root.title("MA303 — Differential Equations Dashboard")
        root.configure(bg=BG)
        root.geometry("1200x820")
        root.minsize(1000, 700)

        header = tk.Frame(root, bg=BG, pady=10); header.pack(fill="x", padx=20)
        tk.Label(header, text="MA303", font=("Courier New", 28, "bold"),
                 fg=ACCENT1, bg=BG).pack(side="left")
        tk.Label(header, text=" DIFFERENTIAL EQUATIONS TOOLKIT",
                 font=("Courier New", 14), fg=SUBTEXT, bg=BG).pack(side="left", pady=4)
        tk.Label(header, text="Eigenvalues · Phase Portraits · Euler · RK4 · Laplace Transforms",
                 font=FONT_SMALL, fg=BORDER, bg=BG).pack(side="right")
        tk.Frame(root, bg=ACCENT2, height=2).pack(fill="x")

        style = ttk.Style(); style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[0,0,0,0])
        style.configure("TNotebook.Tab", background=PANEL, foreground=SUBTEXT,
                        font=("Courier New", 11, "bold"), padding=[18, 8], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(root); nb.pack(fill="both", expand=True, padx=8, pady=8)

        t1 = PhasePortraitTab(nb)
        t2 = NumericalSolverTab(nb)
        t3 = LaplaceTab(nb)

        nb.add(t1.frame, text="  📐 PHASE PORTRAITS  ")
        nb.add(t2.frame, text="  📈 NUMERICAL SOLVER  ")
        nb.add(t3.frame, text="  🔁 LAPLACE TRANSFORMS  ")

        footer = tk.Frame(root, bg=BG, pady=4); footer.pack(fill="x")
        tk.Label(footer,
                 text="Sections: 5.2 · 5.5 · 6.1 · 6.2 · 2.4–2.6 · 7.1–7.4 · Eigenvalue Method · RK4 · Partial Fractions",
                 font=FONT_SMALL, fg=BORDER, bg=BG).pack()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()