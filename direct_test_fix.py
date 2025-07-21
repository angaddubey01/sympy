"""
Direct test of the LaTeX parser fix for nested fractions.
"""
from sympy import symbols, Symbol
from sympy.parsing.latex._parse_latex_antlr import convert_frac
from sympy.core.mul import Mul
from sympy.core.power import Pow

class MockFrac:
    """Mock class to simulate the frac object from ANTLR parser."""
    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower

class MockExpr:
    """Mock class to simulate expr objects."""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Expr({self.value})"

def mock_convert_expr(expr):
    """Mock version of convert_expr function."""
    return expr.value

# Test with our modified convert_frac function
def test_convert_frac():
    """Test the convert_frac function directly."""
    # Setup symbols
    a, b, c = symbols('a b c')
    
    # Create mock objects for our test
    inner_num_expr = MockExpr(a**3 + b)
    inner_den_expr = MockExpr(c)
    inner_frac = MockFrac(inner_num_expr, inner_den_expr)
    
    outer_den_num_expr = MockExpr(1)
    outer_den_den_expr = MockExpr(c**2)
    outer_den_frac = MockFrac(outer_den_num_expr, outer_den_den_expr)
    
    # Override convert_expr for testing
    import types
    import sys
    
    # Store original
    from sympy.parsing.latex import _parse_latex_antlr
    original_convert_expr = _parse_latex_antlr.convert_expr
    
    try:
        # Replace with our mock version for testing
        _parse_latex_antlr.convert_expr = mock_convert_expr
        
        # Test our function
        result_inner_num = convert_frac(inner_frac)
        result_outer_den = convert_frac(outer_den_frac)
        
        # Build expected expression for verification
        expected_inner_num = Mul(a**3 + b, Pow(c, -1, evaluate=False), evaluate=False)
        expected_outer_den = Mul(1, Pow(c**2, -1, evaluate=False), evaluate=False)
        
        # Print results for inspection
        print("Inner numerator:")
        print(f"Result:   {result_inner_num}")
        print(f"Expected: {expected_inner_num}")
        print(f"Equal: {result_inner_num == expected_inner_num}")
        
        print("\nOuter denominator:")
        print(f"Result:   {result_outer_den}")
        print(f"Expected: {expected_outer_den}")
        print(f"Equal: {result_outer_den == expected_outer_den}")
        
    finally:
        # Restore original function
        _parse_latex_antlr.convert_expr = original_convert_expr

if __name__ == "__main__":
    print("Testing convert_frac function...")
    test_convert_frac()