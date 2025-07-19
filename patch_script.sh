#!/bin/bash
# Run these below command in the terminal and stop and tell me if any error occurs or any command is not get executed successfully

set -e  # Stop on error

# Variables
suffix=D09_24066
Last_Hash=4d786a2a07d22cd4e380ed8e4579fcec1ce24a16

# Patch functions
apply_patchA() {
  echo ">>> Applying patch A"
(
  cd "$(git rev-parse --show-toplevel)"
  git apply --3way <<'EOF'
diff --git a/sympy/physics/units/unitsystem.py b/sympy/physics/units/unitsystem.py
index 3daf84c108..c368430bca 100644
--- a/sympy/physics/units/unitsystem.py
+++ b/sympy/physics/units/unitsystem.py
@@ -190,10 +190,23 @@ def _collect_factor_and_dimension(self, expr):
                 dim /= idim**count
             return factor, dim
         elif isinstance(expr, Function):
-            fds = [self._collect_factor_and_dimension(
-                arg) for arg in expr.args]
-            return (expr.func(*(f[0] for f in fds)),
-                    *(d[1] for d in fds))
+            # Generic functions: apply to the argument factors and propagate dimensions,
+            # but collapse dimensionless results to Dimension(1).
+            fds = [self._collect_factor_and_dimension(arg) for arg in expr.args]
+            # build factor by applying function to the factors of the arguments
+            factor = expr.func(*(f[0] for f in fds))
+            # extract argument dimensions
+            arg_dims = [d for (_, d) in fds]
+            # single-argument functions: result dimension equals argument dimension,
+            # collapse to dimensionless if appropriate
+            if len(arg_dims) == 1:
+                dim = arg_dims[0]
+                if self.get_dimension_system().is_dimensionless(dim):
+                    dim = Dimension(1)
+            else:
+                # multi-argument functions: keep tuple of argument dimensions
+                dim = arg_dims
+            return factor, dim
         elif isinstance(expr, Dimension):
             return S.One, expr
         else:
EOF
)
}

apply_patchB() {
  echo ">>> Applying patch B"
(
  cd "$(git rev-parse --show-toplevel)"
  git apply --3way <<'EOF'
diff --git a/sympy/physics/units/tests/test_quantities.py b/sympy/physics/units/tests/test_quantities.py
index 25a68c7be5..a327da04cb 100644
--- a/sympy/physics/units/tests/test_quantities.py
+++ b/sympy/physics/units/tests/test_quantities.py
@@ -553,6 +553,38 @@ def test_prefixed_property():
     assert kilogram.is_prefixed
     assert pebibyte.is_prefixed
 
+def test_dimensionless_functions():
+    """Test that functions of dimensionless quantities are handled correctly."""
+    from sympy.core.singleton import S
+    from sympy.physics.units.definitions import second, ohm, farad
+    
+    # Test second/(ohm*farad) which should be dimensionless
+    expr = second / (ohm * farad)
+    dim = SI._collect_factor_and_dimension(expr)[1]
+    assert SI.get_dimension_system().is_dimensionless(dim)
+    
+    # Test that exp of a dimensionless quantity is dimensionless
+    exp_expr = exp(expr)
+    exp_factor, exp_dim = SI._collect_factor_and_dimension(exp_expr)
+    assert SI.get_dimension_system().is_dimensionless(exp_dim)
+    
+    # Test that a scalar + exp of a dimensionless quantity is dimensionless
+    buggy_expr = 100 + exp(expr)
+    buggy_factor, buggy_dim = SI._collect_factor_and_dimension(buggy_expr)
+    assert SI.get_dimension_system().is_dimensionless(buggy_dim)
+    assert buggy_factor == 100 + S.Exp1
+    assert buggy_dim == Dimension(1)
+    
+    # Test other transcendental functions
+    log_expr = log(expr)
+    log_factor, log_dim = SI._collect_factor_and_dimension(log_expr)
+    assert SI.get_dimension_system().is_dimensionless(log_dim)
+    
+    sin_expr = sin(expr)
+    sin_factor, sin_dim = SI._collect_factor_and_dimension(sin_expr)
+    assert SI.get_dimension_system().is_dimensionless(sin_dim)
+
+
 def test_physics_constant():
     from sympy.physics.units import definitions
diff --git a/sympy/physics/units/unitsystem.py b/sympy/physics/units/unitsystem.py
index 3daf84c108..c0c5414c28 100644
--- a/sympy/physics/units/unitsystem.py
+++ b/sympy/physics/units/unitsystem.py
@@ -192,6 +192,12 @@ def _collect_factor_and_dimension(self, expr):
         elif isinstance(expr, Function):
             fds = [self._collect_factor_and_dimension(
                 arg) for arg in expr.args]
+            # For transcendental functions like exp, log, sin, etc.,
+            # if all arguments are dimensionless (after checking),
+            # the function result is also dimensionless
+            if all(self.get_dimension_system().is_dimensionless(d[1]) for d in fds):
+                return expr.func(*(f[0] for f in fds)), Dimension(1)
+            # Otherwise, return the original behavior
             return (expr.func(*(f[0] for f in fds)),
                     *(d[1] for d in fds))
         elif isinstance(expr, Dimension):
EOF
)
}

# Branch names
branch_Base=Base_$suffix
branch_A=A_$suffix
branch_B=B_$suffix

echo ">>> Creating and pushing $branch_Base"
git checkout -b $branch_Base
git reset --hard $Last_Hash
PREV_HASH=$(git rev-list --parents -n 1 $Last_Hash | cut -d' ' -f2)
echo ">>> Previous hash: $PREV_HASH"
git reset --hard $PREV_HASH
git push --set-upstream origin "$branch_Base"

echo ">>> Creating and pushing $branch_A"
git checkout -b $branch_A
git reset --hard $PREV_HASH
apply_patchA
git add .
git commit -m "$branch_A"
git push --set-upstream origin "$branch_A"
git push

echo ">>> Creating and pushing $branch_B"
git checkout -b $branch_B
git reset --hard $PREV_HASH
apply_patchB
git add .
git commit -m "$branch_B"
git push --set-upstream origin "$branch_B"
git push

echo "✅ All branches created and pushed successfully."
