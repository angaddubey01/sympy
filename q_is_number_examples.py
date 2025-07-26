from sympy import *
from sympy.abc import n, k

print("Examples where q.is_Number becomes True in _eval_product:")
print("=" * 60)

# Example 1: Simple addition with constant term
print("Example 1: Product(k + 5, (k, 1, n))")
expr1 = Product(k + 5, (k, 1, n))
print(f"Expression: {expr1}")
# as_numer_denom() gives: p = k + 5, q = 1
# q = 1 is a Number, so q.is_Number = True
result1 = expr1.doit()
print(f"Result: {result1}")
print()

# Example 2: Addition with rational constant
print("Example 2: Product(k + Rational(3,2), (k, 1, n))")
expr2 = Product(k + Rational(3,2), (k, 1, n))
print(f"Expression: {expr2}")
# as_numer_denom() gives: p = k + 3/2, q = 1
# q = 1 is a Number, so q.is_Number = True
result2 = expr2.doit()
print(f"Result: {result2}")
print()

# Example 3: Addition with multiple constant terms
print("Example 3: Product(k + 2 + sqrt(3), (k, 1, n))")
expr3 = Product(k + 2 + sqrt(3), (k, 1, n))
print(f"Expression: {expr3}")
# as_numer_denom() gives: p = k + 2 + sqrt(3), q = 1
# q = 1 is a Number, so q.is_Number = True
result3 = expr3.doit()
print(f"Result: {result3}")
print()

# Example 4: Product with symbolic constant (not depending on k)
print("Example 4: Product(k + n, (k, 1, 5))")  # n is constant w.r.t. k
expr4 = Product(k + n, (k, 1, 5))
print(f"Expression: {expr4}")
# as_numer_denom() gives: p = k + n, q = 1
# q = 1 is a Number, so q.is_Number = True
result4 = expr4.doit()
print(f"Result: {result4}")
print()

# Example 5: Sum of polynomial terms
print("Example 5: Product(k**2 + 3*k + 7, (k, 1, n))")
expr5 = Product(k**2 + 3*k + 7, (k, 1, n))
print(f"Expression: {expr5}")
# as_numer_denom() gives: p = k**2 + 3*k + 7, q = 1
# q = 1 is a Number, so q.is_Number = True
result5 = expr5.doit()
print(f"Result: {result5}")
print()

# Example 6: Complex addition
print("Example 6: Product(k + I, (k, 1, n))")
expr6 = Product(k + I, (k, 1, n))
print(f"Expression: {expr6}")
# as_numer_denom() gives: p = k + I, q = 1
# q = 1 is a Number, so q.is_Number = True
result6 = expr6.doit()
print(f"Result: {result6}")
print()

print("Counter-examples where q.is_Number is False:")
print("=" * 45)

# Counter-example 1: Your original example
print("Counter-example 1: Product(n + 1/2**k, (k, 0, n-1))")
expr_counter1 = Product(n + 1/2**k, (k, 0, n-1))
print(f"Expression: {expr_counter1}")
# as_numer_denom() gives: p = 2**k*n + 1, q = 2**k
# q = 2**k depends on k, so q.is_Number = False
result_counter1 = expr_counter1.doit()
print(f"Result: {result_counter1}")
print()

# Counter-example 2: Fraction with variable denominator
print("Counter-example 2: Product(1 + k/n, (k, 1, 5))")
expr_counter2 = Product(1 + k/n, (k, 1, 5))
print(f"Expression: {expr_counter2}")
# as_numer_denom() gives: p = n + k, q = n
# q = n depends on n (not constant), so q.is_Number = False
result_counter2 = expr_counter2.doit()
print(f"Result: {result_counter2}")
print()

# Let's test the as_numer_denom behavior directly
print("Direct testing of as_numer_denom():")
print("=" * 35)

test_exprs = [
    k + 5,           # Simple addition
    k**2 + 3*k + 7,  # Polynomial
    k + n,           # With parameter
    n + 1/2**k,      # Your example
    1 + k/n,         # Fraction
]

for expr in test_exprs:
    p, q = expr.as_numer_denom()
    print(f"expr = {expr}")
    print(f"  p = {p}, q = {q}")
    print(f"  q.is_Number = {q.is_Number}")
    print()
