class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def eat(self, token_type=None, value=None):
        tok_type, tok_val = self.current()
        if token_type and tok_type != token_type:
            raise SyntaxError(f"Attendu {token_type}, trouvé {tok_type}")
        if value and tok_val != value:
            raise SyntaxError(f"Attendu {value}, trouvé {tok_val}")
        self.pos += 1
        return tok_val

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            statements.append(self.statement())
        return ('block', statements)

    def statement(self):
        tok_type, tok_val = self.current()

        if tok_type == 'IDENT':
            return self.assignment()
        elif tok_type == 'KEYWORD':
            if tok_val == 'while':
                return self.while_stmt()
            elif tok_val == 'if':
                return self.if_stmt()
            elif tok_val == 'print':
                return self.print_stmt()
        else:
            raise SyntaxError(f"Instruction inattendue : {self.current()}")

    def assignment(self):
        var_name = self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expression()
        return ('assign', var_name, expr)

    def while_stmt(self):
        self.eat('KEYWORD', 'while')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        body = self.block()
        return ('while', condition, body)

    def if_stmt(self):
        self.eat('KEYWORD', 'if')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        if_body = self.block()
        else_body = None
        if self.current() == ('KEYWORD', 'else'):
            self.eat('KEYWORD', 'else')
            else_body = self.block()
        return ('if', condition, if_body, else_body)

    def print_stmt(self):
        self.eat('KEYWORD', 'print')
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        return ('print', expr)

    def block(self):
        self.eat('LBRACE')
        statements = []
        while self.current()[0] != 'RBRACE':
            statements.append(self.statement())
        self.eat('RBRACE')
        return ('block', statements)

    def expression(self):
        tok_type, tok_val = self.current()
        if tok_type == 'NUMBER':
            self.eat('NUMBER')
            return ('number', int(tok_val))
        elif tok_type == 'IDENT':
            self.eat('IDENT')
            return ('var', tok_val)
        elif tok_type == 'STRING':
            self.eat('STRING')
            return ('string', tok_val)
        else:
            raise SyntaxError(f"Expression invalide : {self.current()}")
