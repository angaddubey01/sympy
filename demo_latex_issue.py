"""
This script demonstrates the LaTeX parsing issue with nested fractions
by manually constructing the expressions that would be created by the parser
with the current implementation and the fixed implementation.
"""
import sympy
from sympy import Symbol, Mul, Pow, sympify
import re

def format_expr(expr):
    """Format expression as a LaTeX string."""
    from sympy.printing.latex import latex
    return latex(expr)

def current_parser_behavior():
    """Simulate the current behavior of the LaTeX parser."""
    # Define symbols
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    
    # Inner fraction: (a^3 + b) / c
    inner_num = a**3 + b
    inner_den = c
    inner_frac = Mul(inner_num, Pow(inner_den, -1, evaluate=False), evaluate=False)
    
    # Outer fraction denominator: 1 / c^2
    denom_num = 1
    denom_den = c**2
    denom_frac = Mul(denom_num, Pow(denom_den, -1, evaluate=False), evaluate=False)
    
    # This is how the current parser would handle it incorrectly:
    # It doesn't properly group the denominator fraction
    current = inner_frac / denom_num / denom_den
    
    return current, str(current)

def expected_parser_behavior():
    """Simulate the expected behavior of the fixed LaTeX parser."""
    # Define symbols
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    
    # Inner fraction: (a^3 + b) / c
    inner_num = a**3 + b
    inner_den = c
    inner_frac = Mul(inner_num, Pow(inner_den, -1, evaluate=False), evaluate=False)
    
    # Outer fraction denominator: 1 / c^2
    denom_num = 1
    denom_den = c**2
    denom_frac = Mul(denom_num, Pow(denom_den, -1, evaluate=False), evaluate=False)
    
    # This is how it should be parsed with proper grouping:
    # The denominator fraction should be grouped correctly
    expected = Mul(inner_frac, Pow(denom_frac, -1, evaluate=False), evaluate=False)
    
    return expected, str(expected)

def main():
    """Main function demonstrating the issue."""
    print("LaTeX expression: \\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}")
    
    # Get current and expected behavior
    current, current_str = current_parser_behavior()
    expected, expected_str = expected_parser_behavior()
    
    # Display results
    print("\nCurrent parser output:")
    print(f"Expression: {current}")
    print(f"String representation: {current_str}")
    
    print("\nExpected parser output:")
    print(f"Expression: {expected}")
    print(f"String representation: {expected_str}")
    
    # Verify they simplify to the same mathematical expression
    current_simplified = sympy.simplify(current)
    expected_simplified = sympy.simplify(expected)
    print("\nSimplified expressions:")
    print(f"Current: {current_simplified}")
    print(f"Expected: {expected_simplified}")
    print(f"Mathematically equivalent: {current_simplified == expected_simplified}")
    
    # Show LaTeX representation
    print("\nLaTeX representation:")
    print(f"Current:  {format_expr(current)}")
    print(f"Expected: {format_expr(expected)}")

if __name__ == "__main__":
    main()