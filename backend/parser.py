from collections import namedtuple

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def eat(self, expected_type=None, expected_val=None):
        tok_type, tok_val = self.current()
        if expected_type and tok_type != expected_type:
            raise SyntaxError(f"Attendu {expected_type}, trouvé {tok_type} ({tok_val})")
        if expected_val and tok_val != expected_val:
            raise SyntaxError(f"Attendu {expected_val}, trouvé {tok_val}")
        self.pos += 1
        return tok_val

    def parse(self):
        stmts = []
        while self.current()[0] != 'EOF':
            stmts.append(self.statement())
        return ('block', stmts)

    def statement(self):
        tok_type, tok_val = self.current()
        if tok_type == 'KEYWORD':
            if tok_val == 'if':
                return self.if_stmt()
            if tok_val == 'while':
                return self.while_stmt()
            if tok_val == 'for':
                return self.for_stmt()
            if tok_val == 'print':
                return self.print_stmt()
            if tok_val == 'func':
                return self.func_def()
            if tok_val == 'ret':
                return self.ret_stmt()
        elif tok_type == 'IDENT':
            nxt = self.tokens[self.pos+1] if self.pos+1 < len(self.tokens) else ('EOF', None)
            if nxt[0] == 'ASSIGN':
                return self.assignment()
            elif nxt[0] == 'LPAREN':
                expr = self.expression()
                return ('expr_stmt', expr)
            elif nxt[0] == 'LBRACKET':
                expr = self.expression()
                return ('expr_stmt', expr)
        else:
            # Si ce n’est pas KEYWORD ou IDENT, on tente quand même une expression
            expr = self.expression()
            return ('expr_stmt', expr)

        raise SyntaxError(f"Instruction inattendue: {self.current()}")

    def assignment(self):
        name = self.eat('IDENT')
        if self.current()[0] == 'LBRACKET':
            self.eat('LBRACKET')
            idx = self.expression()
            self.eat('RBRACKET')
            self.eat('ASSIGN')
            expr = self.expression()
            return ('index_assign', name, idx, expr)
        else:
            self.eat('ASSIGN')
            expr = self.expression()
            return ('assign', name, expr)

    def for_stmt(self):
        self.eat('KEYWORD', 'for')
        self.eat('LPAREN')
        # init
        init = None
        if self.current()[0] != 'SEMICOLON':
            if self.current()[0] == 'IDENT' and self.tokens[self.pos+1][0] == 'ASSIGN':
                init = self.assignment()
            else:
                init = ('expr_stmt', self.expression())
        self.eat('SEMICOLON')
        # condition
        cond = None
        if self.current()[0] != 'SEMICOLON':
            cond = self.expression()
        self.eat('SEMICOLON')
        # post
        post = None
        if self.current()[0] != 'RPAREN':
            if self.current()[0] == 'IDENT' and self.tokens[self.pos+1][0] == 'ASSIGN':
                post = self.assignment()
            else:
                post = ('expr_stmt', self.expression())
        self.eat('RPAREN')
        body = self.block()
        return ('for', init, cond, post, body)

    def if_stmt(self):
        self.eat('KEYWORD', 'if')
        self.eat('LPAREN')
        cond = self.expression()
        self.eat('RPAREN')
        if_body = self.block()
        elifs = []
        else_body = None
        while self.current() == ('KEYWORD', 'elseif'):
            self.eat('KEYWORD', 'elseif')
            self.eat('LPAREN')
            c = self.expression()
            self.eat('RPAREN')
            b = self.block()
            elifs.append((c, b))
        if self.current() == ('KEYWORD', 'else'):
            self.eat('KEYWORD', 'else')
            else_body = self.block()
        return ('if', cond, if_body, elifs, else_body)

    def while_stmt(self):
        self.eat('KEYWORD', 'while')
        self.eat('LPAREN')
        cond = self.expression()
        self.eat('RPAREN')
        body = self.block()
        return ('while', cond, body)

    def print_stmt(self):
        self.eat('KEYWORD', 'print')
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        return ('print', expr)

    def func_def(self):
        self.eat('KEYWORD', 'func')
        name = self.eat('IDENT')
        self.eat('LPAREN')
        params = []
        if self.current()[0] != 'RPAREN':
            params.append(self.eat('IDENT'))
            while self.current()[0] == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENT'))
        self.eat('RPAREN')
        body = self.block()
        return ('func_def', name, params, body)

    def ret_stmt(self):
        self.eat('KEYWORD', 'ret')
        val = None
        if self.current()[0] not in ('SEMICOLON', 'RBRACE'):
            val = self.expression()
        return ('ret', val)

    def block(self):
        self.eat('LBRACE')
        stmts = []
        while self.current()[0] != 'RBRACE':
            stmts.append(self.statement())
        self.eat('RBRACE')
        return ('block', stmts)

    # =====================
    # Expression parsing avec priorité
    # =====================

    def expression(self):
        return self._equality()

    def _equality(self):
        node = self._comparison()
        while self.current()[0] == 'OP' and self.current()[1] in ('==', '!='):
            op = self.eat('OP')
            right = self._comparison()
            node = ('binop', op, node, right)
        return node

    def _comparison(self):
        node = self._term()
        while self.current()[0] == 'OP' and self.current()[1] in ('<', '>', '<=', '>='):
            op = self.eat('OP')
            right = self._term()
            node = ('binop', op, node, right)
        return node

    def _term(self):
        node = self._factor()
        while self.current()[0] == 'OP' and self.current()[1] in ('+', '-'):
            op = self.eat('OP')
            right = self._factor()
            node = ('binop', op, node, right)
        return node

    def _factor(self):
        node = self._unary()
        while self.current()[0] == 'OP' and self.current()[1] in ('*', '/'):
            op = self.eat('OP')
            right = self._unary()
            node = ('binop', op, node, right)
        return node

    def _unary(self):
        if self.current()[0] == 'OP' and self.current()[1] in ('-', '!'):
            op = self.eat('OP')
            node = self._unary()
            return ('unary', op, node)
        return self._primary()

    def _primary(self):
        tok_type, tok_val = self.current()
        if tok_type == 'NUMBER':
            self.eat('NUMBER')
            if '.' in tok_val:
                return ('number', float(tok_val))
            else:
                return ('number', int(tok_val))
        if tok_type == 'STRING':
            self.eat('STRING')
            return ('string', tok_val)
        if tok_type == 'IDENT':
            name = self.eat('IDENT')
            # appel fonction
            if self.current()[0] == 'LPAREN':
                self.eat('LPAREN')
                args = []
                if self.current()[0] != 'RPAREN':
                    args.append(self.expression())
                    while self.current()[0] == 'COMMA':
                        self.eat('COMMA')
                        args.append(self.expression())
                self.eat('RPAREN')
                node = ('call', name, args)
            else:
                node = ('var', name)
            # chainage index
            while self.current()[0] == 'LBRACKET':
                self.eat('LBRACKET')
                idx = self.expression()
                self.eat('RBRACKET')
                node = ('index', node, idx)
            return node
        if tok_type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        if tok_type == 'LBRACKET':
            self.eat('LBRACKET')
            elems = []
            if self.current()[0] != 'RBRACKET':
                elems.append(self.expression())
                while self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                    elems.append(self.expression())
            self.eat('RBRACKET')
            return ('list', elems)
        raise SyntaxError(f"Expression invalide: {self.current()}")
