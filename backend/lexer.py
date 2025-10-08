import re

TOKENS = [
    ('STRING',    r'"[^"\n]*"|\'[^\'\n]*\''),  # support double et simple quotes
    ('NUMBER',    r'\d+(?:\.\d+)?'),
    ('IDENT',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',    r'->'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACKET',  r'\['),
    ('RBRACKET',  r'\]'),
    ('COMMA',     r','),
    ('SEMICOLON', r';'),
    ('OP',        r'(?:>=|<=|==|!=)|[+\-*/<>!]'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('COMMENT',   r'//.*'),
]

KEYWORDS = {'while', 'if', 'elseif', 'else', 'print', 'func', 'ret', 'for'}

_regex_list = [(typ, re.compile(pat)) for typ, pat in TOKENS]

def lexer(code):
    tokens = []
    i = 0
    while i < len(code):
        match = None
        for token_type, regex in _regex_list:
            m = regex.match(code, i)
            if m:
                text = m.group(0)
                match = True
                if token_type == 'IDENT' and text in KEYWORDS:
                    tokens.append(('KEYWORD', text))
                elif token_type == 'STRING':
                    tokens.append(('STRING', text[1:-1]))  # supprime les quotes
                elif token_type == 'NUMBER':
                    tokens.append(('NUMBER', text))
                elif token_type in ('SKIP', 'COMMENT', 'NEWLINE'):
                    pass
                else:
                    tokens.append((token_type, text))
                i = m.end(0)
                break
        if not match:
            raise SyntaxError(f"Caractère inattendu: {code[i]!r} à la position {i}")
    tokens.append(('EOF', None))
    return tokens
