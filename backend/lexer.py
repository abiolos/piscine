import re

TOKENS = [
    ('STRING',   r'"[^"\n]*"'),                # 🔹 Chaînes de caractères
    ('NUMBER',   r'\d+'),
    ('IDENT',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',   r'->'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('OP',       r'[+\-*/<>=!]+'),
    ('SEMICOLON', r';'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
]

KEYWORDS = {'while', 'if', 'else', 'print'}

def lexer(code):
    tokens = []
    i = 0
    while i < len(code):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, i)
            if match:
                text = match.group(0)
                if token_type == 'IDENT' and text in KEYWORDS:
                    tokens.append(('KEYWORD', text))
                elif token_type == 'STRING':
                    tokens.append(('STRING', text[1:-1]))  # 🔹 Retire les guillemets
                elif token_type not in ('SKIP', 'NEWLINE'):
                    tokens.append((token_type, text))
                i = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Caractère inattendu : {code[i]}")
    tokens.append(('EOF', None))
    return tokens
