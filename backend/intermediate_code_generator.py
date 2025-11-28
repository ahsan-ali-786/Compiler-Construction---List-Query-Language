from typing import List
from parser import (
    ListDecl, FilterStmt, SortStmt, MapStmt, StatStmt, PrintStmt,
    SetOpStmt, ListOpStmt, BinOp, UnaryOp, Number, Var
)

class TACGenerator:
    def __init__(self):
        self.instructions = []   # list of TAC tuples
        self.temp_count = 0

    def new_temp(self):
        """Generate a new temporary variable"""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast: List):
        """Main entry: walk AST and emit TAC."""
        for node in ast:
            self.visit(node)
        return self.instructions

    # ---------- Dispatcher ----------
    def visit(self, node):
        """Dispatch to appropriate visitor method"""
        
        if isinstance(node, ListDecl):
            return self.visit_ListDecl(node)
        
        if isinstance(node, FilterStmt):
            return self.visit_FilterStmt(node)
        
        if isinstance(node, SortStmt):
            return self.visit_SortStmt(node)
        
        if isinstance(node, MapStmt):
            return self.visit_MapStmt(node)
        
        if isinstance(node, StatStmt):
            return self.visit_StatStmt(node)
        
        if isinstance(node, PrintStmt):
            return self.visit_PrintStmt(node)
        
        if isinstance(node, SetOpStmt):
            return self.visit_SetOpStmt(node)
        
        if isinstance(node, ListOpStmt):
            return self.visit_ListOpStmt(node)
        
        # Handle literal values in list sources
        if isinstance(node, list):
            return node  # Literal array
        
        if isinstance(node, str):
            return node  # Identifier
        
        if isinstance(node, (int, float)):
            return node  # Scalar
        
        raise Exception(f"No TAC handler for node type {type(node).__name__}")

    # ---------- Node handlers ----------
    
    def visit_ListDecl(self, node):
        """Handle: list name = source"""
        
        # Evaluate the source
        source_result = self.visit_source(node.source)
        
        # Emit list assignment
        self.instructions.append(('LIST', node.name, source_result))
        return node.name

    def visit_source(self, source):
        """Handle various list sources"""
        
        # Literal array: [1, 2, 3]
        if isinstance(source, list):
            return source
        
        # Identifier: data
        if isinstance(source, str):
            return source
        
        # Scalar number: 8
        if isinstance(source, (int, float)):
            return source
        
        # Statement (filter, map, set op, list op)
        if isinstance(source, (FilterStmt, MapStmt, SetOpStmt, ListOpStmt)):
            return self.visit(source)
        
        raise Exception(f"Unknown source type: {type(source).__name__}")

    def visit_FilterStmt(self, node):
        """Handle: filter list_name op value"""
        dest = self.new_temp()
        self.instructions.append(('FILTER', dest, node.list_name, node.op, node.value))
        return dest

    def visit_SortStmt(self, node):
        """Handle: sort list_name asc/desc"""
        # Sort modifies in-place
        self.instructions.append(('SORT', node.list_name, node.order))
        return node.list_name

    def visit_MapStmt(self, node):
        """Handle: map list_name $0 => expr"""
        dest = self.new_temp()
        
        # Convert expression to evaluable code
        expr_code = self.expr_to_code(node.expr)
        
        self.instructions.append(('MAP', dest, node.list_name, expr_code))
        return dest

    def visit_StatStmt(self, node):
        """Handle: mean list_name, sum list_name, etc."""
        dest = self.new_temp()
        self.instructions.append(('STAT', dest, node.func, node.list_name))
        return dest

    def visit_PrintStmt(self, node):
        """Handle: print target"""
        
        # If target is a StatStmt, evaluate it first
        if isinstance(node.target, StatStmt):
            result = self.visit_StatStmt(node.target)
            self.instructions.append(('PRINT', result))
        else:
            # Otherwise it's a list identifier
            self.instructions.append(('PRINT', node.target))
        
        return None

    def visit_SetOpStmt(self, node):
        """Handle: list1 union list2"""
        dest = self.new_temp()
        
        # Get left operand
        if isinstance(node.left, str):
            left = node.left
        else:
            left = self.visit(node.left)
        
        # Get right operand
        if isinstance(node.right, str):
            right = node.right
        else:
            right = self.visit(node.right)
        
        self.instructions.append(('SETOP', dest, node.op, left, right))
        return dest

    def visit_ListOpStmt(self, node):
        """Handle: a + b * 2, flags or 8, etc."""
        dest = self.new_temp()
        
        # Get left operand
        if isinstance(node.left, str):
            left = node.left
        elif isinstance(node.left, (int, float)):
            left = node.left
        elif isinstance(node.left, list):
            left = node.left
        elif isinstance(node.left, ListOpStmt):
            left = self.visit_ListOpStmt(node.left)
        else:
            left = self.visit(node.left)
        
        # Get right operand
        if isinstance(node.right, str):
            right = node.right
        elif isinstance(node.right, (int, float)):
            right = node.right
        elif isinstance(node.right, list):
            right = node.right
        elif isinstance(node.right, ListOpStmt):
            right = self.visit_ListOpStmt(node.right)
        else:
            right = self.visit(node.right)
        
        self.instructions.append(('LISTOP', dest, node.op, left, right))
        return dest

    # ---------- Expression handling (for map statements) ----------
    
    def expr_to_code(self, expr):
        """
        Convert expression AST to evaluable Python code string.
        Used for map expressions like: $0 * 2 + 5
        """
        
        if isinstance(expr, Number):
            # Render as integer if it's a whole number
            if isinstance(expr.value, float) and expr.value.is_integer():
                return str(int(expr.value))
            return str(expr.value)
        
        if isinstance(expr, Var):
            # $0 becomes 'x' in the evaluable code (will be replaced at runtime)
            return 'x'
        
        if isinstance(expr, UnaryOp):
            operand = self.expr_to_code(expr.expr)
            return f"(-{operand})"
        
        if isinstance(expr, BinOp):
            left = self.expr_to_code(expr.left)
            right = self.expr_to_code(expr.right)
            
            # Convert bitwise operators to Python equivalents
            op = expr.op
            if op == 'and':
                op = '&'
            elif op == 'or':
                op = '|'
            elif op == 'xor':
                op = '^'
            
            return f"({left} {op} {right})"
        
        raise Exception(f"Unknown expression type: {type(expr).__name__}")

    # ---------- Utility ----------
    
    @staticmethod
    def pretty_print(tac_list):
        """Pretty print TAC instructions"""
        for i, instr in enumerate(tac_list, 1):
            print(f"{i:03}: {instr}")