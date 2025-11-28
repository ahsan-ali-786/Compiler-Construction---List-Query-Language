import math

class Executor:
    def __init__(self, tac, symbol_table=None):
        self.tac = tac
        self.memory = {}  # stores lists, temps, and scalars
        
        # Initialize with symbol table if provided
        if symbol_table:
            self.memory.update(symbol_table)

    # ------------------------------------------------------
    # MAIN EXECUTION LOOP
    # ------------------------------------------------------
    def run(self):
        """Execute all TAC instructions"""
        for instr in self.tac:
            opcode = instr[0]

            if opcode == "LIST":
                self.exec_list(instr)
            
            elif opcode == "FILTER":
                self.exec_filter(instr)
            
            elif opcode == "SORT":
                self.exec_sort(instr)
            
            elif opcode == "MAP":
                self.exec_map(instr)
            
            elif opcode == "STAT":
                self.exec_stat(instr)
            
            elif opcode == "SETOP":
                self.exec_setop(instr)
            
            elif opcode == "LISTOP":
                self.exec_listop(instr)
            
            elif opcode == "COPY":
                self.exec_copy(instr)
            
            elif opcode == "PRINT":
                self.exec_print(instr)
            
            else:
                raise Exception(f"Unknown opcode: {opcode}")

        return self.memory

    # ------------------------------------------------------
    # INSTRUCTION EXECUTORS
    # ------------------------------------------------------
    
    def exec_list(self, instr):
        """Execute: ('LIST', name, source)"""
        _, name, source = instr
        
        # Source can be: literal list, identifier, or scalar
        if isinstance(source, list):
            self.memory[name] = source
        elif isinstance(source, str):
            self.memory[name] = self.memory[source]
        elif isinstance(source, (int, float)):
            self.memory[name] = [source]
        else:
            raise Exception(f"Invalid LIST source: {source}")

    def exec_filter(self, instr):
        """Execute: ('FILTER', dest, src, op, value)"""
        _, dest, src, op, val = instr
        lst = self.get_list(src)
        self.memory[dest] = [x for x in lst if self.eval_condition(x, op, val)]

    def exec_sort(self, instr):
        """Execute: ('SORT', name, order) - modifies in place"""
        _, name, order = instr
        lst = self.get_list(name)
        self.memory[name] = sorted(lst, reverse=(order == "desc"))

    def exec_map(self, instr):
        """Execute: ('MAP', dest, src, expr_code)"""
        _, dest, src, expr_code = instr
        lst = self.get_list(src)
        
        # Expression uses 'x' as the variable name
        # Create a safe evaluation function
        def map_func(x):
            try:
                # Provide safe math functions
                safe_globals = {
                    '__builtins__': {},
                    'abs': abs,
                    'min': min,
                    'max': max,
                    'int': int,
                    'float': float
                }
                return eval(expr_code, safe_globals, {'x': int(x)})
            except Exception as e:
                raise Exception(f"Error evaluating map expression '{expr_code}' with x={x}: {e}")
        
        self.memory[dest] = [map_func(x) for x in lst]

    def exec_stat(self, instr):
        """Execute: ('STAT', dest, func, list_name)"""
        _, dest, func, src = instr
        lst = self.get_list(src)
        self.memory[dest] = self.compute_stat(func, lst)

    def exec_setop(self, instr):
        """Execute: ('SETOP', dest, op, left, right)"""
        _, dest, op, left, right = instr
        
        # Get left operand
        if isinstance(left, str):
            a = self.get_list(left)
        elif isinstance(left, list):
            a = left
        else:
            raise Exception(f"Invalid SETOP left operand: {left}")
        
        # Get right operand
        if isinstance(right, str):
            b = self.get_list(right)
        elif isinstance(right, list):
            b = right
        else:
            raise Exception(f"Invalid SETOP right operand: {right}")
        
        self.memory[dest] = self.set_operation(op, a, b)

    def exec_listop(self, instr):
        """Execute: ('LISTOP', dest, op, left, right) - element-wise operations"""
        _, dest, op, left, right = instr
        
        # Get left operand (can be list, identifier, or scalar)
        left_val = self.get_operand(left)
        
        # Get right operand (can be list, identifier, or scalar)
        right_val = self.get_operand(right)
        
        # Perform element-wise operation
        self.memory[dest] = self.element_wise_op(op, left_val, right_val)

    def exec_copy(self, instr):
        """Execute: ('COPY', dest, src)"""
        _, dest, src = instr
        
        if isinstance(src, str):
            self.memory[dest] = self.memory[src]
        elif isinstance(src, list):
            self.memory[dest] = src
        elif isinstance(src, (int, float)):
            self.memory[dest] = [src]
        else:
            raise Exception(f"Invalid COPY source: {src}")

    def exec_print(self, instr):
        """Execute: ('PRINT', target)"""
        _, target = instr
        
        if target in self.memory:
            value = self.memory[target]
            
            # Pretty print lists
            if isinstance(value, list):
                print(value)
            # Print scalar values (from STAT operations)
            elif isinstance(value, (int, float)):
                print(value)
            else:
                print(value)
        else:
            raise Exception(f"Variable '{target}' not found in memory")

    # ------------------------------------------------------
    # HELPER FUNCTIONS
    # ------------------------------------------------------
    
    def get_list(self, src):
        """Get a list from memory or convert scalar to list"""
        if isinstance(src, str):
            val = self.memory.get(src)
            if val is None:
                raise Exception(f"Variable '{src}' not found")
            if isinstance(val, list):
                return val
            # Convert scalar to single-element list
            return [val]
        elif isinstance(src, list):
            return src
        elif isinstance(src, (int, float)):
            return [src]
        else:
            raise Exception(f"Invalid list source: {src}")

    def get_operand(self, operand):
        """Get operand value (list, scalar, or identifier)"""
        if isinstance(operand, str):
            val = self.memory.get(operand)
            if val is None:
                raise Exception(f"Variable '{operand}' not found")
            return val
        elif isinstance(operand, list):
            return operand
        elif isinstance(operand, (int, float)):
            return operand
        else:
            raise Exception(f"Invalid operand: {operand}")

    def element_wise_op(self, op, left, right):
        """Perform element-wise operation on lists/scalars"""
        
        # Convert scalars to lists for uniform handling
        left_list = left if isinstance(left, list) else [left]
        right_list = right if isinstance(right, list) else [right]
        
        # Handle broadcasting
        if len(left_list) == 1 and len(right_list) > 1:
            # Broadcast left scalar to right list length
            left_list = left_list * len(right_list)
        elif len(right_list) == 1 and len(left_list) > 1:
            # Broadcast right scalar to left list length
            right_list = right_list * len(left_list)
        elif len(left_list) != len(right_list):
            raise Exception(f"List length mismatch: {len(left_list)} vs {len(right_list)}")
        
        # Perform element-wise operation
        result = []
        for a, b in zip(left_list, right_list):
            if op == '+':
                result.append(a + b)
            elif op == '-':
                result.append(a - b)
            elif op == '*':
                result.append(a * b)
            elif op == '/':
                if b == 0:
                    raise Exception("Division by zero")
                result.append(a / b)
            elif op == '%':
                if b == 0:
                    raise Exception("Modulo by zero")
                result.append(a % b)
            elif op == 'and':
                # Bitwise AND (convert to int for bitwise ops)
                result.append(int(a) & int(b))
            elif op == 'or':
                # Bitwise OR
                result.append(int(a) | int(b))
            elif op == 'xor':
                # Bitwise XOR
                result.append(int(a) ^ int(b))
            else:
                raise Exception(f"Unknown list operator: {op}")
        
        return result

    def eval_condition(self, x, op, val):
        """Evaluate comparison condition"""
        if op == ">":
            return x > val
        elif op == "<":
            return x < val
        elif op == ">=":
            return x >= val
        elif op == "<=":
            return x <= val
        elif op == "==":
            return x == val
        elif op == "!=":
            return x != val
        else:
            raise Exception(f"Invalid comparison operator: {op}")

    # def compute_stat(self, func, lst):
    #     """Compute statistical function on list"""
    #     if not lst:
    #         raise Exception(f"Cannot compute {func} on empty list")
        
    #     if func == "sum":
    #         return sum(lst)
        
    #     elif func == "mean":
    #         return sum(lst) / len(lst)
        
    #     elif func == "min":
    #         return min(lst)
        
    #     elif func == "max":
    #         return max(lst)
        
    #     elif func == "count":
    #         return len(lst)
        
    #     elif func == "median":
    #         s = sorted(lst)
    #         n = len(s)
    #         if n % 2 == 1:
    #             return s[n // 2]
    #         return (s[n // 2 - 1] + s[n // 2]) / 2
        
    #     elif func == "variance":
    #         mean = sum(lst) / len(lst)
    #         return sum((x - mean) ** 2 for x in lst) / len(lst)
        
    #     elif func == "std":
    #         mean = sum(lst) / len(lst)
    #         var = sum((x - mean) ** 2 for x in lst) / len(lst)
    #         return math.sqrt(var)
        
    #     else:
    #         raise Exception(f"Unknown statistical function: {func}")

    def compute_stat(self, func, lst):
        """Compute statistical function on list"""

        # Functions that work on empty list
        if func == "count":
            return len(lst)

        if func == "sum":
            return sum(lst)

        # If empty and function requires data, throw error
        if not lst:
            raise Exception(f"Cannot compute {func} on empty list")

        if func == "mean":
            return sum(lst) / len(lst)
        
        elif func == "min":
            return min(lst)
        
        elif func == "max":
            return max(lst)
        
        elif func == "median":
            s = sorted(lst)
            n = len(s)
            if n % 2 == 1:
                return s[n // 2]
            return (s[n // 2 - 1] + s[n // 2]) / 2
        
        elif func == "variance":
            mean = sum(lst) / len(lst)
            return sum((x - mean) ** 2 for x in lst) / len(lst)
        
        elif func == "std":
            mean = sum(lst) / len(lst)
            var = sum((x - mean) ** 2 for x in lst) / len(lst)
            return math.sqrt(var)
        
        else:
            raise Exception(f"Unknown statistical function: {func}")


    def set_operation(self, op, a, b):
        """Perform set operation on two lists"""
        if op == "union":
            # Preserve order, remove duplicates
            result = list(dict.fromkeys(a + b))
            return result
        
        elif op == "intersection":
            # Elements in both lists
            return list(set(a) & set(b))
        
        elif op == "difference":
            # Elements in a but not in b
            return list(set(a) - set(b))
        
        else:
            raise Exception(f"Unknown set operation: {op}")

    # ------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------
    
    def dump_memory(self):
        """Print current memory state (for debugging)"""
        print("\n=== MEMORY DUMP ===")
        for name, value in sorted(self.memory.items()):
            if isinstance(value, list):
                print(f"{name} = {value}")
            else:
                print(f"{name} = {value}")
        print("==================\n")