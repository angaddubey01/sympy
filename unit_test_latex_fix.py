"""
Unit test for LaTeX fraction parsing fix.
"""
import unittest
import sympy
from sympy import symbols, Mul, Pow, Integer
from sympy.parsing.latex import parse_latex


class TestLatexFractionParsing(unittest.TestCase):
    
    def setUp(self):
        # Define symbols for testing
        self.a, self.b, self.c = symbols('a b c')
    
    def test_single_fraction(self):
        """Test basic fraction parsing"""
        try:
            expr = parse_latex(r"\frac{a}{b}")
            self.assertEqual(str(expr), "a/b")
        except ImportError:
            print("Skipping test due to missing antlr4 package")
    
    def test_nested_fraction(self):
        """Test the problematic nested fraction case"""
        try:
            # The problematic expression
            latex_expr = r"\frac{\frac{a^3+b}{c}}{\frac{1}{c^2}}"
            parsed = parse_latex(latex_expr)
            
            # Build expected expression manually
            inner_num = self.a**3 + self.b
            inner_den = self.c
            inner_frac = Mul(inner_num, Pow(inner_den, -1, evaluate=False), evaluate=False)
            
            denom_num = Integer(1)
            denom_den = self.c**2
            denom_frac = Mul(denom_num, Pow(denom_den, -1, evaluate=False), evaluate=False)
            
            expected = Mul(inner_frac, Pow(denom_frac, -1, evaluate=False), evaluate=False)
            
            # Check string representation
            parsed_str = str(parsed)
            expected_str = str(expected)
            
            print(f"Parsed:   {parsed_str}")
            print(f"Expected: {expected_str}")
            
            # Simple test to see if it contains the expected structure
            self.assertIn("((a**3 + b)/c)", parsed_str)
            self.assertIn("(1/c**2)", parsed_str)
            
            # Check algebraic equivalence
            simplified_parsed = sympy.simplify(parsed)
            simplified_expected = sympy.simplify(expected)
            self.assertTrue(simplified_parsed.equals(simplified_expected))
        
        except ImportError:
            print("Skipping test due to missing antlr4 package")


if __name__ == "__main__":
    unittest.main()