# List Query Language (LQL)

A small domain-specific language for **list operations, arithmetic, bitwise, and set operations**, inspired by vectorized languages. This language supports filtering, mapping, sorting, and element-wise operations on lists.

---

## **Table of Contents**

- [Features](#features)
- [Syntax](#syntax)
- [Comments](#comments)
- [List Operations](#list-operations)
- [Arithmetic & Bitwise Rules](#arithmetic--bitwise-rules)
- [Map Operation](#map-operation)
- [Filter Operation](#filter-operation)
- [Sort Operation](#sort-operation)
- [Print Statement](#print-statement)
- [Examples](#examples)

---

## **Features**

- Supports **lists of integers and floats**.
- Arithmetic operations between scalars, lists, and literal arrays.
- Element-wise **bitwise operations**.
- Set operations: `union`, `intersection`, `difference`.
- `map` and `filter` operations for functional-style list processing.
- Sorting with `asc` and `desc`.
- Special variable `$0` in map expressions to reference current element.
- Single-line comments starting with `@`.

---

## **Syntax**

### List Declaration

```lql
list name = [1, 2, 3]
```

### List Assignment

```lql
otherList = name
```

### Arithmetic / Bitwise Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Bitwise: `and`, `or`, `xor`
- Scalar-list operations allowed.
- List-list operations must have **same length**.
- List-literal operations must have **same length**.

### Set Operations

```lql
listA union listB
listA intersection listB
listA difference listB
```

- Operands must be lists of equal length.
- Produces a list of the same length.

### Map Operation

```lql
map listName $0 => expression
```

- `$0` refers to the current element.
- Expression can use arithmetic, bitwise, or scalar operations.
- Returns a new list of same length as input.

### Filter Operation

```lql
filter listName > 5
```

- Only scalar comparisons allowed: `==`, `!=`, `>`, `>=`, `<`, `<=`.
- Returns a new list with elements satisfying the condition.

### Sort Operation

```lql
sort listName asc
sort listName desc
```

- Sorts numeric lists in ascending or descending order.

### Print Statement

```lql
print listName
print mean listName
print sum listName
```

- Supports **statistical functions**: `mean`, `sum`, `median`, `variance`, `std`, `min`, `max`, `count`.

---

## **Comments**

- Use `@` for single-line comments:

```lql
list numbers = [1,2,3]   @ this is a comment
```

---

## **Rules / Semantic Constraints**

1. **Numbers**

   - Integers, floats, negative numbers supported.
   - Division `/` returns floating-point.
   - Modulus `%` is supported.

2. **Bitwise**

   - Operands are converted to integers.
   - Scalar-list and list-list element-wise operations allowed.

3. **Arithmetic / List Operations**

   - Scalar ⟷ List: element-wise arithmetic allowed.
   - List ⟷ List: lengths must match.
   - List ⟷ Literal array: lengths must match.

4. **Set Operations**

   - Lists can be of varaible length.
   - Supports `union`, `intersection`, `difference` operators.

5. **Map**

   - `$0` references the current element.
   - Result list has same length as input.

6. **Filter**

   - Scalar comparison only.
   - Resulting list may have fewer elements.

7. **Sort**

   - Only numeric lists.
   - Can sort ascending or descending.

8. **Assignment**

   - Lists assigned must respect length rules for element-wise operations.

---

## **Examples**

```lql
@ Basic list operations
list numbers = [1,2,3,4]
print sum numbers
print mean numbers

@ Filtering
list positives = filter numbers > 2
print positives

@ Mapping
list doubled = map numbers $0 => $0 * 2
print doubled

@ List arithmetic
list result = numbers + [5,6,7,8]
print result

sort result desc
print result

@ Bitwise operations
list bits = [1,2,3]
list masked = map bits $0 => $0 & 2
print masked
```
