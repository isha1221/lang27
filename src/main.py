import sys
import os
from lexer import tokenize
from langParser import Parser
from langInterpreter import Interpreter

def show_usage():
    print("Usage: python main2.py <filename.lip> [--debug=true] [--version] [--help]")
    print("\nOptions:")
    print("  --debug=true   Enable debug mode to show detailed execution steps")
    print("  --version      Show the interpreter version")
    print("  --help         Display this help message")

def show_version():
    print("Lang27 v0.0.3")

def run_code(code, debug=False):
    """Run a program written in our custom language"""
    try:
        if debug:
            print("Starting lexical analysis...")
        
        tokens = tokenize(code)
        
        if debug:
            print("Tokens generated:")
            for i, token in enumerate(tokens):
                print(f"  {i}: {token}")
        
        if debug:
            print("\nStarting parsing...")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if debug:
            print("AST generated:")
            for i, node in enumerate(ast):
                print(f"  {i}: {node}")
        
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
        return run_code(code, debug)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Main execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "--help" in sys.argv:
            show_usage()
            sys.exit(0)
        if "--version" in sys.argv:
            show_version()
            sys.exit(0)
        
        file_path = sys.argv[1]
        debug_mode = any(arg == "--debug=true" for arg in sys.argv)
        run_file(file_path, debug=debug_mode)
    else:
        show_usage()
