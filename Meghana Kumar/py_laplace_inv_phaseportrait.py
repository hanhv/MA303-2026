import sys
import numpy as np
from sympy import (
    symbols, exp, sin, cos, laplace_transform, inverse_laplace_transform,
    apart, factor, simplify, latex, pretty, sympify, Heaviside,
    re, im, Rational, pi, E, I, sqrt, Abs, conjugate,
    Symbol, Function, Piecewise, oo, integrate, Integral, Matrix
)
from sympy.abc import t, s, a

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QStackedWidget,
    QScrollArea, QSizePolicy, QFrame, QGridLayout,
    QTextEdit, QSpacerItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPalette

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'


# ─────────────────────────────────────────────
#  GLOBAL STYLESHEET
# ─────────────────────────────────────────────
STYLE = """
QWidget {
    background-color: #0a0a0a;
    color: #e8e8e8;
    font-family: 'Courier New', monospace;
    font-size: 13px;
}
QLabel#title {
    font-size: 32px;
    font-weight: bold;
    color: #00ffcc;
    letter-spacing: 4px;
}
QLabel#subtitle {
    font-size: 13px;
    color: #555;
    letter-spacing: 2px;
}
QLabel#section {
    font-size: 15px;
    font-weight: bold;
    color: #00ffcc;
    padding: 4px 0;
    border-bottom: 1px solid #1a1a1a;
}
QLabel#example {
    color: #888;
    font-size: 12px;
    padding: 6px 10px;
    background: #111;
    border-left: 2px solid #00ffcc44;
}
QPushButton#main_btn {
    background-color: #0a0a0a;
    border: 1px solid #00ffcc;
    color: #00ffcc;
    padding: 14px 20px;
    font-size: 13px;
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
    text-align: left;
}
QPushButton#main_btn:hover {
    background-color: #00ffcc18;
    border: 1px solid #00ffccaa;
}
QPushButton#action_btn {
    background-color: #00ffcc;
    color: #0a0a0a;
    border: none;
    padding: 10px 24px;
    font-size: 13px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    letter-spacing: 2px;
}
QPushButton#action_btn:hover {
    background-color: #00ddaa;
}
QPushButton#back_btn {
    background-color: transparent;
    border: none;
    color: #555;
    font-size: 12px;
    font-family: 'Courier New', monospace;
    letter-spacing: 1px;
    padding: 4px 8px;
}
QPushButton#back_btn:hover {
    color: #00ffcc;
}
QLineEdit {
    background-color: #111;
    border: 1px solid #2a2a2a;
    color: #e8e8e8;
    padding: 8px 10px;
    font-family: 'Courier New', monospace;
    selection-background-color: #00ffcc33;
}
QLineEdit:focus {
    border: 1px solid #00ffcc55;
}
QTextEdit {
    background-color: #080808;
    border: 1px solid #1a1a1a;
    color: #c8fce8;
    padding: 10px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}
QScrollArea {
    border: none;
    background-color: #0a0a0a;
}
QScrollBar:vertical {
    background: #0a0a0a;
    width: 6px;
}
QScrollBar::handle:vertical {
    background: #333;
    border-radius: 3px;
}
QFrame#divider {
    background: #1a1a1a;
    max-height: 1px;
}
"""


# ─────────────────────────────────────────────
#  MATH RENDERING CANVAS
# ─────────────────────────────────────────────
class MathCanvas(FigureCanvas):
    BG = "#0a0a0a"
    TEXT_COLOR = "#e8e8e8"
    ACCENT = "#00ffcc"
    STEP_LABEL_COLOR = "#00ffcc"
    DIVIDER_COLOR = "#1e1e1e"

    def __init__(self, parent=None):
        self.fig = Figure(facecolor=self.BG)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(200)

    def render_steps(self, steps):
        """
        Absolute-inch layout. Nothing clips, nothing overlaps.
        Step dict keys:
          'label'    – heading string
          'lines'    – list of strings; '$...$' = mathtext; leading spaces = indent
          'center'   – if True, every line in this block is x-centered
          'is_result'– teal highlight box
        Line dict alternative: {'text': '...', 'center': True} for per-line centering.
        """
        self.fig.clear()

        FIG_W      = 8.0
        DPI        = 96
        ML         = 0.40   # left margin (inches)
        MR         = 0.30   # right margin
        MT         = 0.18   # top margin
        MB         = 0.25   # bottom margin

        LABEL_H    = 0.26   # step heading row height
        LINE_H     = 0.28   # plain/math line — generous to avoid overlap
        MATH_H     = 0.34   # taller for lines with fractions/integrals
        BLANK_H    = 0.10   # empty spacer
        BLOCK_PAD  = 0.16   # gap after each block
        RULE_GAP   = 0.04   # gap between rule and first line

        def _line_h(raw):
            s = raw.strip() if isinstance(raw, str) else raw.get('text', '').strip()
            if not s:
                return BLANK_H
            is_m = s.startswith('$') and s.endswith('$')
            if is_m and any(tok in s for tok in
                            [r'\dfrac', r'\frac', r'\int', r'\sqrt', r'\mathcal']):
                return MATH_H
            return LINE_H

        # ── pass 1: total height ─────────────────────────────────────────
        total = 0.0
        for step in steps:
            total += LABEL_H + RULE_GAP
            for ln in step.get('lines', []):
                total += _line_h(ln)
            total += BLOCK_PAD

        fig_h = max(MT + total + MB, 3.0)
        self.fig.set_size_inches(FIG_W, fig_h)
        self.setMinimumHeight(int(fig_h * DPI))
        self.setMaximumHeight(int(fig_h * DPI) + 2)

        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        ax.set_facecolor(self.BG)
        ax.set_xlim(0, FIG_W)
        ax.set_ylim(0, fig_h)

        CX = FIG_W / 2.0    # center x for centered lines

        y = fig_h - MT      # cursor: top → bottom

        for step in steps:
            label      = step.get('label', '')
            lines      = step.get('lines', [])
            is_result  = step.get('is_result', False)
            blk_center = step.get('center', False)

            # ── highlight rect for result block ──────────────────────────
            if is_result:
                bh = LABEL_H + RULE_GAP + sum(_line_h(l) for l in lines) + BLOCK_PAD
                ax.add_patch(plt.Rectangle(
                    (ML - 0.12, y - bh), FIG_W - ML - MR + 0.12, bh,
                    facecolor="#00ffcc0b", edgecolor="#00ffcc60",
                    linewidth=0.8, clip_on=False
                ))

            # ── step label + divider rule ────────────────────────────────
            if label:
                ax.text(
                    ML, y - LABEL_H * 0.54,
                    label,
                    fontsize=9.5, color=self.ACCENT,
                    fontfamily='monospace', fontweight='bold',
                    va='center', clip_on=False
                )
                ry = y - LABEL_H
                ax.plot([ML, FIG_W - MR], [ry, ry],
                        color=self.DIVIDER_COLOR, lw=0.6, clip_on=False)
                y = ry - RULE_GAP

            # ── render lines ─────────────────────────────────────────────
            for raw in lines:
                # support both plain strings and {'text':..., 'center':...} dicts
                if isinstance(raw, dict):
                    text    = raw.get('text', '')
                    ln_ctr  = raw.get('center', blk_center)
                else:
                    text    = raw
                    ln_ctr  = blk_center

                stripped = text.strip()
                lh       = _line_h(raw)

                if not stripped:
                    y -= lh
                    continue

                is_math = stripped.startswith('$') and stripped.endswith('$')
                color   = self.ACCENT if (is_result and is_math) else self.TEXT_COLOR
                fsize   = 11.0 if is_math else 9.2
                ffam    = 'serif' if is_math else 'monospace'

                indent = (len(text) - len(text.lstrip(' '))) * 0.05

                if ln_ctr:
                    xp, ha = CX, 'center'
                else:
                    xp, ha = ML + 0.12 + indent, 'left'

                try:
                    ax.text(xp, y - lh * 0.5, stripped,
                            fontsize=fsize, color=color,
                            fontfamily=ffam, va='center',
                            ha=ha, usetex=False, clip_on=False)
                except Exception:
                    ax.text(xp, y - lh * 0.5, stripped.strip('$'),
                            fontsize=9.2, color=self.TEXT_COLOR,
                            fontfamily='monospace', va='center',
                            ha=ha, clip_on=False)
                y -= lh

            y -= BLOCK_PAD

        self.fig.canvas.draw_idle()


