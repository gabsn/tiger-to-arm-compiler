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
        op = binop.op
        if op == '&':
            left = binop.left.accept(self)
            if not left:
                return 0;
            elif binop.right.accept(self):
                return 1
            else:
                return 0
        elif op == '|':
            left = binop.left.accept(self)
            if left:
                return 1
            elif binop.right.accept(self):
                return 1
            else:
                return 0
        else: 
            left, right = binop.left.accept(self), binop.right.accept(self)
            if op == '+':
                return left + right
            elif op == '*':
                return left * right
            elif op == '/':
                return left // right
            elif op == '-':
                return left - right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == '=':
                if left == right:
                    return 1
                else:
                    return 0
            elif op == '<>':
                return left != right
            elif op == ':=':
                return right
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

    @visitor(SeqExp)
    def visit(self, seq):
        if len(seq.exps) == 0:
            return None
        else:
            for x in seq.exps[:-1]: 
                x.accept(self)
            return seq.exps[-1].accept(self)

        

