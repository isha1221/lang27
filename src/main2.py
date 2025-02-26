import sys
import os
from lexer import tokenize
from parser2 import Parser
from interpreter2 import Interpreter

def run_code(code, debug=False):
    """Run a program written in our custom language"""
    # Lexical analysis: Convert code string to tokens
    try:
        if debug:
            print("Starting lexical analysis...")
        
        tokens = tokenize(code)
        
        if debug:
            print("Tokens generated:")
            for i, token in enumerate(tokens):
                print(f"  {i}: {token}")
        
        # Parsing: Convert tokens to abstract syntax tree
        if debug:
            print("\nStarting parsing...")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if debug:
            print("AST generated:")
            for i, node in enumerate(ast):
                print(f"  {i}: {node}")
        
        # Interpretation: Execute the abstract syntax tree
        if debug:
            print("\nStarting interpretation...")
        
        interpreter = Interpreter()
        result = interpreter.run(ast)
        
        if debug:
            print(f"\nFinal result: {result}")
            print("Final variable values:")
            for var, value in interpreter.variables.items():
                print(f"  {var} = {value}")
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return None

def run_file(file_path, debug=False):
    """Run a program from a .lip file"""
    if not file_path.endswith('.lip'):
        print(f"Error: File must have a .lip extension, got '{file_path}'")
        return None
    
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        # print(f"Running program from file: {file_path}")
        return run_code(code, debug)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Main execution
if __name__ == "__main__":
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        # Check for debug flag
        debug_mode = False
        for arg in sys.argv:
            if arg.startswith('--debug='):
                debug_value = arg.split('=')[1].lower()
                if debug_value == 'true':
                    debug_mode = True
        
        run_file(file_path, debug=debug_mode)
    else:
        print("No .lip file specified. Usage: python main2.py <filename.lip> [--debug=true]")