from langParser import FunctionCall, FunctionDefinition, LengthFunction, LoopStatement, Input, ReturnStatement
from langParser import Number, Decimal, String, Character, Boolean, Variable, TypedVariable, TypedAssignment, BinOp, Assignment, Print, IfStatement


class Interpreter:
    def __init__(self):
        self.variables = {}  # Global variables
        self.functions = {}  # Store function definitions
        
    def call_function(self, name, args):
        # Handle built-in functions
        if name == "to_num":
            if len(args) != 1:
                raise TypeError("to_num() function expects exactly one argument")
            arg = args[0]
            if isinstance(arg, str):
                try:
                    return int(arg)
                except ValueError:
                    try:
                        return float(arg)
                    except ValueError:
                        raise ValueError(f"Cannot convert '{arg}' to number")
            elif isinstance(arg, (int, float)):
                return arg
            else:
                raise TypeError(f"Cannot convert {type(arg)} to number")
                
        # Handle user-defined functions
        if name not in self.functions:
            raise NameError(f"Undefined function: '{name}'")
            
        func_def = self.functions[name]
        
        if len(args) != len(func_def.parameters):
            raise TypeError(f"Function {name} expected {len(func_def.parameters)} arguments, got {len(args)}")
            
        # Create a new scope for function variables
        old_variables = self.variables.copy()
        
        # Set up parameters in the function scope
        self.variables = {}
        for param_name, arg_value in zip(func_def.parameters, args):
            self.variables[param_name] = arg_value
            
        # Execute function body
        result = None
        try:
            for statement in func_def.body:
                result = self.evaluate(statement)
                # If we hit a return statement, exit early
                if isinstance(statement, ReturnStatement):
                    break
        finally:
            # Restore global scope when function ends
            self.variables = old_variables
            
        return result    

    def evaluate(self, node):
        """Evaluate a node in the AST"""
        if isinstance(node, FunctionDefinition):
            self.functions[node.name] = node
            return None
            
        elif isinstance(node, ReturnStatement):
            return self.evaluate(node.expr)
            
        elif isinstance(node, FunctionCall):
            if node.name == "len":  # Handle built-in len function
                if len(node.args) != 1:
                    raise TypeError("len() function expects exactly one argument")
                return self.evaluate(LengthFunction(node.args[0]))
                
            # Evaluate all argument expressions
            evaluated_args = [self.evaluate(arg) for arg in node.args]
            
            # Call the function
            return self.call_function(node.name, evaluated_args)

        if isinstance(node, Number):
            return node.value

        elif isinstance(node, Decimal):
            return node.value
            
        elif isinstance(node, Character):
            return node.value
            
        elif isinstance(node, Boolean):
            return node.value

        elif isinstance(node, String):
            return node.value
            
        elif isinstance(node, TypedVariable):
            # Just declare a variable with default value based on type
            if node.type_name == 'num ':
                self.variables[node.name] = 0
            elif node.type_name == 'dec':
                self.variables[node.name] = 0.0
            elif node.type_name == 'str':
                self.variables[node.name] = ""
            elif node.type_name == 'chr':
                self.variables[node.name] = ''
            elif node.type_name == 'bool':
                self.variables[node.name] = False
            return None
            
        elif isinstance(node, TypedAssignment):
            value = self.evaluate(node.expr)
            
            # Type checking
            if node.type_name == 'num ' and not isinstance(value, int):
                raise TypeError(f"Cannot assign {type(value)} to num variable '{node.name}'")
            elif node.type_name == 'dec' and not (isinstance(value, float) or isinstance(value, int)):
                # Allow integers to be assigned to decimal variables
                if isinstance(value, int):
                    value = float(value)  # Convert int to float
                else:
                    raise TypeError(f"Cannot assign {type(value)} to dec variable '{node.name}'")
            elif node.type_name == 'str' and not isinstance(value, str):
                raise TypeError(f"Cannot assign {type(value)} to str variable '{node.name}'")
            elif node.type_name == 'chr' and (not isinstance(value, str) or len(value) != 1):
                raise TypeError(f"Cannot assign {type(value)} to chr variable '{node.name}'")
            elif node.type_name == 'bool' and not isinstance(value, bool):
                raise TypeError(f"Cannot assign {type(value)} to bool variable '{node.name}'")
                
            self.variables[node.name] = value
            return value

        elif isinstance(node, Variable):
            if node.name in self.variables:
                return self.variables[node.name]
            raise NameError(f"Undefined variable: '{node.name}'")

        elif isinstance(node, BinOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == '+':
                return left + right
            if node.op == '-':
                return left - right
            if node.op == '*':
                return left * right
            if node.op == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            if node.op == '==':
                return left == right
            if node.op == '!=':
                return left != right
            if node.op == '<':
                return left < right
            if node.op == '>':
                return left > right
            if node.op == '<=':
                return left <= right
            if node.op == '>=':
                return left >= right

            raise ValueError(f"Unknown operator: {node.op}")

        elif isinstance(node, Assignment):
            value = self.evaluate(node.expr)
            self.variables[node.name] = value
            return value

        elif isinstance(node, Print):
            value = self.evaluate(node.expr)
            print(value)
            return value
        
        elif isinstance(node, Input):
            # Get the prompt if provided
            prompt = ""
            if node.prompt is not None:
                prompt = node.prompt
                print(prompt, end='')
            
            # Get the input type if provided (defaults to string)
            input_type = node.input_type if hasattr(node, 'input_type') else 'str'
            
            # Get user input
            user_input = input()
            
            # Convert the input based on the specified type
            if input_type == 'num ':
                try:
                    return int(user_input)
                except ValueError:
                    raise ValueError(f"Cannot convert input '{user_input}' to num")
            elif input_type == 'dec':
                try:
                    return float(user_input)
                except ValueError:
                    raise ValueError(f"Cannot convert input '{user_input}' to dec")
            elif input_type == 'bool':
                lower_input = user_input.lower()
                if lower_input in ('true', 'yes', 'y', '1'):
                    return True
                elif lower_input in ('false', 'no', 'n', '0'):
                    return False
                else:
                    raise ValueError(f"Cannot convert input '{user_input}' to bool")
            elif input_type == 'chr':
                if len(user_input) != 1:
                    raise ValueError(f"Input '{user_input}' is not a single character")
                return user_input
            else:  # Default to string
                return user_input

        elif isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                return self.execute_block(node.body)
            return self.execute_block(node.else_body) if node.else_body else None

        elif isinstance(node, LoopStatement):
            self.evaluate(node.init)
            while self.evaluate(node.condition):
                self.execute_block(node.body)
                self.evaluate(node.update)
            return None

        elif isinstance(node, LengthFunction):
            expr_value = self.evaluate(node.expr)
            if isinstance(expr_value, str) or isinstance(expr_value, list):
                return len(expr_value)
            raise TypeError("len() function only applies to strings and lists")

        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def execute_block(self, statements):
        """Execute a block of statements"""
        if statements is None:
            return None
            
        result = None
        for statement in statements:
            result = self.evaluate(statement)
        return result

    def run(self, ast):
        """Run the program represented by the AST"""
        result = None
        for node in ast:
            result = self.evaluate(node)
        return result
