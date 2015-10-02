from ast.nodes import *
from utils.visitor import visitor

class Evaluator:
    """This contains a simple evaluator visitor which computes the value
    of a tiger expression."""

    @visitor(IntegerLiteral)
    def visit(self, int):
        return int.intValue

    @visitor(BinaryOperator)
    def visit(self, binop):
        left, right = binop.left.accept(self), binop.right.accept(self)
        op = binop.op
        if op == '+':
            return left + right
        elif op == '*':
            return left * right
        elif op == '-':
            return left - right
        elif op == '/':
            return left / right
        elif op == '&':
            return left and right
        elif op == '|':
            return left or right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '<>':
            return left != right

        else:
            raise SyntaxError("unknown operator %s" % op)

    @visitor(IfThenElse)
    def visit(self, cond):
        condition = cond.condition.accept(self) 
        if condition:
            return cond.then_part.accept(self)
        else:
            return cond.else_part.accept(self)
    
    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
