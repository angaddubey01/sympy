"""
Test script for the fix of coth(log(tan(x))) issue.
"""
# Fix collections.Mapping import for Python 3.10+
import sys
import builtins
from collections import abc
sys.modules['collections'].Mapping = abc.Mapping

# Now import sympy
from sympy import *

def test_coth_log_tan():
    x = Symbol('x')
    e = coth(log(tan(x)))
    
    test_values = [2, 3, 5, 6, 8, 9, 11, 12, 13, 15, 18]
    
    print("Testing coth(log(tan(x))) for various values:")
    for val in test_values:
        try:
            result = e.subs(x, val)
            print(f"x = {val}: {result}")
        except Exception as exc:
            print(f"x = {val}: Error: {exc}")

if __name__ == "__main__":
    test_coth_log_tan()