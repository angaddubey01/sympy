import sys
sys.path.insert(0, '/testbed/20250717/140319')
import sympy as sy

# Test case with 0 rows
M1 = sy.Matrix.zeros(0, 0)
M2 = sy.Matrix.zeros(0, 1)
M3 = sy.Matrix.zeros(0, 2)
M4 = sy.Matrix.zeros(0, 3)
result = sy.Matrix.hstack(M1, M2, M3, M4)
print("Hstack with 0 rows result shape:", result.shape)
print("Expected shape: (0, 6)")

# Test case with 1 row
N1 = sy.Matrix.zeros(1, 0)
N2 = sy.Matrix.zeros(1, 1)
N3 = sy.Matrix.zeros(1, 2)
N4 = sy.Matrix.zeros(1, 3)
result2 = sy.Matrix.hstack(N1, N2, N3, N4)
print("Hstack with 1 row result shape:", result2.shape)
print("Expected shape: (1, 6)")