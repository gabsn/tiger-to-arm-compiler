from ast.nodes import *
from utils.visitor import *


class BindException(Exception):
    """Exception encountered during the binding phase."""
    pass


class Binder(Visitor):
    """The binder takes care of linking identifier uses to its declaration. If
    will also remember the depth of every declaration and every identifier,
    and mark a declaration as escaping if it is accessed from a greater depth
    than its definition.

    A new scope is pushed every time a let or a function declaration is
    encountered. It is not allowed to have the same name present several
    times in the same scope.

    The depth is increased every time a function declaration is encountered,
    and restored afterwards."""

    def __init__(self):
        """Create a new binder with an initial scope for top-level
        declarations."""
        self.depth = 0
        self.scopes = []
        self.push_new_scope()

    def push_new_scope(self):
        """Push a new scope on the scopes stack."""
        self.scopes.append({})

    def pop_scope(self):
        """Pop a scope from the scopes stack."""
        del self.scopes[-1]

    def current_scope(self):
        """Return the current scope."""
        return self.scopes[-1]

    def add_binding(self, decl):
        """Add a binding to the current scope and set the depth for
        this declaration. If the name already exists, an exception
        will be raised."""
        if decl.name in self.current_scope():
            raise BindException("name already defined in scope: %s" %
                                decl.name)
        self.current_scope()[decl.name] = decl
        decl.depth = self.depth

    def lookup(self, identifier):
        """Return the declaration associated with a name, looking
        into the closest scope first. If no declaration is found,
        raise an exception. If it is found, the decl and depth field
        for this identifier are set, and the escapes field of the
        declaration is updated if needed."""
        name = identifier.name
        for scope in reversed(self.scopes):
            if name in scope:
                decl = scope[name]
                identifier.decl = decl
                identifier.depth = self.depth
                decl.escapes |= self.depth > decl.depth
                return decl
        else:
            raise BindException("name not found: %s" % name)

    def visit_all(self, l):
        "visit all children nodes"
        for x in l:
            x.accept(self)


########## Surdédinition des méthodes de visitor ##########

    @visitor(None)
    def visit(self, node):
        self.visit_all(node.children)

    @visitor(VarDecl)
    def visit(self, var):
        self.add_binding(var)
        if var.exp:
            var.exp.accept(self)

    @visitor(FunDecl)
    def visit(self, fun):
        self.add_binding(fun)
        self.push_new_scope()
        self.depth += 1
        for x in fun.args:
            x.accept(self)
        fun.exp.accept(self)
        self.depth -= 1

    @visitor(FunCall)
    def visit(self, fun):
        identifier = fun.identifier
        decl = self.lookup(identifier)
        if isinstance(decl, FunDecl):
            if len(fun.params) == len(decl.args):
                self.visit_all(fun.children)
            else:
                raise BindException("Wrong number of paramaters in %s" % identifier.name)
        else:
            raise BindException("%s not a function instance" % identifier.name)

    @visitor(Identifier)
    def visit(self, name):
        self.lookup(name)

    @visitor(Let)
    def visit(self, let):
        self.push_new_scope()
        self.visit_all(let.children)
        self.pop_scope()
        