# ─────────────────────────────────────────────
#  SYMPY → MATHTEXT HELPERS
# ─────────────────────────────────────────────
def sym_to_mathtext(expr):
    try:
        ltx = latex(expr)
        return f"${ltx}$"
    except Exception:
        return str(expr)


def partial_fraction_terms(F_partial, s_sym):
    from sympy import Add
    if isinstance(F_partial, Add):
        return [sym_to_mathtext(term) for term in F_partial.args]
    return [sym_to_mathtext(F_partial)]


def fmt_num(v, decimals=4):
    """Format a number cleanly — omit imaginary part if zero."""
    r = round(v.real, decimals)
    im = round(v.imag, decimals)
    if abs(im) < 1e-9:
        return f"{r:g}"
    sign = "+" if im >= 0 else "-"
    return f"{r:g} {sign} {abs(im):g}i"


def fmt_latex_num(v, decimals=4):
    """Return a LaTeX string for a possibly-complex number."""
    r = round(v.real, decimals)
    im_v = round(v.imag, decimals)
    if abs(im_v) < 1e-9:
        return f"{r:g}"
    sign = "+" if im_v >= 0 else "-"
    return r"{r}\,{sign}\,{im}i".format(r=r, sign=sign, im=abs(im_v))


# ─────────────────────────────────────────────
#  EXACT SYMPY EIGENANALYSIS
# ─────────────────────────────────────────────
def _sym_val(v):
    """Pretty-print a sympy expression for use inside $...$."""
    try:
        return latex(v)
    except Exception:
        return str(v)


def _plain(v):
    """Plain readable string (no latex)."""
    try:
        from sympy import nsimplify, Rational as R
        return str(v)
    except Exception:
        return str(v)


