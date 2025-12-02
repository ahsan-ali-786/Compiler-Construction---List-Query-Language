📘 AST Nodes & Parser Documentation

This section documents the Abstract Syntax Tree (AST) node classes and the Recursive Descent Parser used in the List Query Language (LQL).

# 🔹 1. AST Node Definitions

The AST represents the structure of the program after parsing.
Each class corresponds to a specific syntactic construct in the language.

## 📌 1.1 List Declaration
class ListDecl:
    name: str          # List identifier
    source: Any        # List source (array, identifier, filter, map, list-op)


Used for:

list x = [1,2,3]
list y = filter x > 5

## 📌 1.2 Filter Statement
class FilterStmt:
    list_name: str     # Target list
    op: str            # Comparison operator
    value: float       # Numeric value


Represents:

filter x > 5

## 📌 1.3 Sort Statement
class SortStmt:
    list_name: str
    order: str         # asc / desc


Example:

sort x asc

## 📌 1.4 Map Statement
class MapStmt:
    list_name: str
    expr: AST          # Expression using $0


Example:

map x $0 => $0 * 2

## 📌 1.5 Set Operation
class SetOpStmt:
    left: Any          # List or subexpression
    op: str            # union / intersection / difference
    right: Any


Example:

x union y

## 📌 1.6 List Operation
class ListOpStmt:
    left: Any
    op: str            # + - * / % and or xor
    right: Any


Examples:

x + y
(x * 2) and y

## 📌 1.7 Statistical Operation
class StatStmt:
    func: str          # mean, sum, min, max, ...
    list_name: str


Example:

mean x

## 📌 1.8 Print Statement
class PrintStmt:
    target: Any        # list identifier OR StatStmt


Example:

print x
print mean y

## 📌 1.9 Expression Nodes

Binary, unary, numeric, and variable nodes used in map expressions.

✔ Binary Operation
class BinOp:
    left
    op: str
    right

✔ Unary Operation
class UnaryOp:
    op: str            # '-'
    expr

✔ Number Literal
class Number:
    value: float

✔ Variable
class Var:
    name: str          # Only "$0"

# 🔹 2. Parser Overview

This parser is a handwritten Recursive Descent Parser.
It reads tokens and produces the AST defined above.

## 📌 2.1 Token Navigation Helpers
current()

Returns the current token.

advance()

Moves to the next token.

expect(kind, value=None)

Consumes a token and ensures it matches the expected type/value.

accept(kind, value=None)

Consumes a token only if it matches, otherwise returns None.

## 🔹 2.2 Parsing Entry Point
### ✔ parse()
def parse(self):
    stmts = []
    while self.current().type != 'EOF':
        stmts.append(self.statement())
    return stmts


Parses a list of statements until EOF.

## 🔹 2.3 Statement Parsing
✔ List Declaration
list x = ...

✔ Sort Statement
sort x asc

✔ Print Statement
print x


Invalid standalone identifiers cause:

Error: Unexpected identifier at statement level

## 🔹 2.4 List Declaration & Source
✔ list_decl()

Parses:

list x = <source>

✔ list_source()

Determines whether the source is:

filter statement

map statement

list/set operation expression

## 🔹 2.5 List Operation Grammar (with Precedence)

The following functions implement operator precedence:

Level	Function	Operators
1	list_or_expr()	or
2	list_xor_expr()	xor
3	list_and_expr()	and
4	list_add_expr()	+ -
5	list_mul_expr()	* / %
6	list_primary()	literals, identifiers, arrays

This forms a Pratt-style recursive descent precedence parser.

## 🔹 2.6 List Primary Parsing

Handles:

✔ Parenthesized expressions

( x + y )

✔ Array literals

[1,2,3]

✔ Scalar numbers

5

✔ List identifiers

x

✔ Set ops
x union y
x intersection y
x difference y

## 🔹 2.7 Filter Parsing
filter x > 3


Produces:

FilterStmt(name, op, value)

## 🔹 2.8 Sort Parsing
sort x asc


Produces:

SortStmt(name, "asc")

## 🔹 2.9 Map Parsing
map x $0 => <expression>


Uses full expression parser for RHS.

## 🔹 2.10 Print Parsing

Two valid forms:

print x
print mean x


Internally creates:

PrintStmt(StatStmt(...))


or

PrintStmt("x")

## 🔹 2.11 Expression Parser (Used Only in map)

This is a second precedence-based parser:

Precedence Level	Function	Operators
1	or_expr()	or
2	xor_expr()	xor
3	and_expr()	and
4	add_expr()	+ -
5	mul_expr()	* / %
6	primary()	$0, number, unary -, (...)

Primary handles:

number literals

$0 variable

unary minus

parentheses

Produces:

Number

Var

UnaryOp

BinOp

🟦 Summary Diagram
Program
 └── Statements
      ├── ListDecl
      ├── FilterStmt
      ├── SortStmt
      ├── MapStmt
      ├── PrintStmt
      ├── SetOpStmt
      └── ListOpStmt


Expression trees:

Expr
 ├── BinOp
 ├── UnaryOp
 ├── Number
 └── Var ($0)