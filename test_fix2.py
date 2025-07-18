import sympy
from sympy.printing.mathml import mathml
from sympy.printing.conventions import split_super_sub

# Test split_super_sub function with and without split_digits
print("Testing split_super_sub:")
print("split_super_sub('x2', split_digits=True) =", split_super_sub('x2', split_digits=True))
print("split_super_sub('x2', split_digits=False) =", split_super_sub('x2', split_digits=False))

# Now test the MathML printer
print("\nTesting MathML presentation printer:")
x2, y, z = sympy.symbols('x2 y z')
y_expr = x2*z+x2**3
print("\nExpression with x2:")
print(mathml(y_expr, printer='presentation'))