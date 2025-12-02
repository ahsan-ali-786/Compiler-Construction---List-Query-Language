📘 Optimizer Module Documentation

The Optimizer performs multiple optimization passes on the TAC (Three-Address Code) to reduce execution cost, remove redundancy, fold constants, and simplify expressions.
It operates over the linear TAC list and updates it in-place.

# 🔹 1. Overview

The Optimizer applies traditional compiler optimization techniques such as:

✔ Constant Folding
✔ Algebraic Simplification
✔ Strength Reduction
✔ Dead Code Elimination (DCE)
✔ Copy Propagation
✔ Redundant Operation Removal
✔ Common Subexpression Elimination (CSE)

The goal is to:

Reduce TAC size

Improve runtime efficiency

Remove unnecessary temporary variables

Simplify expressions before interpretation

# 🔹 2. Optimization Pipeline

The optimize() function orchestrates all optimization passes:

def optimize(self):
    run constant_folding()
    run algebraic_simplification()
    run strength_reduction()
    run dead_code_elimination()
    run copy_propagation()
    run remove_redundant_operations()


It executes multiple passes (max 5) until no further changes are detected, ensuring fixed-point optimization.

# 🔹 3. Constant Folding
✔ Purpose

Evaluates constant expressions at compile time instead of runtime.

✔ Applies to MAP expressions only.

Example:

map x $0 => (2 + 3)


Optimized to:

map x $0 => 5

✔ Rule

If expr_code does not contain 'x', it is safe to evaluate:

('MAP', t1, 'x', '(2 * 4)')
→
('MAP', t1, 'x', '8')

# 🔹 4. Algebraic Simplification
✔ Purpose

Simplifies arithmetic and logical operations to reduce computation.

✔ Applied to:

MAP

LISTOP

Examples of Simplifications
Expression	Optimized Result
x + 0	x
0 + x	x
x - 0	x
x * 1	x
1 * x	x
x * 0	0
x / 1	x
x % 1	0
x & 0	0
x | 0	x
x ^ 0	x

Produces TAC such as:

('COPY', dest, src)
('LIST', dest, [0])


MAP expressions undergo string rewriting using _simplify_expr().

# 🔹 5. Strength Reduction
✔ Purpose

Replace expensive operations with cheaper ones.

✔ Example Rewrites:

x * 2 → x + x

2 * x → x + x

These apply to LISTOP instructions:

('LISTOP', t2, '*', x, 2)
→
('LISTOP', t2, '+', x, x)


This reduces computational cost.

# 🔹 6. Dead Code Elimination (DCE)
✔ Purpose

Remove TAC instructions that compute values which are never used.

✔ Process

Find used variables by scanning TAC backwards

Remove instructions defining temps never referenced

Example:

t1 = FILTER x > 5
t2 = MAP t1 $0 => x * 2
PRINT t1


t2 is never used → removed.

# 🔹 7. Copy Propagation
✔ Purpose

Eliminate unnecessary temporary variables.

Given:

COPY t1, x
LISTOP t2, '+', t1, 3


After propagation:

LISTOP t2, '+', x, 3

✔ Mechanism

Builds mapping:

t1 → x


Then replaces future uses.

# 🔹 8. Redundant Operation Removal
Removes:
✔ Sequential duplicate sorts
SORT x asc
SORT x asc   ← redundant

✔ Identity copies
COPY t1, t1

✔ Self-assignments
LIST x, x


These instructions contribute nothing and are removed.

# 🔹 9. Common Subexpression Elimination (CSE)
✔ Purpose

Avoid recomputing expressions with the same operands.

Example TAC:

t1 = LISTOP '+', x, y
t2 = LISTOP '+', x, y


Optimized to:

t1 = LISTOP '+', x, y
t2 = COPY t1

✔ Key

CSE identifies repeated calculations by constructing a signature:

(opcode, operands...) → result

# 🔹 10. Utility: TAC Pretty Printer
Optimizer.pretty_print(tac)


Prints:

001: ('LIST', 'x', [1,2,3])
002: ('FILTER', 't1', 'x', '>', 5)
003: ('MAP', 't2', 't1', '(x * 2)')
...
