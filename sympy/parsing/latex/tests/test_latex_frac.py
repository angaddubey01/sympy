"""Tests for correct parsing of nested fractions in LaTeX expressions."""

from sympy import symbols, Mul, Pow, simplify, Integer, sympify
from sympy.testing.pytest import raises, skip
from sympy.external import import_module


# Test for the antlr4 dependency
antlr4 = import_module('antlr4', warn_not_installed=True)
latex_parser = import_module(
    'sympy.parsing.latex',
    import_kwargs={'fromlist': ['parse_latex']},
    warn_not_installed=True
)


def test_nested_fractions():
    """Test correct parsing of nested fractions in LaTeX expressions."""
    if antlr4 is None or latex_parser is None:
        skip("antlr4 is not installed")
        return
        
    parse_latex = latex_parser.parse_latex
    
    # Test case: \frac{\frac{a^3+b}{c}}{\frac{1}{c^2}}
    # Should parse as ((a**3 + b)/c)/(1/(c**2))
    latex_expr = r"\frac{\frac{a^3+b}{c}}{\frac{1}{c^2}}"
    parsed = parse_latex(latex_expr)
    
    # Construct the expected expression manually
    a, b, c = symbols('a b c')
    
    # Inner fractions
    inner_num = Mul(a**3 + b, Pow(c, -1, evaluate=False), evaluate=False)
    inner_den = Mul(Integer(1), Pow(c**2, -1, evaluate=False), evaluate=False)
    
    # Full expression
    expected = Mul(inner_num, Pow(inner_den, -1, evaluate=False), evaluate=False)
    
    # Test string representation (this may vary based on the exact SymPy version)
    # We check several alternative possible correct representations
    possible_correct_reprs = [
        "((a**3 + b)/c)/(1/(c**2))",
        "((a**3 + b)/c)/((1/c**2))"
    ]
    
    assert any(str(parsed) == repr for repr in possible_correct_reprs), \
        f"Expected one of {possible_correct_reprs}, got {str(parsed)}"
    
    # Test mathematical equivalence
    assert simplify(parsed) == simplify(expected)
    assert simplify(parsed) == c * (a**3 + b)
    
    # Additional test cases
    test_cases = [
        (r"\frac{\frac{2a}{b}}{\frac{3}{c}}", "((2*a)/b)/((3/c))"),
        (r"\frac{\frac{1}{a}}{\frac{1}{b}}", "(1/a)/((1/b))")
    ]
    
    for latex, expected_repr in test_cases:
        parsed = parse_latex(latex)
        # Check either exact match or mathematical equivalence
        assert str(parsed) == expected_repr or \
            str(parsed) == expected_repr.replace("/((", "/(") or \
            str(parsed) == expected_repr.replace("))", ")")
        
        # Reconstruct and check the expected expression
        if "2*a" in expected_repr:
            expected = Mul(
                Mul(Integer(2) * a, Pow(b, -1, evaluate=False), evaluate=False),
                Pow(Mul(Integer(3), Pow(c, -1, evaluate=False), evaluate=False), -1, evaluate=False),
                evaluate=False
            )
        else:  # 1/a case
            expected = Mul(
                Mul(Integer(1), Pow(a, -1, evaluate=False), evaluate=False),
                Pow(Mul(Integer(1), Pow(b, -1, evaluate=False), evaluate=False), -1, evaluate=False),
                evaluate=False
            )
        
        assert simplify(parsed) == simplify(expected)