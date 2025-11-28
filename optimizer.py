# class Optimizer:
#     def __init__(self, tac):
#         self.tac = tac

#     # -----------------------------------------------------
#     # ENTRY POINT
#     # -----------------------------------------------------
#     def optimize(self):
#         self.constant_folding()
#         self.remove_self_assign()
#         self.remove_duplicate_sorts()
#         self.dead_code_elimination()
#         self.copy_propagation()

#         return self.tac

#     # -----------------------------------------------------
#     # CONSTANT FOLDING for MAP expressions
#     # -----------------------------------------------------
#     def constant_folding(self):
#         optimized = []
#         for instr in self.tac:
#             if instr[0] == "MAP":
#                 opcode, dest, src, var, expr = instr

#                 # Try evaluating MAP expr if it's numeric only
#                 try:
#                     # reject if it uses the map variable
#                     if var not in expr:
#                         # Evaluate as Python expression
#                         const_val = eval(expr)
#                         expr = str(const_val)
#                         instr = ("MAP", dest, src, var, expr)
#                 except:
#                     pass

#             optimized.append(instr)
#         self.tac = optimized

#     # -----------------------------------------------------
#     # REMOVE ASSIGN x = x
#     # -----------------------------------------------------
#     def remove_self_assign(self):
#         optimized = []
#         for instr in self.tac:
#             if instr[0] == "ASSIGN":
#                 name, src = instr[1], instr[2]
#                 if name == src:
#                     continue
#             optimized.append(instr)
#         self.tac = optimized

#     # -----------------------------------------------------
#     # REMOVE REDUNDANT SORTS: two consecutive sorts with same order
#     # -----------------------------------------------------
#     def remove_duplicate_sorts(self):
#         optimized = []
#         last_sort = {}

#         for instr in self.tac:
#             if instr[0] == "SORT":
#                 dest, src, order = instr[1], instr[2], instr[3]
#                 key = (src, order)

#                 if key in last_sort:  # redundant
#                     continue

#                 last_sort[key] = True

#             optimized.append(instr)

#         self.tac = optimized

#     # -----------------------------------------------------
#     # DEAD CODE ELIMINATION
#     # Remove instructions producing temps never consumed later
#     # -----------------------------------------------------
#     def dead_code_elimination(self):
#         # Step 1: Find used variables
#         used = set()

#         for instr in self.tac:
#             opcode = instr[0]

#             if opcode == "ASSIGN":
#                 used.add(instr[2])
#             elif opcode in ("FILTER", "SORT", "MAP", "SETOP"):
#                 # record source lists
#                 used.add(instr[2])
#             elif opcode == "STAT":
#                 used.add(instr[3])
#             elif opcode == "PRINT":
#                 used.add(instr[1])

#         # Step 2: Remove instructions that define temps but temps not used
#         optimized = []
#         for instr in self.tac:
#             opcode = instr[0]

#             if opcode in ("FILTER", "SORT", "MAP", "SETOP"):
#                 dest = instr[1]
#                 if dest.startswith("t") and dest not in used:
#                     # temp produced but never used
#                     continue

#             optimized.append(instr)

#         self.tac = optimized

#     # -----------------------------------------------------
#     # COPY PROPAGATION
#     # Replace: ASSIGN x = y, then x→y
#     # -----------------------------------------------------
#     def copy_propagation(self):
#         mapping = {}

#         # Build replacement map
#         for instr in self.tac:
#             if instr[0] == "ASSIGN":
#                 name, src = instr[1], instr[2]
#                 mapping[name] = src

#         # Apply replacement
#         optimized = []
#         for instr in self.tac:
#             new_instr = list(instr)

#             for i in range(1, len(new_instr)):
#                 val = new_instr[i]
#                 if isinstance(val, str) and val in mapping:
#                     new_instr[i] = mapping[val]

#             optimized.append(tuple(new_instr))

#         self.tac = optimized


