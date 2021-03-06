from ast.nodes import *
from utils.visitor import *


class Dumper(Visitor):

    def __init__(self, semantics):
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
        if cond.else_part == None:
            return "if %s then %s" % (cond.condition.accept(self), cond.then_part.accept(self))
        else:
            return "if %s then %s else %s" % (cond.condition.accept(self), cond.then_part.accept(self), cond.else_part.accept(self))

    @visitor(VarDecl)
    def visit(self, var):
        t = ""
        if var.type != None:
            t = t + ": %s" % 'int'
        if self.semantics and var.escapes == True:
            return "var %s/*e*/%s := %s" % (var.name, t, var.exp.accept(self))
        else:
            return "var %s%s := %s" % (var.name, t, var.exp.accept(self))

    @visitor(FunDecl)
    def visit(self, fun):
        args = ""
        t = ""
        if fun.type != None:
            typef = fun.type.typename
            if typef != "void":
                t = t + ": %s" % typef
        l = fun.args
        if len(l) == 1:
            args = args + l[0].name + ": int"
        elif len(l) > 1:
            for i in range(len(l)-1):
                args = args + l[i].name + ": int, "
            args = args + l[len(l)-1].name + ":int"
        return "function %s(%s)%s = %s" % (fun.name, args, t, fun.exp.accept(self))

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
        return "%s(%s)" % (fun.identifier.name, args)


# la fonction tuple() permet de transformer une liste en une séquence
    @visitor(Let)
    def visit(self, let):
        decls, exps = "", ""
        for x in let.decls[:-1]:
            decls = decls + x.accept(self) + " "
        decls = decls + let.decls[-1].accept(self)
        if len(let.exps) > 0:
            for y in let.exps[:-1]:
                exps = exps + y.accept(self) + "; "
            exps = exps + let.exps[-1].accept(self)
        return "let %s in %s end" % (decls, exps)

    @visitor(SeqExp)
    def visit(self, seq):
        result = ""
        if len(seq.exps) == 1:
            result = seq.exps[0].accept(self)
            return result
        elif len(seq.exps) >1:
            result = result + seq.exps[0].accept(self)
            for i in range(1, len(seq.exps)):
                result = result + "; " + seq.exps[i].accept(self)
        return "(%s)" % (result)

    @visitor(Assignment)
    def visit(self, a):
        return "%s := %s" % (a.identifier.name, a.exp.accept(self))
            
    @visitor(While)
    def visit(self, w):
        return "while %s do %s" % (w.condition.accept(self), w.exp.accept(self))

    @visitor(For)
    def visit(self, f):
        return "for %s := %s to %s do %s" % (f.indexdecl.name, f.low_bound.accept(self), f.high_bound.accept(self), f.exp.accept(self))

    @visitor(Break)
    def visit(self, b):
        return "break"
