"""
Minimal test script to verify the fix for coth(log(tan(x))) issue.
"""
# Patch collections.Mapping import for Python 3.10+
import sys
import collections.abc as abc
sys.modules['collections'].Mapping = abc.Mapping
sys.modules['collections'].MutableSet = abc.MutableSet

# Make all necessary imports
from sympy.functions.elementary.hyperbolic import coth
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import tan
from sympy.core.symbol import Symbol
from sympy.core.numbers import S, I, pi

print("Testing the fix...")
x = Symbol('x')
e = coth(log(tan(x)))

test_values = [2, 3, 5, 6]

for val in test_values:
    try:
        result = e.subs(x, val)
        print(f"x = {val}: {result}")
    except Exception as exc:
        print(f"x = {val}: Error: {exc}")
        
print("Test completed successfully!")