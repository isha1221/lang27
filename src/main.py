import sys
from lexer import tokenize
from langParser import Parser
from langInterpreter import evaluate

def run_lip_file(filename):
    with open(filename, 'r') as file:
        code = file.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    for stmt in ast:
        evaluate(stmt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.lip>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".lip"):
        print("Error: Only .lip files are supported!")
        sys.exit(1)

    run_lip_file(filename)
