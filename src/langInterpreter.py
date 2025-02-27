class Interpreter:
    def __init__(self):
        self.variables = {}
        
    def evaluate(self, node):
        """Evaluate a node in the AST"""
        # Import node types here to avoid circular imports
        from langParser import Number, String, Variable, BinOp, Assignment, Print, IfStatement
        
        if isinstance(node, Number):
            return node.value
            
        elif isinstance(node, String):
            return node.value
            
        elif isinstance(node, Variable):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f"Variable '{node.name}' is not defined")
                
        elif isinstance(node, BinOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            
            if node.op == '+': return left + right
            if node.op == '-': return left - right
            if node.op == '*': return left * right
            if node.op == '/': 
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            if node.op == '==': return left == right
            if node.op == '!=': return left != right
            if node.op == '<': return left < right
            if node.op == '>': return left > right
            if node.op == '<=': return left <= right
            if node.op == '>=': return left >= right
            
            raise ValueError(f"Unknown operator: {node.op}")
            
        elif isinstance(node, Assignment):
            value = self.evaluate(node.expr)
            self.variables[node.name] = value
            return value
            
        elif isinstance(node, Print):
            value = self.evaluate(node.expr)
            print(value)
            return value
            
        elif isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                return self.execute_block(node.body)
            elif node.else_body:
                if isinstance(node.else_body, list):
                    return self.execute_block(node.else_body)
                else:
                    # Handle nested if statements in else clause
                    return self.evaluate(node.else_body)
            return None
            
        else:
            raise TypeError(f"Unknown node type: {type(node)}")
    
    def execute_block(self, statements):
        """Execute a block of statements"""
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