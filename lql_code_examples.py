code = [

"""
@ TEST 0: First Test 

list data = [1, 2, 3, 4]
list big = filter data >= 3
list sq = map data $0 => $0 * $0 + (10 + 7) @ 18, 21, 26, 33
list result = sq + [5, 6, 1, 3] @ 23, 27, 27, 36
sort result desc
print result
print mean result

list union_res = data union [3,4,59,10]
print union_res

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 1: Basic List Declaration & Printing
@ Grammar: ListDecl → "list" ListIdentifier "=" "[" Array "]"
@          PrintStmt → "print" ListIdentifier
@ ──────────────────────────────────────────────────────────────────────────
list nums = [1, 2, 3, 4, 5]
print nums

list empty = []
print empty

list floats = [3.14, 2.71, 1.41, -9.8]
print floats

list negatives = [-1, -2, -3, -4]
print negatives

list mixed = [10, -5, 3.14, 0, 7.5, -2.3]
print mixed

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 2: Statistical Operations
@ Grammar: ScalarOpExpr → Operation ListIdentifier
@          Operation → "mean" | "sum" | "median" | "variance" | "std" | 
@                      "min" | "max" | "count"
@ ──────────────────────────────────────────────────────────────────────────
list stats_data = [10, 20, 30, 40, 50]
print sum stats_data
print mean stats_data
print median stats_data
print variance stats_data
print std stats_data
print min stats_data
print max stats_data
print count stats_data

"""

,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 3: Filter with All Comparison Operators
@ Grammar: FilterStmt → "filter" ListIdentifier ComparisonOp Number
@          ComparisonOp → "==" | "!=" | ">" | ">=" | "<" | "<="
@ ──────────────────────────────────────────────────────────────────────────
list values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

list gt_five = filter values > 5
print gt_five

list gte_five = filter values >= 5
print gte_five

list lt_five = filter values < 5
print lt_five

list lte_five = filter values <= 5
print lte_five

list eq_five = filter values == 5
print eq_five

list neq_five = filter values != 5
print neq_five

list decimals = filter values > 3.5
print decimals

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 4: Sort (Ascending & Descending)
@ Grammar: SortStmt → "sort" ListIdentifier ("asc" | "desc")
@ ──────────────────────────────────────────────────────────────────────────
list unsorted = [5, 2, 8, 1, 9, 3]
sort unsorted asc
print unsorted

list reverse_sort = [5, 2, 8, 1, 9, 3]
sort reverse_sort desc
print reverse_sort

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 5: Map with Expression Precedence
@ Grammar: MapStmt → "map" ListIdentifier "$0" "=>" Expr
@          Expr → OrExpr
@          Primary → Number | "$0" | "(" Expr ")" | "-" Primary
@ ──────────────────────────────────────────────────────────────────────────
list base = [1, 2, 3, 4, 5]

@ Simple arithmetic
list squared = map base $0 => $0 * $0
print squared

list doubled = map base $0 => $0 * 2
print doubled

list incremented = map base $0 => $0 + 10
print incremented

@ Unary minus
list negated = map base $0 => -$0
print negated

@ Complex expression with parentheses
list complex = map base $0 => ($0 + 5) * 2
print complex

@ Multiple operations with precedence
list precedence = map base $0 => $0 * 2 + 3
print precedence

@ Nested parentheses
list nested = map base $0 => (($0 + 1) * 2) - 3
print nested

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 6: Map with Bitwise Operations (and, or, xor)
@ Grammar: OrExpr → XorExpr ( "or" XorExpr )*
@          XorExpr → AndExpr ( "xor" AndExpr )*
@          AndExpr → AddExpr ( "and" AddExpr )*
@ ──────────────────────────────────────────────────────────────────────────
list bits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 255]

@ Bitwise AND
list masked = map bits $0 => $0 and 3
print masked

@ Bitwise OR
list set_bits = map bits $0 => $0 or 8
print set_bits

@ Bitwise XOR
list toggled = map bits $0 => $0 xor 1
print toggled

@ Combined bitwise operations with precedence
list bitwise_combo = map bits $0 => $0 and 7 or 8
print bitwise_combo

@ Complex bitwise expression
list complex_bits = map bits $0 => ($0 and 15) xor 7
print complex_bits

@ All three bitwise operators
list all_bitwise = map bits $0 => $0 and 12 xor 5 or 2
print all_bitwise

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 7: Map with Mixed Arithmetic and Bitwise
@ Tests full expression precedence hierarchy
@ ──────────────────────────────────────────────────────────────────────────
list mixed_ops = [1, 2, 4, 8, 16]

@ Multiplication has higher precedence than addition
list arith_precedence = map mixed_ops $0 => $0 + $0 * 2
print arith_precedence

@ Bitwise AND has lower precedence than multiplication
list mixed_precedence = map mixed_ops $0 => $0 * 2 and 7
print mixed_precedence

@ Full precedence test: mul, add, and, xor, or
list full_precedence = map mixed_ops $0 => $0 * 2 + 1 and 15 xor 3 or 1
print full_precedence