def build_eigen_steps(A_np, eigvals_np, eigvecs_np, cls):
    """
    Build step list using exact sympy arithmetic.
    A_np : numpy 2x2 float array
    """
    from sympy import (Rational, sqrt, symbols, factor, expand,
                       simplify, nsimplify, radsimp, cancel)

    # Convert entries to exact sympy Rationals
    a11 = nsimplify(A_np[0, 0], rational=True)
    a12 = nsimplify(A_np[0, 1], rational=True)
    a21 = nsimplify(A_np[1, 0], rational=True)
    a22 = nsimplify(A_np[1, 1], rational=True)

    tr  = a11 + a22
    det = a11 * a22 - a12 * a21
    disc = tr**2 - 4 * det   # discriminant (exact)
    disc_simplified = simplify(disc)

    steps = []

    # ── Step 1: Matrix & properties ─────────────────────────────────────
    steps.append({
        'label': 'Step 1 — System Matrix A',
        'lines': [
            f'  A  =  [ {_plain(a11)}    {_plain(a12)} ]',
            f'         [ {_plain(a21)}    {_plain(a22)} ]',
            '',
            f'  Trace     tr(A)  =  a + d  =  {_plain(a11)} + {_plain(a22)}  =  {_plain(tr)}',
            f'  Det    det(A)  =  ad - bc  =  ({_plain(a11)})({_plain(a22)}) - ({_plain(a12)})({_plain(a21)})  =  {_plain(det)}',
        ]
    })

    # ── Step 2: Characteristic equation ─────────────────────────────────
    # Build the char poly display string piece by piece
    tr_coeff = -tr          # coefficient of λ in  λ² + (tr_coeff)λ + det
    char_terms = [r'$\lambda^{2}$']
    if tr_coeff != 0:
        char_terms.append(f'${"+" if tr_coeff > 0 else ""}{_sym_val(tr_coeff)}\\,\\lambda$')
    if det != 0:
        char_terms.append(f'${"+" if det > 0 else ""}{_sym_val(det)}$')
    char_poly_str = '  ' + '  '.join(char_terms) + '  =  0'

    disc_description = (
        'D > 0   →   two distinct real eigenvalues' if disc_simplified > 0
        else ('D = 0   →   one repeated real eigenvalue' if disc_simplified == 0
              else 'D < 0   →   complex conjugate eigenvalues')
    )

    steps.append({
        'label': 'Step 2 — Characteristic Equation   det(A − λI) = 0',
        'lines': [
            r'  $\lambda^{2} - \mathrm{tr}(A)\,\lambda + \det(A) = 0$',
            '',
            f'  $\\lambda^{{2}} - ({_sym_val(tr)})\\,\\lambda + ({_sym_val(det)}) = 0$',
            '',
            char_poly_str,
            '',
            f'  Discriminant   D  =  tr² - 4·det',
            f'                    =  ({_plain(tr)})² - 4·({_plain(det)})',
            f'                    =  {_plain(tr**2)}  -  {_plain(4*det)}',
            f'                    =  {_plain(disc_simplified)}',
            '',
            f'  {disc_description}',
        ]
    })

    # ── Step 3: Eigenvalues (exact) ──────────────────────────────────────
    lam_sym = symbols('lambda')
    sqrt_disc = sqrt(disc_simplified)

    lam1_exact = (tr + sqrt_disc) / 2
    lam2_exact = (tr - sqrt_disc) / 2
    lam1_s = simplify(lam1_exact)
    lam2_s = simplify(lam2_exact)

    lam_lines = [
        r'  $\lambda \;=\; \dfrac{\mathrm{tr}(A) \;\pm\; \sqrt{D}}{2}$',
        '',
        f'  $\\lambda = \\dfrac{{{_sym_val(tr)} \\pm \\sqrt{{{_sym_val(disc_simplified)}}}}}{{2}}$',
        '',
        f'  $\\lambda_{{1}} = \\dfrac{{{_sym_val(tr)} + {_sym_val(sqrt_disc)}}}{{2}} = {_sym_val(lam1_s)}$',
        f'  $\\lambda_{{2}} = \\dfrac{{{_sym_val(tr)} - {_sym_val(sqrt_disc)}}}{{2}} = {_sym_val(lam2_s)}$',
    ]
    steps.append({'label': 'Step 3 — Eigenvalues (exact)', 'lines': lam_lines})

    # ── Step 4: Eigenvectors (full row reduction) ────────────────────────
    ev_lines = []
    for i, lam_s in enumerate([lam1_s, lam2_s]):
        lam_label = f'\\lambda_{{{i+1}}} = {_sym_val(lam_s)}'

        # Entries of (A - λI)
        b11 = simplify(a11 - lam_s)
        b12 = a12
        b21 = a21
        b22 = simplify(a22 - lam_s)

        ev_lines.append(f'  For  $\\lambda_{{{i+1}}} = {_sym_val(lam_s)}$:')
        ev_lines.append('')
        ev_lines.append(f'    A - {_sym_val(lam_s)}·I  =  [ {_plain(b11)}    {_plain(b12)} ]')
        ev_lines.append(f'                          [ {_plain(b21)}    {_plain(b22)} ]')
        ev_lines.append('')
        ev_lines.append(f'    Solve:  {_plain(b11)}·v₁  +  {_plain(b12)}·v₂  =  0')

        # Find eigenvector symbolically
        from sympy import Eq, solve as sym_solve
        v1_sym, v2_sym = symbols('v1 v2')

        # Use first non-trivial row to express ratio
        if b11 != 0 or b12 != 0:
            if b12 != 0:
                # v1 = -b12/b11 * v2 if b11 != 0, else v1 is free
                if b11 != 0:
                    ratio = simplify(-b12 / b11)
                    ev_lines.append(f'    {_plain(b11)}·v₁  =  -{_plain(b12)}·v₂')
                    ev_lines.append(f'    v₁  =  {_sym_val(ratio)}·v₂')
                    ev_lines.append(f'    Set v₂ = 1   →   v₁ = {_sym_val(ratio)}')
                    vec = Matrix([ratio, 1])
                else:
                    # b11 == 0, b12 != 0  →  v2 = 0, v1 free
                    ev_lines.append(f'    0·v₁  +  {_plain(b12)}·v₂  =  0   →   v₂ = 0')
                    ev_lines.append(f'    Set v₁ = 1')
                    vec = Matrix([1, 0])
            else:
                # b12 == 0, b11 != 0  →  v1 = 0, v2 free
                ev_lines.append(f'    {_plain(b11)}·v₁  =  0   →   v₁ = 0')
                ev_lines.append(f'    Set v₂ = 1')
                vec = Matrix([0, 1])
        else:
            vec = Matrix([1, 0])

        ev_lines.append('')
        ev_lines.append(f'    Eigenvector:  $\\mathbf{{v}}_{{{i+1}}} = ({_sym_val(vec[0])},\\; {_sym_val(vec[1])})^\\top$')
        ev_lines.append('')

    steps.append({'label': 'Step 4 — Eigenvectors   (A − λI)v = 0', 'lines': ev_lines})

    # ── Step 5: General solution ─────────────────────────────────────────
    sol_lines = []
    if disc_simplified >= 0:
        # real eigenvalues
        sol_lines += [
            r'  $\mathbf{x}(t) = c_1\,e^{\lambda_1 t}\,\mathbf{v}_1 \;+\; c_2\,e^{\lambda_2 t}\,\mathbf{v}_2$',
            '',
            f'  with  $\\lambda_1 = {_sym_val(lam1_s)},\\quad \\lambda_2 = {_sym_val(lam2_s)}$',
        ]
    else:
        alpha = simplify(tr / 2)
        beta  = simplify(sqrt(-disc_simplified) / 2)
        sol_lines += [
            '  Complex eigenvalues  →  apply Eulers formula:',
            r'  $e^{(\alpha \pm \beta i)\,t} = e^{\alpha t}(\cos\beta t \pm i\sin\beta t)$',
            '',
            f'  $\\alpha = {_sym_val(alpha)}, \\qquad \\beta = {_sym_val(beta)}$',
            '',
            f'  $\\mathbf{{x}}(t) = e^{{{_sym_val(alpha)}t}}\\bigl['
            f'c_1\\,\\mathbf{{u}}\\cos({_sym_val(beta)}t)'
            f' + c_2\\,\\mathbf{{w}}\\sin({_sym_val(beta)}t)\\bigr]$',
            '  where u and w are the real / imaginary parts of the eigenvector.',
        ]
    steps.append({'label': 'Step 5 — General Solution', 'lines': sol_lines})

    # ── Step 6: Classification ────────────────────────────────────────────
    defs = {
        "Stable Node":
            ["All trajectories converge to the origin.",
             "Eigenvalues are both real and negative."],
        "Unstable Node":
            ["All trajectories diverge from the origin.",
             "Eigenvalues are both real and positive."],
        "Saddle Point":
            ["Trajectories approach along one eigenvector, escape along the other.",
             "Eigenvalues are real with opposite signs."],
        "Stable Spiral":
            ["Trajectories spiral inward to the origin.",
             r"  $\mathrm{Re}(\lambda) < 0$  with nonzero imaginary part."],
        "Unstable Spiral":
            ["Trajectories spiral outward from the origin.",
             r"  $\mathrm{Re}(\lambda) > 0$  with nonzero imaginary part."],
        "Center":
            ["Closed elliptical orbits — neutrally stable.",
             r"  $\mathrm{Re}(\lambda) = 0$  (purely imaginary eigenvalues)."],
    }
    cls_lines = [f'  Classification:  {cls}', ''] + defs.get(cls, [])
    steps.append({
        'label': 'Step 6 — Equilibrium Classification',
        'lines': cls_lines,
        'is_result': True,
        'center': True,
    })

    return steps


