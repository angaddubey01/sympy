"""
Test script to debug LaTeX fraction parsing issue.
"""
from sympy import Symbol, Mul, Pow
import sympy

def convert_frac_current(expr_top, expr_bot):
    """Current implementation of convert_frac function from _parse_latex_antlr.py"""
    inverse_denom = sympy.Pow(expr_bot, -1, evaluate=False)
    if expr_top == 1:
        return inverse_denom
    else:
        return sympy.Mul(expr_top, inverse_denom, evaluate=False)

def convert_frac_fixed(expr_top, expr_bot):
    """Fixed implementation of convert_frac function"""
    # Create a properly grouped expression for nested fractions
    return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

def main():
    # Define symbols for testing
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    
    # Test case: (a^3 + b)/c divided by 1/c^2
    numerator = convert_frac_current(a**3 + b, c)
    denominator = convert_frac_current(1, c**2)
    
    # Current implementation result (wrong)
    current_result = numerator / denominator
    print("Current implementation result:")
    print(current_result)
    print(f"Simplified: {sympy.simplify(current_result)}")
    
    # Expected result
    expected_result = convert_frac_fixed(numerator, denominator)
    print("\nExpected result:")
    print(expected_result)
    print(f"Simplified: {sympy.simplify(expected_result)}")
    
    # Show the difference
    print("\nDifference in representation:")
    print(f"Current: {current_result}")
    print(f"Expected: {expected_result}")

if __name__ == "__main__":
    main()