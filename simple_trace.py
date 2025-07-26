import sys
sys.path.append('/home/yashpal/Music/code/sympy/sympy')

from sympy import *
from sympy.abc import k, n

# Test the step-by-step process
print("=== Tracing Product(k + 5, (k, 1, n)) ===")

# Given
term = k + 5
a, b = 1, n
print(f"term = {term}")
print(f"limits = (k, {a}, {b})")
print(f"term.is_Add = {term.is_Add}")
print()

# Step 1: as_numer_denom
print("Step 1: p, q = term.as_numer_denom()")
p, q = term.as_numer_denom()
print(f"p = {p}")
print(f"q = {q}")
print(f"q.is_Number = {q.is_Number}")
print()

# Step 2: What as_coeff_Add returns
print("Step 2: p.as_coeff_Add()")
coeff_add = p.as_coeff_Add()
print(f"p.as_coeff_Add() = {coeff_add}")
print()

# Step 3: Verify with actual SymPy result
print("Step 3: Actual SymPy calculation")
result = Product(k + 5, (k, 1, n)).doit()
print(f"Product(k + 5, (k, 1, n)).doit() = {result}")