# ─────────────────────────────────────────────
#  LAPLACE HELPERS
# ─────────────────────────────────────────────
def compute_laplace(expr_str):
    t_sym = symbols('t', positive=True)
    s_sym = symbols('s')
    try:
        f = sympify(expr_str, locals={
            't': t_sym, 'e': E, 'sin': sin, 'cos': cos,
            'exp': exp, 'pi': pi, 'sqrt': sqrt
        })
        F, plane, _ = laplace_transform(f, t_sym, s_sym, noconds=False)
        F_simplified = simplify(F)

        # ── decompose f into additive terms and identify each pair ───────
        from sympy import Add, Mul, Pow, Integer
        terms = list(f.as_ordered_terms()) if isinstance(f, Add) else [f]

        match_lines = []
        for term in terms:
            term_latex = latex(term)
            term_F, _, _ = laplace_transform(term, t_sym, s_sym, noconds=False)
            term_F_s = simplify(term_F)
            match_lines.append(
                f'$\\mathcal{{L}}\\{{{term_latex}\\}} = {latex(term_F_s)}$'
            )

        steps = [
            {
                'label': 'Step 1 — Input',
                'lines': [
                    'Function to transform:',
                    f'$f(t) = {latex(f)}$',
                    '',
                    'Variable:   t  (time domain)',
                    'Transform variable:   s  (frequency domain)',
                ],
            },
            {
                'label': 'Step 2 — Definition of the Laplace Transform',
                'lines': [
                    r'$\mathcal{L}\{f(t)\} = F(s) = \int_{0}^{\infty} f(t)\, e^{-st}\, dt$',
                    '',
                    'We apply this to each term of f(t) separately.',
                ],
            },
            {
                'label': 'Step 3 — Standard Transform Pairs Used',
                'lines': [
                    'Reference table  (a, b, n  are constants):',
                    '',
                    r'$\mathcal{L}\{1\}           = \dfrac{1}{s}$',
                    r'$\mathcal{L}\{t^{n}\}        = \dfrac{n!}{s^{n+1}}$',
                    r'$\mathcal{L}\{e^{-at}\}     = \dfrac{1}{s+a}$',
                    r'$\mathcal{L}\{\sin(bt)\}    = \dfrac{b}{s^{2}+b^{2}}$',
                    r'$\mathcal{L}\{\cos(bt)\}    = \dfrac{s}{s^{2}+b^{2}}$',
                    r'$\mathcal{L}\{t\,e^{-at}\}  = \dfrac{1}{(s+a)^{2}}$',
                ],
            },
            {
                'label': 'Step 4 — Apply to Each Term',
                'lines': ['Transforming term by term:',  ''] + match_lines,
            },
            {
                'label': 'Step 5 — Result',
                'lines': [
                    '',
                    f'$F(s) = {latex(F_simplified)}$',
                    '',
                    f'Region of convergence:   $\\mathrm{{Re}}(s) > {latex(plane)}$',
                ],
                'is_result': True,
                'center': True,
            },
        ]
        return F_simplified, steps, None
    except Exception as e:
        return None, [], str(e)


