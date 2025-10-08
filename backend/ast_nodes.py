"""
Définition des classes représentant les nœuds de l’arbre syntaxique abstrait (AST)
pour MiniLang.
"""

class Node:
    """Classe de base pour tous les nœuds AST."""
    pass


class NumberNode(Node):
    def __init__(self, value):
        self.value = value


class StringNode(Node):
    def __init__(self, value):
        self.value = value


class VarNode(Node):
    def __init__(self, name):
        self.name = name


class AssignNode(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class BinOpNode(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpNode(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr


class IfNode(Node):
    def __init__(self, cond, if_body, elifs=None, else_body=None):
        self.cond = cond
        self.if_body = if_body
        self.elifs = elifs or []
        self.else_body = else_body


class WhileNode(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class ForNode(Node):
    def __init__(self, init, cond, post, body):
        self.init = init
        self.cond = cond
        self.post = post
        self.body = body


class FuncDefNode(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class CallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class ReturnNode(Node):
    def __init__(self, expr):
        self.expr = expr


class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements
