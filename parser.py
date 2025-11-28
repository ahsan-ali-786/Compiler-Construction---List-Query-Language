# from typing import List, Any

# # ================================
# # AST Nodes
# # ================================

# class ListDecl:
#     def __init__(self, name: str, source):
#         self.name = name
#         self.source = source

# class FilterStmt:
#     def __init__(self, list_name: str, op: str, value: float):
#         self.list_name = list_name
#         self.op = op
#         self.value = value

# class SortStmt:
#     def __init__(self, list_name: str, order: str):
#         self.list_name = list_name
#         self.order = order

# class MapStmt:
#     def __init__(self, list_name: str, expr):
#         self.list_name = list_name
#         self.expr = expr

# class SetOpStmt:
#     def __init__(self, left, op: str, right):
#         self.left = left
#         self.op = op
#         self.right = right

# class ListOpStmt:
#     def __init__(self, left, op: str, right):
#         self.left = left
#         self.op = op
#         self.right = right

# class StatStmt:
#     def __init__(self, func: str, list_name: str):
#         self.func = func
#         self.list_name = list_name

# class PrintStmt:
#     def __init__(self, target):
#         self.target = target

# # Expression nodes
# class BinOp:
#     def __init__(self, left, op: str, right):
#         self.left = left
#         self.op = op
#         self.right = right

# class UnaryOp:
#     def __init__(self, op: str, expr):
#         self.op = op
#         self.expr = expr

# class Number:
#     def __init__(self, value: float):
#         self.value = value

# class Var:
#     def __init__(self, name: str):
#         self.name = name


# # ================================
# # Parser
# # ================================

# class Parser:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.pos = 0

#     def current(self):
#         if self.pos < len(self.tokens):
#             return self.tokens[self.pos]
#         # Return EOF token
#         from collections import namedtuple
#         Token = namedtuple('Token', ['type', 'value', 'line', 'col'])
#         return Token('EOF', None, 0, 0)

#     def advance(self):
#         self.pos += 1

#     def expect(self, kind, value=None):
#         tok = self.current()
#         if tok.type != kind or (value is not None and tok.value != value):
#             raise SyntaxError(
#                 f"Expected {kind} {value or ''}, got {tok.type} '{tok.value}' "
#                 f"at line {tok.line}, col {tok.col}"
#             )
#         self.advance()
#         return tok

#     def accept(self, kind, value=None):
#         tok = self.current()
#         if tok.type == kind and (value is None or tok.value == value):
#             self.advance()
#             return tok
#         return None

#     # -----------------------------
#     # Main entry
#     # -----------------------------
#     def parse(self):
#         stmts = []
#         while self.current().type != 'EOF':
#             stmts.append(self.statement())
#         return stmts

#     # -----------------------------
#     # Statements
#     # -----------------------------
#     def statement(self):
#         tok = self.current()

#         # list declaration
#         if tok.type == 'KEYWORD' and tok.value == 'list':
#             return self.list_decl()

#         # sort statement
#         if tok.type == 'KEYWORD' and tok.value == 'sort':
#             return self.sort_stmt()

#         # print statement
#         if tok.type == 'KEYWORD' and tok.value == 'print':
#             return self.print_stmt()

#         # Standalone statement-level operations (shouldn't happen with new grammar)
#         # But kept for compatibility
#         if tok.type == 'ID':
#             # This would be a standalone ListOpStmt or SetStmt
#             # In the new grammar, these should only appear in ListSource
#             raise SyntaxError(
#                 f"Unexpected identifier at statement level: {tok.value} "
#                 f"at line {tok.line}. Did you mean to assign it to a list?"
#             )

#         raise SyntaxError(f"Invalid statement start: {tok.type} '{tok.value}' at line {tok.line}")

#     # -----------------------------
#     # List declaration / sources
#     # -----------------------------
#     def list_decl(self):
#         self.expect('KEYWORD', 'list')
#         name = self.expect('ID').value
#         self.expect('ASSIGN')
#         source = self.list_source()
#         return ListDecl(name, source)

#     def list_source(self):
#         tok = self.current()

#         # Check for filter statement
#         if tok.type == 'KEYWORD' and tok.value == 'filter':
#             return self.filter_stmt()

#         # Check for map statement
#         if tok.type == 'KEYWORD' and tok.value == 'map':
#             return self.map_stmt()

#         # Check for set operations or list operations
#         # These follow the ListOpStmt grammar
#         return self.list_op_stmt()

#     # -----------------------------
#     # List operations with precedence
#     # -----------------------------
#     def list_op_stmt(self):
#         """Parse list operations with proper precedence"""
#         return self.list_or_expr()

#     def list_or_expr(self):
#         node = self.list_xor_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'or':
#             self.advance()
#             right = self.list_xor_expr()
#             node = ListOpStmt(node, 'or', right)
#         return node

#     def list_xor_expr(self):
#         node = self.list_and_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'xor':
#             self.advance()
#             right = self.list_and_expr()
#             node = ListOpStmt(node, 'xor', right)
#         return node

#     def list_and_expr(self):
#         node = self.list_add_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'and':
#             self.advance()
#             right = self.list_add_expr()
#             node = ListOpStmt(node, 'and', right)
#         return node

#     def list_add_expr(self):
#         node = self.list_mul_expr()
#         while self.current().type == 'OP' and self.current().value in ('+', '-'):
#             op = self.current().value
#             self.advance()
#             right = self.list_mul_expr()
#             node = ListOpStmt(node, op, right)
#         return node

#     def list_mul_expr(self):
#         node = self.list_primary()
#         while self.current().type == 'OP' and self.current().value in ('*', '/'):
#             op = self.current().value
#             self.advance()
#             right = self.list_primary()
#             node = ListOpStmt(node, op, right)
#         return node

#     def list_primary(self):
#         """
#         ListPrimary → ListIdentifier | Number | "[" Array "]" | "(" ListOpStmt ")"
#         Also handles set operations (union, intersection, difference)
#         """
#         tok = self.current()

#         # Parenthesized list expression
#         if tok.type == 'LPAREN':
#             self.advance()
#             node = self.list_op_stmt()
#             self.expect('RPAREN')
#             return node

#         # Literal array
#         if tok.type == 'LBRACK':
#             self.advance()
#             nums = []
#             if not self.accept('RBRACK'):
#                 nums.append(float(self.expect('NUMBER').value))
#                 while self.accept('COMMA'):
#                     nums.append(float(self.expect('NUMBER').value))
#                 self.expect('RBRACK')
#             return nums

#         # Number (for scalar operations like: flags or 8)
#         if tok.type == 'NUMBER':
#             self.advance()
#             return float(tok.value)

#         # List identifier
#         if tok.type == 'ID':
#             name = tok.value
#             self.advance()
            
#             # Check for set operations
#             next_tok = self.current()
#             if next_tok.type == 'KEYWORD' and next_tok.value in ('union', 'intersection', 'difference'):
#                 op = next_tok.value
#                 self.advance()
#                 right = self.list_primary()
#                 return SetOpStmt(name, op, right)
            
#             # Otherwise just return the identifier
#             return name

#         raise SyntaxError(
#             f"Invalid list primary: {tok.type} '{tok.value}' at line {tok.line}"
#         )

#     # -----------------------------
#     # Specific statements
#     # -----------------------------
#     def filter_stmt(self):
#         self.expect('KEYWORD', 'filter')
#         name = self.expect('ID').value
#         op = self.expect('COMP').value
#         val = float(self.expect('NUMBER').value)
#         return FilterStmt(name, op, val)

#     def sort_stmt(self):
#         self.expect('KEYWORD', 'sort')
#         name = self.expect('ID').value
#         order = self.expect('KEYWORD').value  # asc / desc
#         if order not in ('asc', 'desc'):
#             raise SyntaxError(f"Sort order must be 'asc' or 'desc', got '{order}'")
#         return SortStmt(name, order)

#     def map_stmt(self):
#         self.expect('KEYWORD', 'map')
#         list_name = self.expect('ID').value
#         self.expect('DOLLAR0')
#         self.expect('ARROW')
#         expr = self.expr()
#         return MapStmt(list_name, expr)

