📘 Semantic Analyzer – Operations & Checks

The Semantic Analyzer performs several validation steps to ensure that the program is meaningfully correct, even if it is syntactically valid.
Below is a detailed breakdown of all semantic rules enforced.

## 🔹 1. Symbol Table Management

Tracks declared variables (list identifiers).

Each entry contains:

type: "list"

declared: True

Ensures no redeclaration occurs:

list x = [1,2]
list x = [3,4] ❌ Error: redeclaration of 'x'

## 🔹 2. List Declaration Rules

For statements of the form:

list name = source

✔ Ensures the list is not already declared
✔ Validates the right-hand side source, which may be:

Literal arrays ([1,2,3])

Identifiers

Numeric scalars

Filter/Map/Set/List Operation expressions

❌ Raises an error for invalid types.

## 🔹 3. List Source Validation

Checks that the RHS of a list declaration is meaningful:

✔ Literal Array

All elements must be numeric.

✔ Identifier

Must be declared.

Must be of type list.

✔ Numeric Value

Allowed only for operations.

✔ Filter / Map / Set / List Operation

Fully visited and validated recursively.

## 🔹 4. Filter Statement Validation

Example:

filter x > 5

Checks:

x is declared

x is a list

Valid comparison operator:

== != > >= < <=

Filter value must be numeric

## 🔹 5. Sort Statement Validation

Example:

sort x asc

Checks:

x is declared

x is a list

Sort order must be:

asc
desc

## 🔹 6. Map Statement Validation

Example:

map x $0 => $0 \* 2

Checks:

The list being mapped is declared

The list is of type list

Expression on RHS must contain only:

$0 variable

numeric literals

unary -

arithmetic/boolean binary operators (+, -, \*, /, %, and, or, xor)

❌ No other variables allowed in map expressions.

## 🔹 7. Statistical Operation Validation

Examples:

mean x
sum x

Checks:

The list exists

The list is of type list

Valid functions:

mean, sum, median, variance, std,
min, max, count

## 🔹 8. Print Statement Validation

Allowed:

print x
print mean x

Checks:

If printing a list:

list must be declared

list must be of type list

If printing a statistic:

recursively validates the StatStmt

## 🔹 9. Set Operation Validation

Examples:

x union y
x intersection y
x difference y

Checks:

Both operands declared

Both operands must be lists

Valid operators:

union
intersection
difference

## 🔹 10. List Operation Validation

Examples:

x + y \* 2
(x + y) / 3

Checks:

Left & right operands must be:

declared list

numeric literal

literal array

nested list operation

Valid list operators:

- - - / % and or xor

## 🔹 11. Expression Validation (map & internal)

Ensures expressions use only allowed:

literals

$0 variable

unary -

binary operations

All operands recursively validated.

## 🔹 12. Helper Checks

✔ assert_declared(name)

Ensures variable has been declared.

✔ assert_list(name)

Ensures variable is of type "list".

Both guard against semantic misuse, such as:

sort a ❌ a not declared
mean 5 ❌ 5 is not a list
map x $0 => y ❌ y is not allowed in map expressions
