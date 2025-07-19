# Test script to understand the bug behavior and analyze solutions

from sympy import exp, log, sin
from sympy.physics import units
from sympy.physics.units.systems.si import SI

print("=== Testing the original bug scenario ===")

# The problematic expression
expr = units.second / (units.ohm * units.farad)
print(f"Expression: {expr}")

# Check if it's dimensionless
dim = SI._collect_factor_and_dimension(expr)[1]
print(f"Dimension: {dim}")
print(f"Is dimensionless: {SI.get_dimension_system().is_dimensionless(dim)}")

# The buggy case that should work but doesn't
print("\n=== Testing exp() of dimensionless expression ===")
try:
    buggy_expr = 100 + exp(expr)
    result = SI._collect_factor_and_dimension(buggy_expr)
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Current Function handling ===")
# Let's see what happens with just exp(expr)
try:
    exp_expr = exp(expr)
    exp_result = SI._collect_factor_and_dimension(exp_expr)
    print(f"exp({expr}) -> factor: {exp_result[0]}, dim: {exp_result[1]}")
except Exception as e:
    print(f"Error with exp: {e}")
