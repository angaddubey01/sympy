import sys
sys.path.insert(0, '/testbed/20250717/140319')
import sympy as sy
from sympy.matrices import Matrix

# Override the row_join method to simulate the broken behavior in Sympy 1.1
original_row_join = Matrix.row_join

def broken_row_join(self, other):
    """This simulates the broken version in Sympy 1.1"""
    # Broken code used "if not self:" instead of checking rows and columns
    if not self:  # This is the buggy condition
        return self._new(other)

    if self.rows != other.rows:
        raise sy.ShapeError(
            "`self` and `rhs` must have the same number of rows.")
    return self._eval_row_join(other)

# Replace the row_join method with our broken version
Matrix.row_join = broken_row_join

# Now test the broken implementation
print("Testing with the broken row_join implementation:")

# Test case with 0 rows
M1 = Matrix.zeros(0, 0)
M2 = Matrix.zeros(0, 1)
M3 = Matrix.zeros(0, 2)
M4 = Matrix.zeros(0, 3)
result = Matrix.hstack(M1, M2, M3, M4)
print("Hstack with 0 rows result shape:", result.shape)
print("Expected in broken version: (0, 3)")  # Last matrix's column count only

# Test case with 1 row
N1 = Matrix.zeros(1, 0)
N2 = Matrix.zeros(1, 1)
N3 = Matrix.zeros(1, 2)
N4 = Matrix.zeros(1, 3)
result2 = Matrix.hstack(N1, N2, N3, N4)
print("Hstack with 1 row result shape:", result2.shape)
print("Expected: (1, 6)")  # Should work fine for non-empty matrices

# Restore the original row_join method
Matrix.row_join = original_row_join