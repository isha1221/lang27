from langParser import FunctionCall, LengthFunction, LoopStatement


class Interpreter:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        """Evaluate a node in the AST"""
        from langParser import Number, String, Variable, BinOp, Assignment, Print, IfStatement

        if isinstance(node, Number):
            return node.value

        elif isinstance(node, String):
            return node.value

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
        elif isinstance(node, FunctionCall):
            if node.name == "len":  # Handling built-in length() function
                if len(node.args) != 1:
                    raise TypeError(
                        "len() function expects exactly one argument")
                return self.evaluate(LengthFunction(node.args[0]))

            raise NameError(f"Undefined function: '{node.name}'")

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
