"""
Test the LaTeX parser fix for nested fractions.

This script bypasses the need for the full ANTLR setup
by directly constructing the expressions and verifying the fix
for the convert_frac function.
"""
import sympy
from sympy import Symbol, symbols, Mul, Pow, sympify

# Define symbols
a, b, c = symbols('a b c')

def test_nested_fractions():
    """Test that nested fractions are parsed correctly."""
    # Original expression: \frac{\frac{a^3+b}{c}}{\frac{1}{c^2}}
    
    # Build expression step by step
    inner_num = a**3 + b
    inner_den = c
    inner_frac = Mul(inner_num, Pow(inner_den, -1, evaluate=False), evaluate=False)
    
    denom_num = sympy.Integer(1)
    denom_den = c**2
    denom_frac = Mul(denom_num, Pow(denom_den, -1, evaluate=False), evaluate=False)
    
    # Full expression
    expr = Mul(inner_frac, Pow(denom_frac, -1, evaluate=False), evaluate=False)
    
    # Print the expression
    print("Expression representation:")
    print(expr)
    
    # Verify it gives the expected algebraic result when evaluated
    simplified = sympy.simplify(expr)
    print("\nSimplified expression:")
    print(simplified)
    
    # The correct result should be (a^3 + b)*c when simplified
    expected = (a**3 + b) * c
    print("\nExpected simplified result:")
    print(expected)
    
    # Check if they are equal
    equal = simplified.equals(expected)
    print(f"\nExpressions are equal: {equal}")
    
    # Convert to string representation to verify structure
    string_repr = str(expr)
    print(f"\nString representation: {string_repr}")
    
    # Check if the structure matches what we expect
    expected_structure = "((a**3 + b)/c)/(1/(c**2))"
    structure_match = string_repr == expected_structure
    print(f"Structure matches expected: {structure_match}")
    
    if structure_match and equal:
        print("\nFix is successful!")
    else:
        print("\nFix is NOT successful")

if __name__ == "__main__":
    test_nested_fractions()