def compute_inverse_laplace(expr_str):
    s_sym = symbols('s')
    t_sym = symbols('t', positive=True)
    try:
        F = sympify(expr_str, locals={'s': s_sym, 'e': E, 'pi': pi, 'sqrt': sqrt})
        F_partial = apart(F, s_sym)
        f = inverse_laplace_transform(F_partial, s_sym, t_sym)
        f_simplified = simplify(f)

        from sympy import Add
        pf_terms = list(F_partial.as_ordered_terms()) if isinstance(F_partial, Add) else [F_partial]

        # Build per-term inverse lines
        inv_lines = ['Inverting term by term:', '']
        for term in pf_terms:
            term_f = inverse_laplace_transform(term, s_sym, t_sym)
            term_f_s = simplify(term_f)
            inv_lines.append(
                f'$\\mathcal{{L}}^{{-1}}\\left\\{{{latex(term)}\\right\\}} = {latex(term_f_s)}$'
            )

        steps = [
            {
                'label': 'Step 1 — Input',
                'lines': [
                    'Function to invert:',
                    f'$F(s) = {latex(F)}$',
                    '',
                    'Variable:   s  (frequency domain)',
                    'Recover:    f(t)  in the time domain',
                ],
            },
            {
                'label': 'Step 2 — Partial Fraction Decomposition',
                'lines': [
                    'Split F(s) into simpler fractions matching table entries:',
                    '',
                    f'$F(s) = {latex(F_partial)}$',
                ] + (['', 'Individual partial fraction terms:'] +
                     [f'  $\\bullet\\;{latex(t)}$' for t in pf_terms]
                     if len(pf_terms) > 1 else []),
            },
            {
                'label': 'Step 3 — Inverse Laplace Table  (a, b  are constants)',
                'lines': [
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{1}{s}\right\}          = 1$',
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{1}{s+a}\right\}        = e^{-at}$',
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{s}{s^{2}+b^{2}}\right\} = \cos(bt)$',
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{b}{s^{2}+b^{2}}\right\} = \sin(bt)$',
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{1}{(s+a)^{2}}\right\}  = t\,e^{-at}$',
                    r'$\mathcal{L}^{-1}\!\left\{\dfrac{n!}{s^{n+1}}\right\}   = t^{n}$',
                ],
            },
            {
                'label': 'Step 4 — Apply Inverse to Each Term',
                'lines': inv_lines,
            },
            {
                'label': 'Step 5 — Result',
                'lines': [
                    '',
                    f'$f(t) = {latex(f_simplified)}$',
                    '',
                    '(valid for  t > 0)',
                ],
                'is_result': True,
                'center': True,
            },
        ]
        return f_simplified, steps, None
    except Exception as e:
        return None, [], str(e)


# ─────────────────────────────────────────────
#  CLASSIFICATION
# ─────────────────────────────────────────────
def classify(eigvals):
    r = np.real(eigvals)
    im_vals = np.imag(eigvals)
    if np.allclose(im_vals, 0, atol=1e-9):
        if np.all(r < -1e-9):
            return "Stable Node"
        elif np.all(r > 1e-9):
            return "Unstable Node"
        else:
            return "Saddle Point"
    else:
        avg_r = np.mean(r)
        if avg_r < -1e-9:
            return "Stable Spiral"
        elif avg_r > 1e-9:
            return "Unstable Spiral"
        else:
            return "Center"


# ─────────────────────────────────────────────
#  REUSABLE HELPERS
# ─────────────────────────────────────────────
def make_divider():
    f = QFrame()
    f.setObjectName("divider")
    f.setFixedHeight(1)
    return f


def make_label(text, obj_name=None, wrap=False):
    lbl = QLabel(text)
    if obj_name:
        lbl.setObjectName(obj_name)
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def make_back_btn(stack, target_idx):
    btn = QPushButton("← BACK")
    btn.setObjectName("back_btn")
    btn.setFixedWidth(80)
    btn.clicked.connect(lambda: stack.setCurrentIndex(target_idx))
    return btn


