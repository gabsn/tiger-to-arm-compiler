from ast.nodes import *
from utils.visitor import *


class Dumper(Visitor):

    def __init__(self, semantics=False):
        """Initialize a new Dumper visitor. If semantics is True,
        additional information will be printed along with declarations
        and identifiers."""
        self.semantics = semantics

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to dump %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        return str(i.intValue)

    @visitor(BinaryOperator)
    def visit(self, binop):
        # Always use parentheses to reflect grouping and associativity,
        # even if they may be superfluous.
        return "(%s %s %s)" % \
               (binop.left.accept(self), binop.op, binop.right.accept(self))

    @visitor(Identifier)
    def visit(self, id):
        if self.semantics:
            diff = id.depth - id.decl.depth
            scope_diff = "/*%d*/" % diff if diff else ''
        else:
            scope_diff = ''
        return '%s%s' % (id.name, scope_diff)


    @visitor(IfThenElse)
    def visit(self, cond):
        return "if %s then %s else %s" % (cond.condition.accept(self), cond.then_part.accept(self), cond.else_part.accept(self))

    @visitor(VarDecl)
    def visit(self, var):
        if self.semantics and var.escapes == True:
            return "var %s/*e*/ := %s" % (var.name, var.exp.accept(self))
        else:
            return "var %s := %s" % (var.name, var.exp.accept(self))

    @visitor(FunDecl)
    def visit(self, fun):
        args = ""
        l = fun.args
        if len(l) == 1:
            args = args + l[0].name
        elif len(l) > 1:
            for i in range(len(l)-1):
                args = args + l[i].name + ", "
            args = args + l[len(l)-1].name 
        return "%s(%s) = %s" % (fun.name, args, fun.exp.accept(self))

    @visitor(FunCall)
    def visit(self, fun):
        args = ""
        l = fun.params
        if len(l) == 1:
            args = args + l[0].accept(self)
        elif len(l) > 1:
            for i in range(len(l)-1):
                args = args + l[i].accept(self) + ", "
            args = args + l[len(l)-1].accept(self)
        return "%s(%s)" % (fun.identifier, args)

# la fonction tuple() permet de transformer une liste en une séquence
    @visitor(Let)
    def visit(self, let):
        decls, exps = "", ""
        for x in let.decls:
            decls = decls + x.accept(self) + " "
        for y in let.exps:
            exps = exps + y.accept(self) + " "
        return "let %s in %s end" % (decls, exps)
