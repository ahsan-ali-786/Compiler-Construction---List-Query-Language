📘 Executor Module Documentation

The Executor is the final phase of the compiler pipeline.
It takes optimized Three-Address Code (TAC) as input and executes each instruction sequentially.
The Executor maintains a runtime memory environment, where lists, temporaries, and scalars are stored.

# 🔹 1. Overview

The Executor:

Interprets TAC instructions

Manages runtime memory (variables, lists, temps)

Performs element-wise operations

Executes statistical, set, and map operations

Handles printing and safe expression evaluation

The execution model is deterministic and sequential: each TAC instruction is executed in order.

# 🔹 2. Runtime Memory

A Python dictionary represents memory:

self.memory = {
"list1": [1,2,3],
"t1": [filtered results],
"x": 12,
...
}

Memory can be pre-initialized using a symbol_table, useful for REPL or testing.

# 🔹 3. Main Execution Loop

The run() function dispatches each TAC instruction:

def run(self):
for instr in self.tac:
match instr[0]:
LIST → exec_list
FILTER → exec_filter
SORT → exec_sort
MAP → exec_map
STAT → exec_stat
SETOP → exec_setop
LISTOP → exec_listop
COPY → exec_copy
PRINT → exec_print

Execution ends with the complete memory snapshot returned.

# 🔹 4. Instruction Executors

4.1 LIST

Handles:

Literal lists

Identifiers (copy references)

Scalars → converted into single-element lists

('LIST', name, source)

Example:

LIST x [1,2,3] → memory[x] = [1,2,3]
LIST y x → memory[y] = memory[x]
LIST z 5 → memory[z] = [5]

4.2 FILTER
('FILTER', dest, src, op, value)

Filters elements using comparison operators:

Operator Meaning

>     Greater than
>
> < Less than
> = Greater equal
> <= Less equal
> == Equality
> != Not equal

Result stored in dest.

4.3 SORT
('SORT', name, order)

Sorts list in-place.

Supported orders: asc, desc.

4.4 MAP
('MAP', dest, src, expr_code)

Performs mapping over each element using a safe eval of the expression.

Expression Format:

Uses x as variable placeholder

Safe builtins only (abs, min, max, int, float)

Prevents arbitrary code execution

Example:

MAP t1 nums "(x \* 2) + 5"

4.5 STAT

Applies statistical functions:

('STAT', dest, func, list)

Supported:

Function Description
sum Sum of list
mean Average
min Minimum
max Maximum
count Number of elements
median Middle value
variance Average squared deviation
std Standard deviation

Count & sum work on empty lists; others error.

4.6 SETOP
('SETOP', dest, op, left, right)

Supports:

Operation Description
union Combine sets, preserve order
intersection Elements present in both
difference left minus right
4.7 LISTOP
('LISTOP', dest, op, left, right)

Performs element-wise operations with broadcasting:

Supported operators

- addition

* subtraction

- multiplication

/ division

% modulo

and bitwise AND

or bitwise OR

xor bitwise XOR

Broadcasting Rules

scalar + list → replicate scalar

list + scalar → replicate scalar

list + list (same length)

Errors on size mismatch.

4.8 COPY
('COPY', dest, src)

Copies lists, scalars, or identifiers.
Used heavily after optimization.

4.9 PRINT

Prints values from memory.

Supports:

lists

scalars (from STAT)

errors if identifier not found

# 🔹 5. Helper Functions

get_list()

Ensures the operand becomes a list:

identifier → memory lookup

scalar → single-element list

literal list → returned directly

get_operand()

Fetches:

scalar

list

variable reference

element_wise_op()

Handles binary operations with broadcasting.

eval_condition()

Compares values for filter operations.

compute_stat()

Computes all supported statistical results.

set_operation()

Performs union / intersection / difference.

# 🔹 6. Memory Dump Utility

dump_memory() prints all stored variables for debugging.

Example output:

MEMORY DUMP 
- a = [1, 3, 5]
- b = [2, 4, 6]
- t1 = [3, 7]
- mean_val = 5.0