#     def print_stmt(self):
#         self.expect('KEYWORD', 'print')
#         target = self.expression_or_list()
#         return PrintStmt(target)

#     def expression_or_list(self):
#         tok = self.current()
        
#         # Check for statistical operations
#         if tok.type == 'KEYWORD' and tok.value in (
#             'mean', 'sum', 'median', 'variance', 'std', 'min', 'max', 'count'
#         ):
#             func = tok.value
#             self.advance()
#             name = self.expect('ID').value
#             return StatStmt(func, name)
        
#         # Otherwise must be a list identifier
#         if tok.type == 'ID':
#             return self.expect('ID').value
        
#         raise SyntaxError(
#             f"Print target must be list identifier or statistical operation, "
#             f"got {tok.type} '{tok.value}' at line {tok.line}"
#         )

#     # -----------------------------
#     # Map expression parser (for $0 expressions)
#     # -----------------------------
#     def expr(self):
#         return self.or_expr()

#     def or_expr(self):
#         node = self.xor_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'or':
#             self.advance()
#             node = BinOp(node, 'or', self.xor_expr())
#         return node

#     def xor_expr(self):
#         node = self.and_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'xor':
#             self.advance()
#             node = BinOp(node, 'xor', self.and_expr())
#         return node

#     def and_expr(self):
#         node = self.add_expr()
#         while self.current().type == 'KEYWORD' and self.current().value == 'and':
#             self.advance()
#             node = BinOp(node, 'and', self.add_expr())
#         return node

#     def add_expr(self):
#         node = self.mul_expr()
#         while self.current().type == 'OP' and self.current().value in ('+', '-'):
#             op = self.current().value
#             self.advance()
#             node = BinOp(node, op, self.mul_expr())
#         return node

#     def mul_expr(self):
#         node = self.primary()
#         while self.current().type == 'OP' and self.current().value in ('*', '/'):
#             op = self.current().value
#             self.advance()
#             node = BinOp(node, op, self.primary())
#         return node

#     def primary(self):
#         tok = self.current()
        
#         # Unary minus
#         if tok.type == 'OP' and tok.value == '-':
#             self.advance()
#             return UnaryOp('-', self.primary())

#         # Number
#         if tok.type == 'NUMBER':
#             self.advance()
#             return Number(float(tok.value))

#         # $0 variable
#         if tok.type == 'DOLLAR0':
#             self.advance()
#             return Var('$0')

#         # Parenthesized expression
#         if tok.type == 'LPAREN':
#             self.advance()
#             node = self.expr()
#             self.expect('RPAREN')
#             return node

#         raise SyntaxError(
#             f"Invalid expression primary: {tok.type} '{tok.value}' at line {tok.line}"
#         )

from typing import List, Any

# ================================
# AST Nodes
# ================================

class ListDecl:
    def __init__(self, name: str, source):
        self.name = name
        self.source = source

class FilterStmt:
    def __init__(self, list_name: str, op: str, value: float):
        self.list_name = list_name
        self.op = op
        self.value = value

class SortStmt:
    def __init__(self, list_name: str, order: str):
        self.list_name = list_name
        self.order = order

class MapStmt:
    def __init__(self, list_name: str, expr):
        self.list_name = list_name
        self.expr = expr

class SetOpStmt:
    def __init__(self, left, op: str, right):
        self.left = left
        self.op = op
        self.right = right

class ListOpStmt:
    def __init__(self, left, op: str, right):
        self.left = left
        self.op = op
        self.right = right

class StatStmt:
    def __init__(self, func: str, list_name: str):
        self.func = func
        self.list_name = list_name

class PrintStmt:
    def __init__(self, target):
        self.target = target

