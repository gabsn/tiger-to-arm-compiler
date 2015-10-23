from ast.nodes import *

from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'DIFFERENT', 'INFERIOR', 'INFERIOREQUAL', 'SUPERIOR', 'SUPERIOREQUAL', 'ASSIGN', 'COLON', 'COMMA'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

############## Binary Operator ##################

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression INFERIOR expression
                  | expression INFERIOREQUAL expression 
                  | expression SUPERIOR expression
                  | expression SUPERIOREQUAL expression 
                  | expression EQUAL expression
                  | expression DIFFERENT expression
                  | expression OR expression
                  | expression AND expression'''
    p[0] = BinaryOperator(p[2], p[1], p[3])

############ Expressions #############

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = BinaryOperator('-', IntegerLiteral(0), p[2])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

########### Parenthesis ###############

def p_expression_parentheses(p):
    'expression : LPAREN list RPAREN'
    p[0] = SeqExp(p[2])

def p_list(p):
    '''list : 
            | listexp'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]

############ IfThenElse #############

def p_expression_ifthenelse(p):
    '''expression : IF expression THEN expression ELSE expression'''
    if len(p) == 7:
        p[0] = IfThenElse(p[2], p[4], p[6])
    else:
        p[0] = IfThenElse(p[2], p[4], None)

def p_expression_ifthen(p):
    '''expression : IF expression THEN expression'''
    p[0] = IfThenElse(p[2], p[4], None)

############ VarDecl ############

def p_expression_vardecl(p):
    '''vardecl : VAR ID ASSIGN expression
               | VAR ID COLON INT ASSIGN expression'''
    if len(p) == 5:
        p[0] = VarDecl(p[2], None, p[4])  
        #print('vardecl sans int')
    else:
        p[0] = VarDecl(p[2], Type(p[4]), p[6])  
        #print('vardecl avec int')

############ FunDecl #############

def p_expression_fundecl(p):
    '''fundecl : FUNCTION ID LPAREN params RPAREN EQUAL expression
               | FUNCTION ID LPAREN params RPAREN COLON INT EQUAL expression'''
    if len(p) == 8:
        p[0] = FunDecl(p[2], p[4], None , p[7])
    else:
        p[0] = FunDecl(p[2], p[4], Type(p[7]), p[9])

def p_params(p):
    '''params : 
              | ID COLON INT
              | params COMMA ID COLON INT'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 4:
        p[0] = [VarDecl(p[1], Type(p[3]), None)]
        #print('params %s' % p[1])
    elif len(p) == 6 and p[1] == []: 
        raise Exception('Bad syntax in parser.py')
    else:
        p[0] = p[1] + [VarDecl(p[3], Type(p[5]), None)]
        #print('params %s' % p[3])

############ FunCall ##############

def p_expression_funcall(p):
    '''expression : ID LPAREN explist RPAREN'''
    p[0] = FunCall(Identifier(p[1]), p[3])

def p_explist(p):
    '''explist : 
               | expression
               | explist COMMA expression'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4 and p[1] == []:
        raise Exception('Bad syntax in parser.py')
    else:
        p[0] = p[1] + [p[3]]

############## Let ################

def p_expression_let(p):
    '''expression : LET decls IN listexp END
                  | LET decls IN END'''
    #TODO rajouter assignment
    if len(p) == 5:
        p[0] = Let(p[2], [])
    else:
        p[0] = Let(p[2], p[4])

def p_decls(p):
    '''decls : vardecl 
             | fundecl
             | decls vardecl
             | decls fundecl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_listexp(p):
    '''listexp : expression
               | listexp SEMICOLON expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

############## Assignment ##############

def p_assignment(p):
    '''expression : ID ASSIGN expression'''
    p[0] = Assignment(Identifier(p[1]), p[3])

############## Parse error #############

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