@ With parentheses to override precedence
list override = map mixed_ops $0 => ($0 + 1) * (2 and 3)
print override
"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 8: Set Operations
@ Grammar: SetStmt → ListIdentifier SetOperator ListIdentifier
@          SetOperator → "union" | "intersection" | "difference"
@ ──────────────────────────────────────────────────────────────────────────
list set_a = [1, 2, 3, 4, 5]
list set_b = [4, 5, 6, 7, 8]

list union_ab = set_a union set_b
print union_ab

list intersection_ab = set_a intersection set_b
print intersection_ab

list diff_ab = set_a difference set_b
print diff_ab

@ With duplicates
list dupes_a = [1, 1, 2, 2, 3, 3]
list dupes_b = [2, 2, 3, 3, 4, 4]

list union_dupes = dupes_a union dupes_b
print union_dupes

"""

,


"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 9: List Operations with Precedence
@ Grammar: ListOpStmt → ListOrExpr
@          ListOrExpr → ListXorExpr ( "or" ListXorExpr )*
@          ListXorExpr → ListAndExpr ( "xor" ListAndExpr )*
@          ListAndExpr → ListAddExpr ( "and" ListAddExpr )*
@          ListAddExpr → ListMulExpr ( ("+" | "-") MulExpr )*
@          ListMulExpr → ListPrimary ( ("*" | "/") ListPrimary )*
@ ──────────────────────────────────────────────────────────────────────────
list a = [1, 2, 3, 4]
list b = [10, 20, 30, 40]
list c = [2, 2, 2, 2]

@ Arithmetic operations
list add_result = a + b
print add_result

list sub_result = b - a
print sub_result

list mul_result = a * c
print mul_result

list div_result = b / c
print div_result

@ Precedence: multiplication before addition
list precedence1 = a + b * c
print precedence1

@ Precedence: division before subtraction
list precedence2 = b - a / c
print precedence2

@ Bitwise list operations
list and_result = a and b
print and_result

list or_result = a or b
print or_result

list xor_result = a xor b
print xor_result

@ Full precedence: or < xor < and < +- < */
list full_list_precedence = a + b * c and b or a
print full_list_precedence

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 10: List Operations with Scalars (Broadcasting)
@ Grammar: ListPrimary → ListIdentifier | Number | "[" Array "]"
@ ──────────────────────────────────────────────────────────────────────────
list broadcast_base = [1, 2, 3, 4, 5]

@ Scalar addition
list scalar_add = broadcast_base + 10
print scalar_add

@ Scalar multiplication
list scalar_mul = broadcast_base * 3
print scalar_mul

@ Scalar bitwise operations
list scalar_and = broadcast_base and 1
print scalar_and

list scalar_or = broadcast_base or 8
print scalar_or

@ Mixed: list + scalar with precedence
list mixed_scalar = broadcast_base * 2 + 5
print mixed_scalar

"""
,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 11: List Operations with Literal Arrays
@ Grammar: ListPrimary → "[" Array "]"
@ ──────────────────────────────────────────────────────────────────────────
list literal_base = [1, 2, 3]

list literal_add = literal_base + [10, 20, 30]
print literal_add

list literal_mul = literal_base * [2, 3, 4]
print literal_mul

@ Direct operation with two literal arrays
list two_literals = [1, 2, 3] + [4, 5, 6]
print two_literals
"""

,

"""


@ ──────────────────────────────────────────────────────────────────────────
@ TEST 12: Parenthesized List Operations
@ Grammar: ListPrimary → "(" ListOpStmt ")"
@ ──────────────────────────────────────────────────────────────────────────
list paren_a = [1, 2, 3, 4]
list paren_b = [2, 2, 2, 2]
list paren_c = [10, 10, 10, 10]

@ Without parentheses: a + b * c = a + (b * c)
list no_paren = paren_a + paren_b * paren_c
print no_paren

@ With parentheses: (a + b) * c
list with_paren = (paren_a + paren_b) * paren_c
print with_paren

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 13: Chained List Declarations
@ Grammar: ListSource → FilterStmt | MapStmt | SetStmt | ListOpStmt
@ ──────────────────────────────────────────────────────────────────────────
list chain_start = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@ Filter as source
list chain_filtered = filter chain_start > 5
print chain_filtered

@ Map as source
list chain_mapped = map chain_filtered $0 => $0 * 2
print chain_mapped

@ ListOp as source
list chain_added = chain_mapped + [100, 200, 300, 400, 400]
print chain_added

@ Sort the result
sort chain_added desc
print chain_added

@ Set operation as source
list chain_set = chain_filtered union chain_mapped
print chain_set

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 14: Complex Nested Expressions in Map
@ Tests deep nesting and all operators
@ ──────────────────────────────────────────────────────────────────────────
list nest_base = [1, 2, 3, 4, 5]

@ Deep arithmetic nesting
list deep_nest = map nest_base $0 => ((($0 + 1) * 2) - 3) / 4
print deep_nest

