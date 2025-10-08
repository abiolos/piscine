class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.global_env = {}
        # ajouter builtin
        self.global_env.update({
            'print': ('__builtin_print__', None),
            'append': ('__builtin_append__', None),
        })

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env
        ntype = node[0]

        if ntype == 'block':
            result = None
            for stmt in node[1]:
                result = self.eval(stmt, env)
            return result

        if ntype == 'assign':
            _, name, expr = node
            val = self.eval(expr, env)
            env[name] = val
            return val

        if ntype == 'index_assign':
            _, name, idx_node, expr = node
            idx = self.eval(idx_node, env)
            val = self.eval(expr, env)
            if name not in env:
                raise NameError(f"Variable non définie: {name}")
            target = env[name]
            if not isinstance(target, list):
                raise TypeError("Indexation sur un non-tableau")
            target[idx] = val
            return val

        if ntype == 'number':
            return node[1]
        if ntype == 'string':
            return node[1]
        if ntype == 'list':
            return [self.eval(elem, env) for elem in node[1]]
        if ntype == 'var':
            name = node[1]
            if name in env:
                val = env[name]
                return val
            raise NameError(f"Variable non définie: {name}")

        if ntype == 'index':
            _, container_node, idx_node = node
            container = self.eval(container_node, env)
            idx = self.eval(idx_node, env)
            return container[idx]

        if ntype == 'expr_stmt':
            return self.eval(node[1], env)

        if ntype == 'print':
            val = self.eval(node[1], env)
            print(val)
            return val

        if ntype == 'binop':
            _, op, left_node, right_node = node
            a = self.eval(left_node, env)
            b = self.eval(right_node, env)
            if op == '+':
                return a + b
            if op == '-':
                return a - b
            if op == '*':
                return a * b
            if op == '/':
                return a / b
            if op == '==':
                return a == b
            if op == '!=':
                return a != b
            if op == '<':
                return a < b
            if op == '>':
                return a > b
            if op == '<=':
                return a <= b
            if op == '>=':
                return a >= b
            raise RuntimeError(f"Opérateur inconnu: {op}")

        if ntype == 'unary':
            _, op, node1 = node
            v = self.eval(node1, env)
            if op == '-':
                return -v
            if op == '!':
                return not v

        if ntype == 'if':
            _, cond, if_body, elifs, else_body = node
            if self.eval(cond, env):
                return self.eval(if_body, dict(env))
            for c, b in elifs:
                if self.eval(c, env):
                    return self.eval(b, dict(env))
            if else_body:
                return self.eval(else_body, dict(env))
            return None

        if ntype == 'while':
            _, cond, body = node
            while self.eval(cond, env):
                self.eval(body, dict(env))
            return None

        if ntype == 'for':
            _, init, cond, post, body = node
            local = dict(env)
            if init:
                if init[0] == 'assign' or init[0] == 'index_assign':
                    self.eval(init, local)
                else:
                    self.eval(init, local)
            while True:
                if cond:
                    if not self.eval(cond, local):
                        break
                else:
                    # condition omitted -> true by default
                    pass
                self.eval(body, dict(local))
                if post:
                    self.eval(post, local)
            return None

        if ntype == 'func_def':
            _, name, params, body = node
            env[name] = ('user_func', params, body)
            return None

        if ntype == 'call':
            _, name, args = node
            # builtins
            if name == 'print':
                vals = [self.eval(a, env) for a in args]
                print(*vals)
                return None
            if name == 'append':
                if len(args) != 2:
                    raise TypeError('append requires 2 arguments')
                arr = self.eval(args[0], env)
                val = self.eval(args[1], env)
                if not isinstance(arr, list):
                    raise TypeError('append: premier argument doit être un tableau')
                arr.append(val)
                return None
            # user func
            if name not in env:
                raise NameError(f"Fonction non définie: {name}")
            entry = env[name]
            if entry[0] == 'user_func':
                _, params, body = entry
                if len(params) != len(args):
                    raise TypeError('Nombre d\'arguments incorrect')
                local = dict(env)
                for p, a in zip(params, args):
                    local[p] = self.eval(a, env)
                try:
                    self.eval(body, local)
                except ReturnException as r:
                    return r.value
                return None
            raise RuntimeError('Type de fonction non supporté')

        if ntype == 'ret':
            _, val_node = node
            val = None
            if val_node is not None:
                val = self.eval(val_node, env)
            raise ReturnException(val)

        raise RuntimeError(f"Nœud inconnu: {ntype}")