class Optimizer:
    def __init__(self, tac):
        self.tac = tac

    # -----------------------------------------------------
    # ENTRY POINT
    # -----------------------------------------------------
    def optimize(self):
        """Run all optimization passes"""
        initial_size = len(self.tac)
        
        # Run optimizations in multiple passes until no changes
        changed = True
        passes = 0
        max_passes = 5
        
        while changed and passes < max_passes:
            old_size = len(self.tac)
            
            self.constant_folding()
            self.algebraic_simplification()
            self.strength_reduction()
            self.dead_code_elimination()
            self.copy_propagation()
            self.remove_redundant_operations()
            
            changed = (len(self.tac) != old_size)
            passes += 1
        
        final_size = len(self.tac)
        print(f"✓ Optimization complete: {initial_size} → {final_size} instructions ({passes} passes)")
        
        return self.tac

    # -----------------------------------------------------
    # CONSTANT FOLDING for MAP expressions
    # -----------------------------------------------------
    def constant_folding(self):
        """Fold constant expressions in MAP statements"""
        optimized = []
        
        for instr in self.tac:
            if instr[0] == "MAP":
                # New format: ('MAP', dest, src, expr_code)
                opcode, dest, src, expr_code = instr
                
                # Try evaluating if expression doesn't contain 'x' (the $0 variable)
                if 'x' not in expr_code:
                    try:
                        # Evaluate as Python expression
                        const_val = eval(expr_code, {"__builtins__": {}})
                        # Replace with constant
                        expr_code = str(const_val)
                        instr = ("MAP", dest, src, expr_code)
                    except:
                        pass  # Keep original if evaluation fails
            
            optimized.append(instr)
        
        self.tac = optimized

    # -----------------------------------------------------
    # ALGEBRAIC SIMPLIFICATION
    # -----------------------------------------------------
    def algebraic_simplification(self):
        """Simplify algebraic expressions in MAP and LISTOP"""
        optimized = []
        
        for instr in self.tac:
            if instr[0] == "MAP":
                opcode, dest, src, expr_code = instr
                expr_code = self._simplify_expr(expr_code)
                instr = ("MAP", dest, src, expr_code)
            
            elif instr[0] == "LISTOP":
                # ('LISTOP', dest, op, left, right)
                opcode, dest, op, left, right = instr
                
                # Simplify: x + 0 = x, x * 1 = x, x * 0 = 0, etc.
                if op == '+' and right == 0:
                    # Replace with copy
                    instr = ("COPY", dest, left)
                elif op == '+' and left == 0:
                    instr = ("COPY", dest, right)
                elif op == '-' and right == 0:
                    instr = ("COPY", dest, left)
                elif op == '*' and (left == 1 or right == 1):
                    other = right if left == 1 else left
                    instr = ("COPY", dest, other)
                elif op == '*' and (left == 0 or right == 0):
                    instr = ("LIST", dest, [0])
                elif op == '/' and right == 1:
                    instr = ("COPY", dest, left)
                elif op == 'and' and (left == 0 or right == 0):
                    instr = ("LIST", dest, [0])
                elif op == 'or' and left == 0:
                    instr = ("COPY", dest, right)
                elif op == 'or' and right == 0:
                    instr = ("COPY", dest, left)
                elif op == 'xor' and right == 0:
                    instr = ("COPY", dest, left)
                elif op == 'xor' and left == 0:
                    instr = ("COPY", dest, right)
            
            optimized.append(instr)
        
        self.tac = optimized

    def _simplify_expr(self, expr):
        """Simplify constant subexpressions in MAP expressions"""
        # x + 0 → x
        expr = expr.replace('(x + 0)', 'x').replace('(0 + x)', 'x')
        # x - 0 → x
        expr = expr.replace('(x - 0)', 'x')
        # x * 1 → x
        expr = expr.replace('(x * 1)', 'x').replace('(1 * x)', 'x')
        # x * 0 → 0
        expr = expr.replace('(x * 0)', '0').replace('(0 * x)', '0')
        # x / 1 → x
        expr = expr.replace('(x / 1)', 'x')
        # x & 0 → 0
        expr = expr.replace('(x & 0)', '0').replace('(0 & x)', '0')
        # x | 0 → x
        expr = expr.replace('(x | 0)', 'x').replace('(0 | x)', 'x')
        # x ^ 0 → x
        expr = expr.replace('(x ^ 0)', 'x').replace('(0 ^ x)', 'x')
        
        return expr

    # -----------------------------------------------------
    # STRENGTH REDUCTION
    # -----------------------------------------------------
    def strength_reduction(self):
        """Replace expensive operations with cheaper equivalents"""
        optimized = []
        
        for instr in self.tac:
            if instr[0] == "MAP":
                opcode, dest, src, expr_code = instr
                
                # x * 2 → x + x (shift would be better but not in our language)
                # x / 2 → x * 0.5
                # Keep for now, as our language doesn't have bit shifts
                
            elif instr[0] == "LISTOP":
                opcode, dest, op, left, right = instr
                
                # x * 2 → x + x (addition is faster than multiplication)
                if op == '*' and right == 2:
                    instr = ("LISTOP", dest, '+', left, left)
                elif op == '*' and left == 2:
                    instr = ("LISTOP", dest, '+', right, right)
            
            optimized.append(instr)
        
        self.tac = optimized

    # -----------------------------------------------------
    # DEAD CODE ELIMINATION
    # -----------------------------------------------------
    def dead_code_elimination(self):
        """Remove instructions that produce unused results"""
        
        # Step 1: Find all used variables (backward pass)
        used = set()
        
        for instr in self.tac:
            opcode = instr[0]
            
            # Track all variables that are READ
            if opcode == "LIST":
                # ('LIST', name, source)
                if len(instr) > 2 and isinstance(instr[2], str):
                    used.add(instr[2])
            
            elif opcode == "FILTER":
                # ('FILTER', dest, src, op, value)
                used.add(instr[2])  # src
            
            elif opcode == "MAP":
                # ('MAP', dest, src, expr)
                used.add(instr[2])  # src
            
            elif opcode == "SORT":
                # ('SORT', name, order)
                used.add(instr[1])  # name (both read and write)
            
            elif opcode == "STAT":
                # ('STAT', dest, func, list_name)
                used.add(instr[3])  # list_name
            
            elif opcode == "PRINT":
                # ('PRINT', target)
                used.add(instr[1])  # target
            
            elif opcode == "SETOP":
                # ('SETOP', dest, op, left, right)
                if isinstance(instr[3], str):
                    used.add(instr[3])
                if isinstance(instr[4], str):
                    used.add(instr[4])
            
            elif opcode == "LISTOP":
                # ('LISTOP', dest, op, left, right)
                if isinstance(instr[3], str):
                    used.add(instr[3])
                if isinstance(instr[4], str):
                    used.add(instr[4])
            
            elif opcode == "COPY":
                # ('COPY', dest, src)
                used.add(instr[2])
        
        # Step 2: Remove instructions that define temps never used
        optimized = []
        
        for instr in self.tac:
            opcode = instr[0]
            
            # Check if this instruction produces a dead temp
            if opcode in ("FILTER", "MAP", "STAT", "SETOP", "LISTOP", "COPY"):
                dest = instr[1]
                # If destination is a temp and never used, skip this instruction
                if dest.startswith("t") and dest not in used:
                    continue
            
            elif opcode == "LIST":
                # ('LIST', name, source)
                name = instr[1]
                if name.startswith("t") and name not in used:
                    continue
            
            optimized.append(instr)
        
        self.tac = optimized

    # -----------------------------------------------------
    # COPY PROPAGATION
    # -----------------------------------------------------
    def copy_propagation(self):
        """Replace copies with direct references where possible"""
        
        # Build copy mapping: dest -> src for simple copies
        copies = {}
        
        for instr in self.tac:
            if instr[0] == "COPY":
                dest, src = instr[1], instr[2]
                copies[dest] = src
            elif instr[0] == "LIST" and isinstance(instr[2], str):
                # list x = y is also a copy
                dest, src = instr[1], instr[2]
                copies[dest] = src
        
        # Apply copy propagation
        optimized = []
        
        for instr in self.tac:
            new_instr = list(instr)
            opcode = instr[0]
            
            # Don't propagate into the destination
            start_idx = 2 if opcode in ("LIST", "FILTER", "MAP", "STAT", "SETOP", "LISTOP", "COPY") else 1
            
            # Replace uses with original source
            for i in range(start_idx, len(new_instr)):
                val = new_instr[i]
                if isinstance(val, str) and val in copies:
                    new_instr[i] = copies[val]
            
            optimized.append(tuple(new_instr))
        
        self.tac = optimized

    # -----------------------------------------------------
    # REMOVE REDUNDANT OPERATIONS
    # -----------------------------------------------------
    def remove_redundant_operations(self):
        """Remove redundant sorts, filters, and other operations"""
        optimized = []
        last_sort = {}
        
        for instr in self.tac:
            skip = False
            
            # Remove consecutive identical sorts
            if instr[0] == "SORT":
                # ('SORT', name, order)
                name, order = instr[1], instr[2]
                key = (name, order)
                
                if key in last_sort:
                    skip = True  # Redundant sort
                else:
                    last_sort[key] = True
            
            # Remove identity copies (added by algebraic simplification)
            elif instr[0] == "COPY":
                dest, src = instr[1], instr[2]
                if dest == src:
                    skip = True
            
            # Remove list x = x
            elif instr[0] == "LIST" and isinstance(instr[2], str):
                name, src = instr[1], instr[2]
                if name == src:
                    skip = True
            
            if not skip:
                optimized.append(instr)
        
        self.tac = optimized

    # -----------------------------------------------------
    # COMMON SUBEXPRESSION ELIMINATION (NEW)
    # -----------------------------------------------------
    def common_subexpression_elimination(self):
        """Eliminate redundant computations"""
        optimized = []
        computed = {}  # (opcode, operands) -> result temp
        
        for instr in self.tac:
            opcode = instr[0]
            
            # Check for duplicate computations
            if opcode in ("FILTER", "MAP", "LISTOP", "SETOP"):
                # Create key from operation
                key = tuple(instr[1:])  # Everything except dest
                
                if key in computed:
                    # Replace with copy from previous result
                    dest = instr[1]
                    prev_result = computed[key]
                    optimized.append(("COPY", dest, prev_result))
                else:
                    # Record this computation
                    dest = instr[1]
                    computed[key] = dest
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        self.tac = optimized

    # -----------------------------------------------------
    # UTILITY: Pretty print
    # -----------------------------------------------------
    @staticmethod
    def pretty_print(tac_list):
        """Pretty print TAC instructions"""
        for i, instr in enumerate(tac_list, 1):
            print(f"{i:03}: {instr}")