# Expression nodes
class BinOp:
    def __init__(self, left, op: str, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp:
    def __init__(self, op: str, expr):
        self.op = op
        self.expr = expr

class Number:
    def __init__(self, value: float):
        self.value = value

class Var:
    def __init__(self, name: str):
        self.name = name


# ================================
# Parser
# ================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        # Return EOF token
        from collections import namedtuple
        Token = namedtuple('Token', ['type', 'value', 'line', 'col'])
        return Token('EOF', None, 0, 0)

    def advance(self):
        self.pos += 1

    def expect(self, kind, value=None):
        tok = self.current()
        if tok.type != kind or (value is not None and tok.value != value):
            raise SyntaxError(
                f"Expected {kind} {value or ''}, got {tok.type} '{tok.value}' "
                f"at line {tok.line}, col {tok.col}"
            )
        self.advance()
        return tok

    def accept(self, kind, value=None):
        tok = self.current()
        if tok.type == kind and (value is None or tok.value == value):
            self.advance()
            return tok
        return None

    # -----------------------------
    # Main entry
    # -----------------------------
    def parse(self):
        stmts = []
        while self.current().type != 'EOF':
            stmts.append(self.statement())
        return stmts

    # -----------------------------
    # Statements
    # -----------------------------
    def statement(self):
        tok = self.current()

        # list declaration
        if tok.type == 'KEYWORD' and tok.value == 'list':
            return self.list_decl()

        # sort statement
        if tok.type == 'KEYWORD' and tok.value == 'sort':
            return self.sort_stmt()

        # print statement
        if tok.type == 'KEYWORD' and tok.value == 'print':
            return self.print_stmt()

        # Standalone statement-level operations (shouldn't happen with new grammar)
        if tok.type == 'ID':
            raise SyntaxError(
                f"Unexpected identifier at statement level: {tok.value} "
                f"at line {tok.line}. Did you mean to assign it to a list?"
            )

        raise SyntaxError(f"Invalid statement start: {tok.type} '{tok.value}' at line {tok.line}")

    # -----------------------------
    # List declaration / sources
    # -----------------------------
    def list_decl(self):
        self.expect('KEYWORD', 'list')
        name = self.expect('ID').value
        self.expect('ASSIGN')
        source = self.list_source()
        return ListDecl(name, source)

    def list_source(self):
        tok = self.current()

        # Check for filter statement
        if tok.type == 'KEYWORD' and tok.value == 'filter':
            return self.filter_stmt()

        # Check for map statement
        if tok.type == 'KEYWORD' and tok.value == 'map':
            return self.map_stmt()

        # Check for set operations or list operations
        return self.list_op_stmt()

    # -----------------------------
    # List operations with precedence
    # -----------------------------
    def list_op_stmt(self):
        """Parse list operations with proper precedence"""
        return self.list_or_expr()

    def list_or_expr(self):
        node = self.list_xor_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'or':
            self.advance()
            right = self.list_xor_expr()
            node = ListOpStmt(node, 'or', right)
        return node

    def list_xor_expr(self):
        node = self.list_and_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'xor':
            self.advance()
            right = self.list_and_expr()
            node = ListOpStmt(node, 'xor', right)
        return node

    def list_and_expr(self):
        node = self.list_add_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'and':
            self.advance()
            right = self.list_add_expr()
            node = ListOpStmt(node, 'and', right)
        return node

    def list_add_expr(self):
        node = self.list_mul_expr()
        while self.current().type == 'OP' and self.current().value in ('+', '-'):
            op = self.current().value
            self.advance()
            right = self.list_mul_expr()
            node = ListOpStmt(node, op, right)
        return node

    def list_mul_expr(self):
        node = self.list_primary()
        while self.current().type == 'OP' and self.current().value in ('*', '/', '%'):
            op = self.current().value
            self.advance()
            right = self.list_primary()
            node = ListOpStmt(node, op, right)
        return node

    def list_primary(self):
        """
        ListPrimary → ListIdentifier | Number | "[" Array "]" | "(" ListOpStmt ")"
        Also handles set operations (union, intersection, difference)
        """
        tok = self.current()

        # Parenthesized list expression
        if tok.type == 'LPAREN':
            self.advance()
            node = self.list_op_stmt()
            self.expect('RPAREN')
            return node

        # Literal array
        if tok.type == 'LBRACK':
            self.advance()
            nums = []
            if not self.accept('RBRACK'):
                nums.append(float(self.expect('NUMBER').value))
                while self.accept('COMMA'):
                    nums.append(float(self.expect('NUMBER').value))
                self.expect('RBRACK')
            return nums

        # Number (for scalar operations)
        if tok.type == 'NUMBER':
            self.advance()
            return float(tok.value)

        # List identifier
        if tok.type == 'ID':
            name = tok.value
            self.advance()
            
            # Check for set operations
            next_tok = self.current()
            if next_tok.type == 'KEYWORD' and next_tok.value in ('union', 'intersection', 'difference'):
                op = next_tok.value
                self.advance()
                right = self.list_primary()
                return SetOpStmt(name, op, right)
            
            # Otherwise just return the identifier
            return name

        raise SyntaxError(
            f"Invalid list primary: {tok.type} '{tok.value}' at line {tok.line}"
        )

    # -----------------------------
    # Specific statements
    # -----------------------------
    def filter_stmt(self):
        self.expect('KEYWORD', 'filter')
        name = self.expect('ID').value
        op = self.expect('COMP').value
        val = float(self.expect('NUMBER').value)
        return FilterStmt(name, op, val)

    def sort_stmt(self):
        self.expect('KEYWORD', 'sort')
        name = self.expect('ID').value
        order = self.expect('KEYWORD').value  # asc / desc
        if order not in ('asc', 'desc'):
            raise SyntaxError(f"Sort order must be 'asc' or 'desc', got '{order}'")
        return SortStmt(name, order)

    def map_stmt(self):
        self.expect('KEYWORD', 'map')
        list_name = self.expect('ID').value
        self.expect('DOLLAR0')
        self.expect('ARROW')
        expr = self.expr()
        return MapStmt(list_name, expr)

    def print_stmt(self):
        self.expect('KEYWORD', 'print')
        target = self.expression_or_list()
        return PrintStmt(target)

    def expression_or_list(self):
        tok = self.current()
        
        # Check for statistical operations
        if tok.type == 'KEYWORD' and tok.value in (
            'mean', 'sum', 'median', 'variance', 'std', 'min', 'max', 'count'
        ):
            func = tok.value
            self.advance()
            name = self.expect('ID').value
            return StatStmt(func, name)
        
        # Otherwise must be a list identifier
        if tok.type == 'ID':
            return self.expect('ID').value
        
        raise SyntaxError(
            f"Print target must be list identifier or statistical operation, "
            f"got {tok.type} '{tok.value}' at line {tok.line}"
        )

    # -----------------------------
    # Map expression parser (for $0 expressions)
    # -----------------------------
    def expr(self):
        return self.or_expr()

    def or_expr(self):
        node = self.xor_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'or':
            self.advance()
            node = BinOp(node, 'or', self.xor_expr())
        return node

    def xor_expr(self):
        node = self.and_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'xor':
            self.advance()
            node = BinOp(node, 'xor', self.and_expr())
        return node

    def and_expr(self):
        node = self.add_expr()
        while self.current().type == 'KEYWORD' and self.current().value == 'and':
            self.advance()
            node = BinOp(node, 'and', self.add_expr())
        return node

    def add_expr(self):
        node = self.mul_expr()
        while self.current().type == 'OP' and self.current().value in ('+', '-'):
            op = self.current().value
            self.advance()
            node = BinOp(node, op, self.mul_expr())
        return node

    def mul_expr(self):
        node = self.primary()
        while self.current().type == 'OP' and self.current().value in ('*', '/', '%'):
            op = self.current().value
            self.advance()
            node = BinOp(node, op, self.primary())
        return node

    def primary(self):
        tok = self.current()
        
        # Unary minus
        if tok.type == 'OP' and tok.value == '-':
            self.advance()
            return UnaryOp('-', self.primary())

        # Number
        if tok.type == 'NUMBER':
            self.advance()
            return Number(float(tok.value))

        # $0 variable
        if tok.type == 'DOLLAR0':
            self.advance()
            return Var('$0')

        # Parenthesized expression
        if tok.type == 'LPAREN':
            self.advance()
            node = self.expr()
            self.expect('RPAREN')
            return node

        raise SyntaxError(
            f"Invalid expression primary: {tok.type} '{tok.value}' at line {tok.line}"
        )