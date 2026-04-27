#!/usr/bin/env python3
"""
MA303 Laplace Transform Calculator

A small command-line tool that computes Laplace transforms and inverse
Laplace transforms of many standard symbolic expressions using SymPy.

Examples:
    python laplace_calculator.py laplace "t**2 * exp(-t)"
    python laplace_calculator.py inverse "(s+1)/(s**2+9)"
    python laplace_calculator.py demo
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)


TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

# Symbols used throughout the calculator.
t = sp.symbols("t", real=True, nonnegative=True)
s = sp.symbols("s", real=True)
a = sp.symbols("a", real=True)

ALLOWED_NAMES = {
    "t": t,
    "s": s,
    "pi": sp.pi,
    "E": sp.E,
    "exp": sp.exp,
    "sin": sp.sin,
    "cos": sp.cos,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "sqrt": sp.sqrt,
    "log": sp.log,
    "Heaviside": sp.Heaviside,
}


@dataclass
class CalculationResult:
    mode: str
    input_expr: sp.Expr
    output_expr: sp.Expr


def safe_parse(expression: str, variable_name: str) -> sp.Expr:
    """Parse a user expression into a SymPy expression.

    Args:
        expression: Expression typed by the user.
        variable_name: The expected main variable, either 't' or 's'.

    Returns:
        Parsed SymPy expression.

    Raises:
        ValueError: If parsing fails or the expression uses the wrong variable.
    """
    try:
        expr = parse_expr(
            expression,
            local_dict=ALLOWED_NAMES,
            transformations=TRANSFORMATIONS,
            evaluate=True,
        )
    except Exception as exc:  # pragma: no cover - defensive error handling
        raise ValueError(f"Could not parse expression: {expression}") from exc

    other_var = s if variable_name == "t" else t
    main_var = t if variable_name == "t" else s

    if expr.has(other_var) and not expr.has(main_var):
        raise ValueError(
            f"Expression appears to use '{other_var}' instead of '{main_var}'."
        )

    return sp.simplify(expr)


def compute_laplace(expression: str) -> CalculationResult:
    expr = safe_parse(expression, "t")
    transformed = sp.laplace_transform(expr, t, s, noconds=True)
    return CalculationResult("Laplace transform", expr, sp.simplify(transformed))


def compute_inverse_laplace(expression: str) -> CalculationResult:
    expr = safe_parse(expression, "s")
    transformed = sp.inverse_laplace_transform(expr, s, t)
    return CalculationResult(
        "Inverse Laplace transform", expr, sp.simplify(transformed)
    )


def print_result(result: CalculationResult) -> None:
    print(f"\n{result.mode}")
    print("-" * len(result.mode))
    print(f"Input : {sp.pretty(result.input_expr)}")
    print(f"Output: {sp.pretty(result.output_expr)}")
    print("\nMachine-friendly output:")
    print(result.output_expr)


def run_demo() -> None:
    demo_cases = [
        ("laplace", "5*t**3 - sin(t) + t**2*exp(-t)"),
        ("inverse", "7/s**2 + 6/(s-3)**4 + (s+1)/(s**2+9)"),
        ("laplace", "Heaviside(t-1)*(t-1)"),
    ]

    print("MA303 Laplace Calculator Demo")
    print("=" * 28)
    for mode, expr in demo_cases:
        if mode == "laplace":
            result = compute_laplace(expr)
        else:
            result = compute_inverse_laplace(expr)
        print_result(result)
        print("\n" + "=" * 60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compute Laplace transforms and inverse Laplace transforms for many "
            "standard symbolic expressions."
        )
    )
    subparsers = parser.add_subparsers(dest="command")

    laplace_parser = subparsers.add_parser(
        "laplace", help="Compute the Laplace transform F(s) of a function f(t)."
    )
    laplace_parser.add_argument(
        "expression",
        type=str,
        help='Expression in t, for example: "t**2 * exp(-t)"',
    )

    inverse_parser = subparsers.add_parser(
        "inverse",
        help="Compute the inverse Laplace transform f(t) of an expression F(s).",
    )
    inverse_parser.add_argument(
        "expression",
        type=str,
        help='Expression in s, for example: "(s+1)/(s**2+9)"',
    )

    subparsers.add_parser("demo", help="Run built-in demonstration examples.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    try:
        if args.command == "laplace":
            result = compute_laplace(args.expression)
            print_result(result)
        elif args.command == "inverse":
            result = compute_inverse_laplace(args.expression)
            print_result(result)
        elif args.command == "demo":
            run_demo()
        else:  # pragma: no cover - unreachable with argparse, kept for safety
            parser.error("Unknown command")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive error handling
        print(
            "Error: SymPy could not compute that transform. Try a simpler expression "
            f"or a standard Laplace form. Details: {exc}",
            file=sys.stderr,
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
