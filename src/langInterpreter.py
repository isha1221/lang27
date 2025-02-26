from langParser import Parser, String
from lexer import tokenize
from langParser import Assignment, BinOp, IfStatement, Number, Print, Variable

variables = {}

def evaluate(node):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    elif isinstance(node, Variable):
        return variables.get(node.name, 0)
    elif isinstance(node, BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == '+': return left + right
        if node.op == '-': return left - right
        if node.op == '*': return left * right
        if node.op == '/': return left / right
        if node.op == '==': return left == right
        if node.op == '!=': return left != right
        if node.op == '<': return left < right
        if node.op == '>': return left > right
        if node.op == '<=': return left <= right
        if node.op == '>=': return left >= right
    elif isinstance(node, Assignment):
        variables[node.name] = evaluate(node.expr)
    elif isinstance(node, Print):
        print(evaluate(node.expr))
    elif isinstance(node, IfStatement):
        if evaluate(node.condition):
            for stmt in node.body:
                evaluate(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                evaluate(stmt)
