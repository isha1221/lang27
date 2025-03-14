import re

TOKEN_SPEC = [
    ('PRINT',     r'drucken'),           # Print statement
    ('IF',        r'if'),                # If statement
    ('ELF',       r'elf'),               # Else if statement
    ('ELSE',      r'el'),                # Else statement
    ('FOR',       r'for'),               # for loop
    ('INPUT',     r'eingabe'),          # Input function
    ('FUNCTION',  r'func'),              # Function declaration
    ('TYPE_NUM',  r'num '),               # Number type declaration
    ('TYPE_STR',  r'str'),               # String type declaration
    ('TYPE_DEC',  r'dec'),               # Decimal/float type declaration
    ('TYPE_CHR',  r'chr'),               # Character type declaration
    ('TYPE_BOOL', r'bool'),              # Boolean type declaration
    ('BOOL_TRUE', r'true'),              # Boolean true value
    ('BOOL_FALSE',r'false'),             # Boolean false value
    ('DECIMAL',   r'\d+\.\d+'),          # Decimal number (must be before NUMBER)
    ('RETURN',    r'return'),            # Return statement
    ('COMMA',     r','),                 # Comma for separating parameters
    ('EQ',        r'=='),                # Equals (must be before ASSIGN)
    ('NEQ',       r'!='),                # Not Equals
    ('LE',        r'<='),                # Less Than or Equal
    ('GE',        r'>='),                # Greater Than or Equal
    ('ASSIGN',    r'='),                 # Assignment
    ('SEMICOLON',     r';'),             # Semicolon
    ('LT',        r'<'),                 # Less Than
    ('GT',        r'>'),                 # Greater Than
    ('NUMBER',    r'\d+'),               # Integer
    ('STRING',    r'(["\'])(?:(?=(\\?))\2.)*?\1'),  # Matches "text" or 'text'
    ('IDENT',     r'[a-zA-Z_]\w*'),      # Variable names
    ('PLUS',      r'\+'),                # Addition
    ('MINUS',     r'-'),                 # Subtraction
    ('MUL',       r'\*'),                # Multiplication
    ('DIV',       r'/'),                 # Division
    ('LPAREN',    r'\('),                # Left Parenthesis
    ('RPAREN',    r'\)'),                # Right Parenthesis
    ('LBRACE',    r'\{'),                # Left Brace
    ('RBRACE',    r'\}'),                # Right Brace
    ('NEWLINE',   r'\n'),                # Newline
    ('SKIP',      r'[ \t]+'),            # Spaces and tabs (ignored)
]


def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_SPEC:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'STRING':
                    # Remove surrounding quotes
                    tokens.append((token_type, text[1:-1]))
                elif token_type == 'NUMBER':
                    # Convert to integer
                    tokens.append((token_type, int(text)))
                elif token_type == 'DECIMAL':
                    # Convert to float
                    tokens.append((token_type, float(text)))
                elif token_type == 'BOOL_TRUE':
                    tokens.append((token_type, True))
                elif token_type == 'BOOL_FALSE':
                    tokens.append((token_type, False))
                elif token_type in ('SKIP', 'NEWLINE'):
                    pass  # Ignore spaces and newlines
                else:
                    tokens.append((token_type, text))
                pos += len(text)
                break
        if not match:
            raise SyntaxError(
                f"Unexpected character: {code[pos]} at position {pos}")
    return tokens