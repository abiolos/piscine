class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        ntype = node[0]

        if ntype == 'block':
            result = None
            for stmt in node[1]:
                result = self.eval(stmt)
            return result

        elif ntype == 'assign':
            _, name, expr = node
            value = self.eval(expr)
            self.env[name] = value
            return value

        elif ntype == 'number':
            return node[1]

        elif ntype == 'string':
            return node[1]

        elif ntype == 'var':
            name = node[1]
            if name in self.env:
                return self.env[name]
            else:
                raise NameError(f"Variable non définie : {name}")

        elif ntype == 'print':
            _, expr = node
            value = self.eval(expr)
            print(value)
            return value

        elif ntype == 'while':
            _, cond, body = node
            while self.eval(cond):
                self.eval(body)
            return None

        elif ntype == 'if':
            _, cond, if_body, else_body = node
            if self.eval(cond):
                return self.eval(if_body)
            elif else_body:
                return self.eval(else_body)

        else:
            raise RuntimeError(f"Nœud inconnu : {ntype}")
