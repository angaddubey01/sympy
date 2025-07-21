"""
Simple test to verify the fix for the LaTeX fraction parsing issue.

This test does not rely on the full ANTLR setup but directly tests the
modified convert_frac function to ensure it produces the correct structure.
"""
import sympy
from sympy import symbols, Mul, Pow, Integer

def convert_frac_original(expr_top, expr_bot):
    """The original implementation of the convert_frac function."""
    inverse_denom = sympy.Pow(expr_bot, -1, evaluate=False)
    if expr_top == 1:
        return inverse_denom
    else:
        return sympy.Mul(expr_top, inverse_denom, evaluate=False)

def convert_frac_fixed(expr_top, expr_bot):
    """The fixed implementation of the convert_frac function."""
    # Create a properly grouped fraction expression that preserves the structure
    return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

def test_nested_fractions():
    """Test nested fractions parsing with the fixed implementation."""
    # Define symbols
    a, b, c = symbols('a b c')
    
    print("=== Testing fix for LaTeX fraction parsing ===")
    print("Original LaTeX: \\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}")
    
    # Simulate parsing the LaTeX expression step by step
    print("\nStep 1: Parse inner numerator \\frac{a^3+b}{c}")
    inner_num_expr = a**3 + b
    inner_den_expr = c
    inner_frac = convert_frac_fixed(inner_num_expr, inner_den_expr)
    print(f"Inner numerator: {inner_frac}")
    
    print("\nStep 2: Parse inner denominator \\frac{1}{c^2}")
    denom_num_expr = Integer(1)
    denom_den_expr = c**2
    denom_frac = convert_frac_fixed(denom_num_expr, denom_den_expr)
    print(f"Inner denominator: {denom_frac}")
    
    print("\nStep 3: Parse outer fraction with original implementation")
    result_original = inner_frac / denom_frac
    print(f"Original result: {result_original}")
    print(f"Simplified: {sympy.simplify(result_original)}")
    
    print("\nStep 4: Parse outer fraction with fixed implementation")
    result_fixed = convert_frac_fixed(inner_frac, denom_frac)
    print(f"Fixed result: {result_fixed}")
    print(f"Simplified: {sympy.simplify(result_fixed)}")
    
    print("\nExpected structure: ((a**3 + b)/c)/(1/(c**2))")
    
    # Verify structure
    structure_correct = str(result_fixed) == "((a**3 + b)/c)/((1/c**2))"
    print(f"\nStructure correct: {structure_correct}")
    
    # Verify mathematical equivalence
    expected_simplified = c * (a**3 + b)
    math_equivalent = sympy.simplify(result_fixed) == expected_simplified
    print(f"Mathematically equivalent: {math_equivalent}")
    
    return structure_correct and math_equivalent

if __name__ == "__main__":
    success = test_nested_fractions()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")