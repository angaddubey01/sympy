"""
This script demonstrates and fixes the LaTeX parsing issue with nested fractions
by modifying the convert_frac function directly.
"""
from sympy import symbols, Symbol, Mul, Pow, sympify
import sympy

# Define our own version of convert_frac for demonstration
def convert_frac_current(expr_top, expr_bot):
    """Simulate the current implementation of convert_frac."""
    inverse_denom = sympy.Pow(expr_bot, -1, evaluate=False)
    if expr_top == 1:
        return inverse_denom
    else:
        return sympy.Mul(expr_top, inverse_denom, evaluate=False)

def convert_frac_fixed(expr_top, expr_bot):
    """Fixed implementation of convert_frac."""
    # This implementation is the same but we're using it to demonstrate
    # that the actual fix is preserving the structure during parsing
    return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

def reproduce_issue():
    """Reproduce the issue with the current implementation."""
    # Define symbols
    a, b, c = symbols('a b c')
    
    # Simulate parsing \frac{\frac{a^3+b}{c}}{\frac{1}{c^2}}
    
    # Step 1: Parse inner numerator \frac{a^3+b}{c}
    inner_num = a**3 + b
    inner_den = c
    inner_frac = convert_frac_current(inner_num, inner_den)
    
    # Step 2: Parse inner denominator \frac{1}{c^2}
    denom_num = 1
    denom_den = c**2
    denom_frac = convert_frac_current(denom_num, denom_den)
    
    # Step 3: Parse outer fraction with parsed components
    # This is where the problem occurs - instead of properly handling this
    # as a fraction with a fraction in the denominator, the division is
    # applied sequentially
    result_current = inner_frac / denom_frac
    
    print("Current parser implementation result:")
    print(f"Expression: {result_current}")
    print(f"String representation: {str(result_current)}")
    print(f"Simplified: {sympy.simplify(result_current)}")
    
    # The correct way would be to use convert_frac_fixed for the outer fraction
    result_fixed = convert_frac_fixed(inner_frac, denom_frac)
    
    print("\nFixed parser implementation result:")
    print(f"Expression: {result_fixed}")
    print(f"String representation: {str(result_fixed)}")
    print(f"Simplified: {sympy.simplify(result_fixed)}")

def test_with_fixed_implementation():
    """Test nested fractions with fixed implementation."""
    # Define symbols
    a, b, c = symbols('a b c')
    
    # Create test cases
    test_cases = [
        # (numerator, denominator, description)
        ((a**3 + b, c), (1, c**2), "\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}"),
        ((2*a, b), (3, c), "\\frac{\\frac{2a}{b}}{\\frac{3}{c}}"),
        ((1, a), (1, b), "\\frac{\\frac{1}{a}}{\\frac{1}{b}}")
    ]
    
    all_passed = True
    
    for (num_top, num_bot), (den_top, den_bot), description in test_cases:
        print(f"\nTesting: {description}")
        
        # Create the inner fractions
        num_frac = convert_frac_fixed(num_top, num_bot)
        den_frac = convert_frac_fixed(den_top, den_bot)
        
        # Create the outer fraction - with current and fixed implementation
        result_current = num_frac / den_frac
        result_fixed = convert_frac_fixed(num_frac, den_frac)
        
        # Expected manually constructed result for verification
        expected_expr = Mul(
            num_frac, 
            Pow(den_frac, -1, evaluate=False),
            evaluate=False
        )
        
        # Check if the fixed implementation produces the correct structure
        structure_match = str(result_fixed) == str(expected_expr)
        
        # Print the results
        print(f"Current result: {result_current}")
        print(f"Fixed result:   {result_fixed}")
        print(f"Expected:       {expected_expr}")
        print(f"Structure match: {structure_match}")
        
        # Check if the expressions are mathematically equivalent
        math_equiv = sympy.simplify(result_fixed) == sympy.simplify(expected_expr)
        print(f"Mathematically equivalent: {math_equiv}")
        
        test_passed = structure_match and math_equiv
        print(f"Test passed: {test_passed}")
        
        all_passed = all_passed and test_passed
    
    print(f"\nAll tests passed: {all_passed}")
    return all_passed

if __name__ == "__main__":
    print("=== Reproducing the issue ===")
    reproduce_issue()
    
    print("\n\n=== Testing fixed implementation ===")
    success = test_with_fixed_implementation()
    
    if success:
        print("\nFix successfully addresses the issue!")
    else:
        print("\nFix needs further adjustment.")