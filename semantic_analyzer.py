from parser import (
    ListDecl, FilterStmt, SortStmt, MapStmt, StatStmt, PrintStmt, 
    SetOpStmt, ListOpStmt, BinOp, UnaryOp, Number, Var
)

class SemanticAnalyzer:
    def __init__(self):
        # symbol table: name -> { "type": "list", "declared": True }
        self.symbols = {}

    def analyze(self, ast):
        """Perform semantic analysis on the AST"""
        for node in ast:
            self.visit(node)
        return self.symbols

    # --------------------------------------------
    # Node Dispatcher
    # --------------------------------------------
    def visit(self, node):
        """Dispatch to appropriate visitor method"""
        
        if isinstance(node, ListDecl):
            return self.visit_list_decl(node)
        
        if isinstance(node, FilterStmt):
            return self.visit_filter(node)
        
        if isinstance(node, SortStmt):
            return self.visit_sort(node)
        
        if isinstance(node, MapStmt):
            return self.visit_map(node)
        
        if isinstance(node, StatStmt):
            return self.visit_stat(node)
        
        if isinstance(node, PrintStmt):
            return self.visit_print(node)
        
        if isinstance(node, SetOpStmt):
            return self.visit_set_op(node)
        
        if isinstance(node, ListOpStmt):
            return self.visit_list_op(node)
        
        # For expressions in map statements
        if isinstance(node, (BinOp, UnaryOp, Number, Var)):
            return self.validate_expr(node)
        
        # For literal lists and identifiers
        if isinstance(node, list):
            return  # Literal array
        
        if isinstance(node, str):
            return  # Identifier (will be checked when used)
        
        if isinstance(node, (int, float)):
            return  # Scalar number
        
        raise Exception(f"Unknown AST node type: {type(node).__name__}")

    # --------------------------------------------
    # Semantic Rule Implementations
    # --------------------------------------------

    def visit_list_decl(self, node):
        """Validate list declaration: list name = source"""
        
        # Check for redeclaration
        if node.name in self.symbols:
            raise Exception(f"Semantic Error: Redeclaration of '{node.name}'")
        
        # Validate the source
        self.validate_list_source(node.source)
        
        # Add to symbol table
        self.symbols[node.name] = {"type": "list", "declared": True}

    def validate_list_source(self, source):
        """Validate a list source (array, identifier, or statement)"""
        
        # Literal array [1, 2, 3]
        if isinstance(source, list):
            for v in source:
                if not isinstance(v, (int, float)):
                    raise Exception(f"Semantic Error: List contains non-numeric value {v}")
            return
        
        # Identifier reference
        if isinstance(source, str):
            self.assert_declared(source)
            self.assert_list(source)
            return
        
        # Scalar number (for operations like: list x = 5)
        if isinstance(source, (int, float)):
            return
        
        # Statement (filter, map, set op, list op)
        if isinstance(source, (FilterStmt, MapStmt, SetOpStmt, ListOpStmt)):
            self.visit(source)
            return
        
        raise Exception(f"Semantic Error: Invalid list source type {type(source).__name__}")

    def visit_filter(self, node):
        """Validate filter statement: filter list_name > value"""
        self.assert_declared(node.list_name)
        self.assert_list(node.list_name)
        
        # Validate comparison operator
        if node.op not in ("==", "!=", ">", ">=", "<", "<="):
            raise Exception(f"Semantic Error: Invalid comparison operator '{node.op}'")
        
        # Validate value is numeric
        if not isinstance(node.value, (int, float)):
            raise Exception(f"Semantic Error: Filter value must be numeric, got {type(node.value).__name__}")

    def visit_sort(self, node):
        """Validate sort statement: sort list_name asc/desc"""
        self.assert_declared(node.list_name)
        self.assert_list(node.list_name)
        
        if node.order not in ("asc", "desc"):
            raise Exception(f"Semantic Error: Sort order must be 'asc' or 'desc', got '{node.order}'")

    def visit_map(self, node):
        """Validate map statement: map list_name $0 => expr"""
        self.assert_declared(node.list_name)
        self.assert_list(node.list_name)
        
        # Validate the expression uses only $0 and numbers
        self.validate_map_expr(node.expr)

    def visit_stat(self, node):
        """Validate statistical operation: mean list_name"""
        self.assert_declared(node.list_name)
        self.assert_list(node.list_name)
        
        valid_funcs = ('mean', 'sum', 'median', 'variance', 'std', 'min', 'max', 'count')
        if node.func not in valid_funcs:
            raise Exception(f"Semantic Error: Invalid statistical function '{node.func}'")

    def visit_print(self, node):
        """Validate print statement: print target"""
        
        # Print a statistical operation
        if isinstance(node.target, StatStmt):
            self.visit_stat(node.target)
            return
        
        # Print a list identifier
        if isinstance(node.target, str):
            self.assert_declared(node.target)
            self.assert_list(node.target)
            return
        
        raise Exception(f"Semantic Error: Print target must be a list identifier or statistical operation")

    def visit_set_op(self, node):
        """Validate set operation: list1 union list2"""
        
        # Validate left operand
        if isinstance(node.left, str):
            self.assert_declared(node.left)
            self.assert_list(node.left)
        else:
            self.validate_list_source(node.left)
        
        # Validate right operand
        if isinstance(node.right, str):
            self.assert_declared(node.right)
            self.assert_list(node.right)
        else:
            self.validate_list_source(node.right)
        
        # Validate operator
        if node.op not in ("union", "intersection", "difference"):
            raise Exception(f"Semantic Error: Invalid set operation '{node.op}'")

    def visit_list_op(self, node):
        """Validate list operation: a + b * 2"""
        
        # Validate left operand
        if isinstance(node.left, str):
            self.assert_declared(node.left)
            self.assert_list(node.left)
        elif isinstance(node.left, (int, float)):
            pass  # Scalar is ok
        elif isinstance(node.left, list):
            pass  # Literal array is ok
        elif isinstance(node.left, ListOpStmt):
            self.visit_list_op(node.left)  # Recursive
        else:
            raise Exception(f"Semantic Error: Invalid list operation operand type {type(node.left).__name__}")
        
        # Validate right operand
        if isinstance(node.right, str):
            self.assert_declared(node.right)
            self.assert_list(node.right)
        elif isinstance(node.right, (int, float)):
            pass  # Scalar is ok
        elif isinstance(node.right, list):
            pass  # Literal array is ok
        elif isinstance(node.right, ListOpStmt):
            self.visit_list_op(node.right)  # Recursive
        else:
            raise Exception(f"Semantic Error: Invalid list operation operand type {type(node.right).__name__}")
        
        # Validate operator
        if node.op not in ('+', '-', '*', '/', '%', 'and', 'or', 'xor'):
            raise Exception(f"Semantic Error: Invalid list operation '{node.op}'")

    # --------------------------------------------
    # Expression Validation (for map statements)
    # --------------------------------------------
    def validate_map_expr(self, expr):
        """Validate expression in map statement - only $0 and numbers allowed"""
        
        if isinstance(expr, Number):
            return  # Numbers are always valid
        
        if isinstance(expr, Var):
            if expr.name != "$0":
                raise Exception(f"Semantic Error: Invalid variable '{expr.name}' in map expression. Only $0 is allowed.")
            return
        
        if isinstance(expr, UnaryOp):
            if expr.op != '-':
                raise Exception(f"Semantic Error: Invalid unary operator '{expr.op}' in map expression")
            self.validate_map_expr(expr.expr)
            return
        
        if isinstance(expr, BinOp):
            # Validate operator
            if expr.op not in ('+', '-', '*', '/', '%', 'and', 'or', 'xor'):
                raise Exception(f"Semantic Error: Invalid operator '{expr.op}' in map expression")
            
            # Recursively validate operands
            self.validate_map_expr(expr.left)
            self.validate_map_expr(expr.right)
            return
        
        raise Exception(f"Semantic Error: Invalid expression type {type(expr).__name__} in map")

    def validate_expr(self, expr):
        """General expression validation (for non-map contexts)"""
        # Currently same as validate_map_expr, but separated for future extension
        return self.validate_map_expr(expr)

    # --------------------------------------------
    # Helper Functions
    # --------------------------------------------
    def assert_declared(self, name):
        """Check if a variable has been declared"""
        if name not in self.symbols:
            raise Exception(f"Semantic Error: Variable '{name}' not declared")

    def assert_list(self, name):
        """Check if a variable is a list type"""
        if name not in self.symbols:
            raise Exception(f"Semantic Error: Variable '{name}' not declared")
        
        if self.symbols[name]["type"] != "list":
            raise Exception(f"Semantic Error: Variable '{name}' is not a list")