📘 Three-Address Code (TAC) Generator Documentation

The TAC Generator transforms the validated Abstract Syntax Tree (AST) into a low-level, intermediate representation known as Three-Address Code (TAC).
This IR is used later by the interpreter or backend to execute operations efficiently.

# 🔹 1. Overview

The TAC Generator performs the following tasks:

✔ Walks the AST
✔ Converts high-level constructs into TAC instructions
✔ Uses temporary variables (t1, t2, …) for intermediate results
✔ Produces a linear list of executable low-level instructions

It follows the Visitor Pattern, generating TAC based on each AST node type.

# 🔹 2. Internal State

### ✔ Instruction List

self.instructions = []

Stores TAC as tuples such as:

('FILTER', t1, 'x', '>', 5)

✔ Temporary Variable Counter
self.temp_count = 0

✔ Temporary Generator
def new_temp(self):
return f"t{self.temp_count+1}"

# 🔹 3. TAC Generation Entry Point

def generate(self, ast):
for node in ast:
self.visit(node)
return self.instructions

Walks the entire AST and emits TAC instructions.

# 🔹 4. Visitor Dispatcher

def visit(self, node):
if isinstance(node, ListDecl): return self.visit_ListDecl(node)
if isinstance(node, FilterStmt): return self.visit_FilterStmt(node)
if isinstance(node, SortStmt): return self.visit_SortStmt(node)
...

This dynamic dispatch calls the appropriate method for each node type.

# 🔹 5. TAC Handlers for Each AST Node

Below are all operations supported, along with the TAC they generate.

## 📌 5.1 List Declaration

list x = <source>

TAC:

('LIST', name, evaluated_source)

Example:

('LIST', 'x', [1,2,3])

## 📌 5.2 Filter Statement

filter x > 5

TAC:

('FILTER', t1, 'x', '>', 5)

t1 is the resulting filtered list.

## 📌 5.3 Sort Statement

sort x asc

TAC:

('SORT', 'x', 'asc')

Sorting happens in-place.

## 📌 5.4 Map Statement

map x $0 => $0 \* 2

Steps:

Convert $0 \* 2 to Python code:

(x \* 2)

Emit TAC:

('MAP', t1, 'x', '(x \* 2)')

## 📌 5.5 Statistical Operations

mean x

TAC:

('STAT', t1, 'mean', 'x')

Where t1 stores the computed value.

## 📌 5.6 Print Statement

✔ Printing a list:
print x

TAC:

('PRINT', 'x')

✔ Printing a statistic:
print mean x

TAC:

('STAT', t1, 'mean', 'x')
('PRINT', t1)

## 📌 5.7 Set Operations

x union y

TAC:

('SETOP', t1, 'union', 'x', 'y')

Supports:

union

intersection

difference

## 📌 5.8 List Arithmetic Operations

Examples:

x + y
a \* 2
(x + y) % 3

TAC format:

('LISTOP', t1, op, left, right)

Example:

('LISTOP', t2, '+', 'x', 'y')

# 🔹 6. Expression Handling in Map

Map expressions use AST nodes:

✔ Number → "5"
✔ Var ($0) → "x"
✔ UnaryOp → (-expr)
✔ BinOp → (left op right)

Logical operators are converted to Python equivalents:

LQL Python
and &
or |
xor ^

Generated strings are used inside the MAP TAC instruction.

Example AST:

$0 xor 3

Becomes:

(x ^ 3)

# 🔹 7. Utility: Pretty Printing

TACGenerator.pretty_print(tac_list)

Formats TAC like:

001: ('LIST', 'x', [1, 2, 3])
002: ('FILTER', 't1', 'x', '>', 5)
003: ('PRINT', 't1')