@ Deep bitwise nesting
list deep_bitwise = map nest_base $0 => (($0 and 7) or 8) xor 15
print deep_bitwise

@ Mixed arithmetic and bitwise with multiple levels
list ultimate = map nest_base $0 => (($0 * 2 + 3) and 31) or (($0 - 1) xor 7)
print ultimate

"""

,

"""

@ ──────────────────────────────────────────────────────────────────────────
@ TEST 15: Edge Cases
@ ──────────────────────────────────────────────────────────────────────────

@ Empty list operations
list empty1 = []
list empty2 = []
list empty_union = empty1 union empty2
print empty_union
print count empty_union

@ Single element
list single = [42]
print single
list single_squared = map single $0 => $0 * $0
print single_squared

@ Large numbers
list large = [1000000, 2000000, 3000000]
print sum large
print mean large

@ Decimal precision
list precise = [0.1, 0.2, 0.3]
print sum precise

@ Negative numbers in all contexts
list all_negative = [-1, -2, -3, -4, -5]
list negative_filter = filter all_negative > -3
print negative_filter

list negative_map = map all_negative $0 => -$0
print negative_map

@ Zero in operations
list with_zeros = [0, 1, 0, 2, 0, 3]
list zero_filter = filter with_zeros != 0
print zero_filter

list zero_ops = with_zeros + 5
print zero_ops

"""

,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 16: Real-World Use Cases
@ ──────────────────────────────────────────────────────────────────────────

@ Data analysis pipeline
list temperatures = [72, 68, 75, 80, 85, 90, 88, 82, 79, 73]
list hot_days = filter temperatures >= 80
print count hot_days
print mean hot_days
print max hot_days

@ Normalization (scale to 0-1 range)
list scores = [50, 75, 100, 25, 80]
list normalized = map scores $0 => $0 / 100
print normalized

@ Bit manipulation for flags
list permissions = [0, 1, 2, 3, 4, 5, 6, 7]
list read_perm = map permissions $0 => $0 and 1
list write_perm = map permissions $0 => ($0 and 2) / 2
print read_perm
print write_perm

@ Set operations for data deduplication
list dataset1 = [1, 2, 3, 4, 5, 5, 5]
list dataset2 = [4, 5, 6, 7, 8, 8, 8]
list unique_all = dataset1 union dataset2
list common = dataset1 intersection dataset2
list exclusive = dataset1 difference dataset2
print unique_all
print common
print exclusive

@ Multi-step transformation
list raw_data = [10, 20, 30, 40, 50]
list filtered_data = filter raw_data >= 25
list transformed = map filtered_data $0 => ($0 - 20) * 2
list final = transformed + [100, 200, 300]
sort final asc
print final
print median final
print std final
"""

,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 17: Operator Precedence Validation
@ Explicit tests for correct precedence parsing
@ ──────────────────────────────────────────────────────────────────────────
list prec = [5, 10, 15, 20]

@ Mul before Add: 5 + 10 * 2 = 5 + 20 = 25
list test1 = map prec $0 => $0 + $0 * 2
print test1

@ And before Or: 5 or 3 and 1 = 5 or (3 and 1) = 5 or 1
list test2 = map prec $0 => $0 or 3 and 1
print test2

@ Xor between And and Or: 5 and 3 xor 1 or 2 = (5 and 3) xor 1 or 2
list test3 = map prec $0 => $0 and 3 xor 1 or 2
print test3

@ Division before subtraction: 20 - 10 / 2 = 20 - 5 = 15
list test4 = map prec $0 => $0 - $0 / 2
print test4
"""

,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 18: ListSource Combinations
@ All possible ways to create a list
@ ──────────────────────────────────────────────────────────────────────────

@ From literal array
list from_literal = [100, 200, 300]
print from_literal

@ From another list
list from_list = from_literal
print from_list

@ From filter
list from_filter = filter from_literal > 150
print from_filter

@ From map
list from_map = map from_literal $0 => $0 / 10
print from_map

@ From set operation
list set1 = [1, 2, 3]
list set2 = [2, 3, 4]
list from_set = set1 union set2
print from_set

@ From list operation
list op1 = [1, 2, 3]
list op2 = [10, 20, 30]
list from_listop = op1 + op2
print from_listop
"""
,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 19: Kitchen Sink
@ Everything together in one complex program
@ ──────────────────────────────────────────────────────────────────────────
list kitchen_sink = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
list filtered = filter kitchen_sink >= 5
list mapped = map filtered $0 => ($0 * 2.0 + 3.0) and 31.0
list combined = mapped + [100, 200, 1, 1, 1, 1, 1, 1, 1, 1, 1] * 2
list others = [50, 60, 70]
list final_result = combined union others
sort final_result desc
print final_result
print mean final_result
print count final_result
"""
,

"""
@ ──────────────────────────────────────────────────────────────────────────
@ TEST 20: 
@ Testing MOD operator
@ ──────────────────────────────────────────────────────────────────────────

list l1 = [2,4,5,6]
list modList = l1 % 2
print modList

list l2 = [3,3]
list res = l1 union l2

print res

"""

]