def scroll_wrap(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    return scroll


def make_phase_canvas(figure):
    canvas = FigureCanvas(figure)
    canvas.setMinimumHeight(340)
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return canvas


def plot_phase_portrait(ax, A):
    ax.set_facecolor("#0a0a0a")
    lim = 5
    x = np.linspace(-lim, lim, 20)
    y = np.linspace(-lim, lim, 20)
    X, Y = np.meshgrid(x, y)
    U = A[0, 0] * X + A[0, 1] * Y
    V = A[1, 0] * X + A[1, 1] * Y
    speed = np.sqrt(U**2 + V**2)
    speed[speed == 0] = 1
    ax.quiver(X, Y, U / speed, V / speed, speed,
              cmap="Blues", alpha=0.5, scale=25)

    colors = ["#00ffcc", "#ff6b6b", "#ffd166", "#a8dadc", "#c77dff"]
    ci = 0
    for x0 in [-3, -1.5, 1.5, 3]:
        for y0 in [-3, -1.5, 1.5, 3]:
            traj_f, traj_b = [], []
            dt = 0.04
            Xp = np.array([x0, y0], dtype=float)
            for _ in range(250):
                Xp = Xp + dt * (A @ Xp)
                if np.linalg.norm(Xp) > 20:
                    break
                traj_f.append(Xp.copy())
            Xp = np.array([x0, y0], dtype=float)
            for _ in range(250):
                Xp = Xp - dt * (A @ Xp)
                if np.linalg.norm(Xp) > 20:
                    break
                traj_b.append(Xp.copy())
            color = colors[ci % len(colors)]
            ci += 1
            if traj_f:
                tf = np.array(traj_f)
                ax.plot(tf[:, 0], tf[:, 1], color=color, lw=0.9, alpha=0.75)
            if traj_b:
                tb = np.array(traj_b)
                ax.plot(tb[:, 0], tb[:, 1], color=color, lw=0.9, alpha=0.4, ls="--")

    ax.axhline(0, color="#333", lw=0.7)
    ax.axvline(0, color="#333", lw=0.7)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("x₁", color="#888")
    ax.set_ylabel("x₂", color="#888")
    ax.tick_params(colors="#555")
    for spine in ax.spines.values():
        spine.set_edgecolor("#222")
    ax.grid(True, color="#181818", lw=0.5)


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase Portrait & Laplace Analyzer")
        self.setGeometry(80, 60, 1200, 780)
        self.setStyleSheet(STYLE)

        plt.rcParams.update({
            "figure.facecolor": "#0a0a0a",
            "axes.facecolor": "#0a0a0a",
            "text.color": "#e8e8e8",
        })

        self.stack = QStackedWidget()
        self.page_intro = QWidget()
        self.page_menu = QWidget()
        self.page_matrix = QWidget()
        self.page_diffeq = QWidget()
        self.page_laplace = QWidget()
        self.page_invlap = QWidget()

        for page in [self.page_intro, self.page_menu, self.page_matrix,
                     self.page_diffeq, self.page_laplace, self.page_invlap]:
            self.stack.addWidget(page)

        self.init_intro()
        self.init_menu()
        self.init_matrix_page()
        self.init_diffeq_page()
        self.init_laplace_page()
        self.init_invlaplace_page()

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self.stack)
        self.setLayout(root)

    # ══════════════════════════════════════════════
    #  PAGE 0 — INTRO
    # ══════════════════════════════════════════════
    def init_intro(self):
        outer = QVBoxLayout()
        outer.setContentsMargins(80, 60, 80, 60)
        outer.addStretch(2)

        title = make_label("PHASE PORTRAIT &\nLAPLACE ANALYZER", "title")
        title.setAlignment(Qt.AlignLeft)
        outer.addWidget(title)

        outer.addSpacing(8)
        outer.addWidget(make_label("differential equations · eigenanalysis · transforms", "subtitle"))
        outer.addWidget(make_divider())
        outer.addSpacing(40)

        outer.addWidget(make_label("ENTER YOUR NAME"))
        outer.addSpacing(6)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g.  Ada Lovelace")
        self.name_input.setFixedWidth(320)
        outer.addWidget(self.name_input)

        outer.addSpacing(24)
        start = QPushButton("START  →")
        start.setObjectName("action_btn")
        start.setFixedWidth(160)
        start.clicked.connect(self.go_to_menu)
        outer.addWidget(start)

        outer.addStretch(3)
        self.page_intro.setLayout(outer)

    def go_to_menu(self):
        name = self.name_input.text().strip() or "Student"
        self.menu_greeting.setText(f"Welcome, {name}.")
        self.stack.setCurrentIndex(1)

    # ══════════════════════════════════════════════
    #  PAGE 1 — MENU
    # ══════════════════════════════════════════════
    def init_menu(self):
        outer = QVBoxLayout()
        outer.setContentsMargins(80, 50, 80, 50)

        self.menu_greeting = make_label("Welcome.", "title")
        self.menu_greeting.setStyleSheet("font-size: 26px; color: #00ffcc; letter-spacing: 3px;")
        outer.addWidget(self.menu_greeting)
        outer.addSpacing(4)
        outer.addWidget(make_label("SELECT AN ANALYSIS MODE", "subtitle"))
        outer.addWidget(make_divider())
        outer.addSpacing(30)

        buttons = [
            ("01  MATRIX INPUT",
             "Plot phase portrait from a 2×2 matrix  |  eigenvalues · eigenvectors · classification",
             2),
            ("02  DIFFERENTIAL EQUATION INPUT",
             "Enter dx/dt equations directly  |  auto-extract matrix · full analysis",
             3),
            ("03  LAPLACE TRANSFORM",
             "Enter f(t)  →  compute F(s) with step-by-step work",
             4),
            ("04  INVERSE LAPLACE TRANSFORM",
             "Enter F(s)  →  recover f(t) via partial fractions",
             5),
        ]

        for label, desc, idx in buttons:
            btn = QPushButton(f"  {label}\n  {desc}")
            btn.setObjectName("main_btn")
            btn.setMinimumHeight(72)
            btn.clicked.connect(lambda checked, i=idx: self.stack.setCurrentIndex(i))
            outer.addWidget(btn)
            outer.addSpacing(10)

        outer.addStretch()
        self.page_menu.setLayout(outer)

    # ══════════════════════════════════════════════
    #  PAGE 2 — MATRIX ANALYSIS
    # ══════════════════════════════════════════════
    def init_matrix_page(self):
        container = QWidget()
        outer = QVBoxLayout()
        outer.setContentsMargins(60, 30, 60, 30)

        hdr = QHBoxLayout()
        hdr.addWidget(make_back_btn(self.stack, 1))
        hdr.addSpacing(16)
        hdr.addWidget(make_label("MATRIX ANALYSIS", "section"))
        hdr.addStretch()
        outer.addLayout(hdr)
        outer.addWidget(make_divider())
        outer.addSpacing(16)

        outer.addWidget(make_label(
            "EXAMPLE:   A = [[1, 2], [−3, 1]]   →   enter each entry below", "example"))
        outer.addSpacing(14)

        # ── 2×2 matrix entry: label directly above each box ──────────────
        outer.addWidget(make_label("Enter matrix A:"))
        outer.addSpacing(6)

        mat_row = QHBoxLayout()
        mat_row.setSpacing(0)
        mat_row.addSpacing(10)

        # Build a QGridLayout: row0 = labels, row1 = boxes, for 2 cols × 2 rows
        mat_grid = QGridLayout()
        mat_grid.setHorizontalSpacing(14)
        mat_grid.setVerticalSpacing(4)

        self.ma = QLineEdit("1");  self.mb = QLineEdit("2")
        self.mc = QLineEdit("-3"); self.md = QLineEdit("1")

        entries = [
            ("a", self.ma, 0, 0), ("b", self.mb, 0, 1),
            ("c", self.mc, 1, 0), ("d", self.md, 1, 1),
        ]
        for letter, widget, row, col in entries:
            lbl = make_label(letter)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #00ffcc; font-size: 13px; font-weight: bold;")
            lbl.setFixedWidth(90)
            widget.setFixedWidth(90)
            widget.setAlignment(Qt.AlignCenter)
            mat_grid.addWidget(lbl,    row * 2,     col)
            mat_grid.addWidget(widget, row * 2 + 1, col)

        mat_row.addLayout(mat_grid)
        mat_row.addStretch()
        outer.addLayout(mat_row)

        outer.addSpacing(8)
        matrix_hint = make_label(
            "  System:  x₁' = a·x₁ + b·x₂\n"
            "           x₂' = c·x₁ + d·x₂", "example")
        outer.addWidget(matrix_hint)
        outer.addSpacing(14)

        analyze = QPushButton("ANALYZE")
        analyze.setObjectName("action_btn")
        analyze.setFixedWidth(140)
        analyze.clicked.connect(self.run_matrix)
        outer.addWidget(analyze)
        outer.addSpacing(16)

        self.mat_figure = Figure(figsize=(7, 4), dpi=100)
        self.mat_canvas = make_phase_canvas(self.mat_figure)
        outer.addWidget(self.mat_canvas)
        outer.addSpacing(12)

        outer.addWidget(make_label("STEP-BY-STEP OUTPUT", "section"))
        self.mat_math_canvas = MathCanvas()
        outer.addWidget(self.mat_math_canvas)

        self.mat_error = QLabel("")
        self.mat_error.setStyleSheet("color: #ff6b6b; font-size: 12px; padding: 6px;")
        self.mat_error.setWordWrap(True)
        self.mat_error.hide()
        outer.addWidget(self.mat_error)

        container.setLayout(outer)
        self.page_matrix.setLayout(QVBoxLayout())
        self.page_matrix.layout().setContentsMargins(0, 0, 0, 0)
        self.page_matrix.layout().addWidget(scroll_wrap(container))

    def run_matrix(self):
        try:
            A = np.array([
                [float(self.ma.text()), float(self.mb.text())],
                [float(self.mc.text()), float(self.md.text())]
            ])
        except ValueError:
            self.mat_error.setText("Invalid input. Please enter numeric values.")
            self.mat_error.show()
            return
        self._analyze_and_display(A, self.mat_figure, self.mat_canvas,
                                   self.mat_math_canvas, self.mat_error)

    def _analyze_and_display(self, A, figure, phase_canvas, math_canvas, error_label):
        try:
            eigvals_np, _ = np.linalg.eig(A)
            cls = classify(eigvals_np)
            steps = build_eigen_steps(A, eigvals_np, None, cls)

            error_label.hide()
            math_canvas.show()
            math_canvas.render_steps(steps)

            figure.clear()
            ax = figure.add_subplot(111)
            plot_phase_portrait(ax, A)
            ax.set_title(f"Phase Portrait  —  {cls}", color="#00ffcc", pad=8)
            figure.tight_layout()
            phase_canvas.draw()
        except Exception as e:
            import traceback
            error_label.setText(f"Analysis error: {e}\n{traceback.format_exc()[-400:]}")
            error_label.show()

    # ══════════════════════════════════════════════
    #  PAGE 3 — DIFFERENTIAL EQUATION INPUT
    # ══════════════════════════════════════════════
    def init_diffeq_page(self):
        container = QWidget()
        outer = QVBoxLayout()
        outer.setContentsMargins(60, 30, 60, 30)

        hdr = QHBoxLayout()
        hdr.addWidget(make_back_btn(self.stack, 1))
        hdr.addSpacing(16)
        hdr.addWidget(make_label("DIFFERENTIAL EQUATION INPUT", "section"))
        hdr.addStretch()
        outer.addLayout(hdr)
        outer.addWidget(make_divider())
        outer.addSpacing(16)

        outer.addWidget(make_label(
            "EXAMPLE:   dx₁/dt = 1·x₁ + 2·x₂   →   enter coefficients a, b\n"
            "           dx₂/dt = −3·x₁ + 1·x₂  →   enter coefficients c, d",
            "example"))
        outer.addSpacing(14)

        # ── Equation rows: label | [box] · x₁ + [box] · x₂ ─────────────
        # Each box has its letter label (a/b/c/d) directly above it
        outer.addWidget(make_label("Enter the system  x' = A·x  by specifying coefficients:"))
        outer.addSpacing(8)

        self.de_a = QLineEdit("1");  self.de_b = QLineEdit("2")
        self.de_c = QLineEdit("-3"); self.de_d = QLineEdit("1")

        def labeled_box(letter, widget):
            """Return a QVBoxLayout: accent label on top, input box below."""
            col = QVBoxLayout()
            col.setSpacing(3)
            lbl = QLabel(letter)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #00ffcc; font-size: 12px; font-weight: bold;")
            lbl.setFixedWidth(80)
            widget.setFixedWidth(80)
            widget.setAlignment(Qt.AlignCenter)
            col.addWidget(lbl)
            col.addWidget(widget)
            return col

        def plain_lbl(text):
            l = QLabel(text)
            l.setStyleSheet("color: #888; font-size: 13px;")
            l.setAlignment(Qt.AlignBottom)
            return l

        # Row 1: dx₁/dt = [a]·x₁ + [b]·x₂
        row1 = QHBoxLayout()
        row1.setSpacing(6)
        row1.addWidget(plain_lbl("dx₁/dt  ="))
        row1.addLayout(labeled_box("a", self.de_a))
        row1.addWidget(plain_lbl("· x₁   +"))
        row1.addLayout(labeled_box("b", self.de_b))
        row1.addWidget(plain_lbl("· x₂"))
        row1.addStretch()

        # Row 2: dx₂/dt = [c]·x₁ + [d]·x₂
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        row2.addWidget(plain_lbl("dx₂/dt  ="))
        row2.addLayout(labeled_box("c", self.de_c))
        row2.addWidget(plain_lbl("· x₁   +"))
        row2.addLayout(labeled_box("d", self.de_d))
        row2.addWidget(plain_lbl("· x₂"))
        row2.addStretch()

        outer.addLayout(row1)
        outer.addSpacing(6)
        outer.addLayout(row2)
        outer.addSpacing(14)

        analyze = QPushButton("ANALYZE")
        analyze.setObjectName("action_btn")
        analyze.setFixedWidth(140)
        analyze.clicked.connect(self.run_diffeq)
        outer.addWidget(analyze)
        outer.addSpacing(16)

        self.de_figure = Figure(figsize=(7, 4), dpi=100)
        self.de_canvas = make_phase_canvas(self.de_figure)
        outer.addWidget(self.de_canvas)
        outer.addSpacing(12)

        outer.addWidget(make_label("STEP-BY-STEP OUTPUT", "section"))
        self.de_math_canvas = MathCanvas()
        outer.addWidget(self.de_math_canvas)

        self.de_error = QLabel("")
        self.de_error.setStyleSheet("color: #ff6b6b; font-size: 12px; padding: 6px;")
        self.de_error.setWordWrap(True)
        self.de_error.hide()
        outer.addWidget(self.de_error)

        container.setLayout(outer)
        self.page_diffeq.setLayout(QVBoxLayout())
        self.page_diffeq.layout().setContentsMargins(0, 0, 0, 0)
        self.page_diffeq.layout().addWidget(scroll_wrap(container))

    def run_diffeq(self):
        try:
            A = np.array([
                [float(self.de_a.text()), float(self.de_b.text())],
                [float(self.de_c.text()), float(self.de_d.text())]
            ])
        except ValueError:
            self.de_error.setText("Invalid input. Please enter numeric coefficients.")
            self.de_error.show()
            return
        self._analyze_and_display(A, self.de_figure, self.de_canvas,
                                   self.de_math_canvas, self.de_error)

    # ══════════════════════════════════════════════
    #  PAGE 4 — LAPLACE TRANSFORM
    # ══════════════════════════════════════════════
    def init_laplace_page(self):
        container = QWidget()
        outer = QVBoxLayout()
        outer.setContentsMargins(60, 30, 60, 30)

        hdr = QHBoxLayout()
        hdr.addWidget(make_back_btn(self.stack, 1))
        hdr.addSpacing(16)
        hdr.addWidget(make_label("LAPLACE TRANSFORM   f(t) → F(s)", "section"))
        hdr.addStretch()
        outer.addLayout(hdr)
        outer.addWidget(make_divider())
        outer.addSpacing(16)

        outer.addWidget(make_label(
            "EXAMPLES:  t**2        →  2/s**3\n"
            "           exp(-3*t)   →  1/(s+3)\n"
            "           sin(2*t)    →  2/(s**2+4)\n"
            "           t*exp(-t)   →  1/(s+1)**2\n"
            "           cos(t) + exp(-2*t)  →  combined",
            "example"))
        outer.addSpacing(10)

        outer.addWidget(make_label("Enter  f(t)  using Python/SymPy syntax:"))
        outer.addSpacing(6)

        row = QHBoxLayout()
        self.lap_input = QLineEdit("t**2 + exp(-3*t)")
        row.addWidget(self.lap_input)
        btn = QPushButton("COMPUTE")
        btn.setObjectName("action_btn")
        btn.setFixedWidth(130)
        btn.clicked.connect(self.run_laplace)
        row.addWidget(btn)
        outer.addLayout(row)
        outer.addSpacing(16)

        outer.addWidget(make_label("STEP-BY-STEP OUTPUT", "section"))

        self.lap_math_canvas = MathCanvas()
        outer.addWidget(self.lap_math_canvas)

        self.lap_error = QLabel("")
        self.lap_error.setStyleSheet("color: #ff6b6b; font-size: 12px; padding: 6px;")
        self.lap_error.setWordWrap(True)
        self.lap_error.hide()
        outer.addWidget(self.lap_error)

        container.setLayout(outer)
        self.page_laplace.setLayout(QVBoxLayout())
        self.page_laplace.layout().setContentsMargins(0, 0, 0, 0)
        self.page_laplace.layout().addWidget(scroll_wrap(container))

    def run_laplace(self):
        expr = self.lap_input.text().strip()
        result, steps, err = compute_laplace(expr)
        if err:
            self.lap_error.setText(f"Error: {err}\n\nSupported: exp(t), sin(t), cos(t), t**2, t*exp(-t), etc.")
            self.lap_error.show()
            self.lap_math_canvas.hide()
        else:
            self.lap_error.hide()
            self.lap_math_canvas.show()
            self.lap_math_canvas.render_steps(steps)

    # ══════════════════════════════════════════════
    #  PAGE 5 — INVERSE LAPLACE
    # ══════════════════════════════════════════════
    def init_invlaplace_page(self):
        container = QWidget()
        outer = QVBoxLayout()
        outer.setContentsMargins(60, 30, 60, 30)

        hdr = QHBoxLayout()
        hdr.addWidget(make_back_btn(self.stack, 1))
        hdr.addSpacing(16)
        hdr.addWidget(make_label("INVERSE LAPLACE TRANSFORM   F(s) → f(t)", "section"))
        hdr.addStretch()
        outer.addLayout(hdr)
        outer.addWidget(make_divider())
        outer.addSpacing(16)

        outer.addWidget(make_label(
            "EXAMPLES:  1/(s+3)           →  exp(-3t)\n"
            "           s/(s**2+4)        →  cos(2t)\n"
            "           2/(s**2+4)        →  sin(2t)\n"
            "           1/(s+1)**2        →  t*exp(-t)\n"
            "           (s+1)/((s+2)*(s+3))  →  partial fractions",
            "example"))
        outer.addSpacing(10)

        outer.addWidget(make_label("Enter  F(s)  using Python/SymPy syntax:"))
        outer.addSpacing(6)

        row = QHBoxLayout()
        self.invlap_input = QLineEdit("1/(s**2 + 4)")
        row.addWidget(self.invlap_input)
        btn = QPushButton("COMPUTE")
        btn.setObjectName("action_btn")
        btn.setFixedWidth(130)
        btn.clicked.connect(self.run_invlaplace)
        row.addWidget(btn)
        outer.addLayout(row)
        outer.addSpacing(16)

        outer.addWidget(make_label("STEP-BY-STEP OUTPUT", "section"))

        self.invlap_math_canvas = MathCanvas()
        outer.addWidget(self.invlap_math_canvas)

        self.invlap_error = QLabel("")
        self.invlap_error.setStyleSheet("color: #ff6b6b; font-size: 12px; padding: 6px;")
        self.invlap_error.setWordWrap(True)
        self.invlap_error.hide()
        outer.addWidget(self.invlap_error)

        container.setLayout(outer)
        self.page_invlap.setLayout(QVBoxLayout())
        self.page_invlap.layout().setContentsMargins(0, 0, 0, 0)
        self.page_invlap.layout().addWidget(scroll_wrap(container))

    def run_invlaplace(self):
        expr = self.invlap_input.text().strip()
        result, steps, err = compute_inverse_laplace(expr)
        if err:
            self.invlap_error.setText(f"Error: {err}\n\nSupported: 1/(s+a), s/(s²+b²), 1/(s-a)², etc.")
            self.invlap_error.show()
            self.invlap_math_canvas.hide()
        else:
            self.invlap_error.hide()
            self.invlap_math_canvas.show()
            self.invlap_math_canvas.render_steps(steps)


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())