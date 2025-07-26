# Matrix hstack and vstack Empty Matrix Fix

## Issue
In Sympy 1.1, there was a bug in the `row_join` method (used by `Matrix.hstack`) that incorrectly handled matrices with 0 rows. This caused `hstack` to return incorrect shapes when stacking empty matrices. 

For example:
```python
M1 = Matrix.zeros(0, 0)
M2 = Matrix.zeros(0, 1)
M3 = Matrix.zeros(0, 2)
M4 = Matrix.zeros(0, 3)
result = Matrix.hstack(M1, M2, M3, M4).shape
```

In Sympy 1.0, this correctly returned `(0, 6)`, but in Sympy 1.1 it incorrectly returned `(0, 3)`.

## Cause
The issue was introduced when the code for handling null matrices was changed from:

```python
# Original working code
if self.cols == 0 and self.rows != other.rows:
    return self._new(other.rows, 0, []).row_join(other)
```

to:

```python
# Broken code in Sympy 1.1
if not self:
    return self._new(other)
```

The problem with `if not self:` is that it doesn't properly accumulate dimensions for empty matrices. It simply returns the last matrix in the stack, losing the column counts of previous matrices.

## Fix
The issue has been fixed in Sympy 1.1.1rc1 by reverting to the original behavior:

```python
# Fixed code
if self.cols == 0 and self.rows != other.rows:
    return self._new(other.rows, 0, []).row_join(other)
```

This properly handles empty matrices by correctly accumulating the column dimensions.

## Verification
We've verified that in Sympy 1.1.1rc1, both test cases work correctly:
1. For matrices with 0 rows: `(0, 6)` is returned as expected.
2. For matrices with 1 row: `(1, 6)` is returned as expected.

This fix ensures that `hstack` behaves consistently for all matrix dimensions, including edge cases with empty matrices.