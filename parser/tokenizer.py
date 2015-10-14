import ply.lex as lex

states = (
        ('pythonccomment', 'exclusive'),
        ('ccomment', 'exclusive')
         )

# List of keywords. Each keyword will be return as a token of a specific
# type, which makes it easier to match it in grammatical rules.
keywords = {'array': 'ARRAY',
            'break': 'BREAK',
            'do': 'DO',
            'else': 'ELSE',
            'end': 'END',
            'for': 'FOR',
            'function': 'FUNCTION',
            'if': 'IF',
            'in': 'IN',
            'let': 'LET',
            'nil': 'NIL',
            'of': 'OF',
            'then': 'THEN',
            'to': 'TO',
            'type': 'TYPE',
            'int': 'INT',
            'var': 'VAR',
            'while': 'WHILE'}

# List of tokens that can be recognized and are handled by the current
# grammar rules.
tokens = ('END', 'IN', 'LET', 'VAR',
          'PLUS', 'TIMES',
          'MINUS', 'DIVIDE',
          'COMMA', 'SEMICOLON',
          'LPAREN', 'RPAREN',
          'NUMBER', 'ID',
          'COLON', 'ASSIGN',
          'INFERIOR', 'INFERIOREQUAL',
          'SUPERIOR', 'SUPERIOREQUAL',
          'EQUAL', 'DIFFERENT',
          'OR', 'AND',
          'IF', 'THEN', 'ELSE',
          'FUNCTION', 'INT') 

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_ASSIGN = r':='
t_COMMA = r','
t_SEMICOLON = r';'
t_INFERIOR = r'\<'
t_INFERIOREQUAL = r'\<='
t_SUPERIOR = r'\>'
t_SUPERIOREQUAL = r'\>='
t_EQUAL = r'\='
t_DIFFERENT = r'\<>'
t_OR = r'\|'
t_AND = r'\&'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_LET = r'let'
t_VAR = r'var'
t_IN = r'in'
t_END = r'end'
t_FUNCTION = r'function'
t_INT = r'in'

t_ignore = ' \t'

# Count lines when newlines are encountered
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Distinguish between identifier and keyword. If the keyword is not also
# in the tokens list, this is a syntax error pure and simple since we do
# not know what to do about it.
def t_ID(t):
    r'[A-Za-z][A-Za-z\d_]*'
    if t.value in keywords:
        t.type = keywords.get(t.value)
        if t.type not in tokens:
            raise lex.LexError("unhandled keyword %s" % t.value, t.type)
    return t

# Recognize number - no leading 0 are allowed
def t_NUMBER(t):
    r'[1-9]\d*|0'
    t.value = int(t.value)
    return t

def t_error(t):
    raise lex.LexError("unknown token %s" % t.value, t.value)

############## Implémentation des ccommentaires ###################"

# inline ccomment : ignore the rest of the line
def t_pythonccommentStart(t):
    r'//.*'
    t.lexer.begin('pythonccomment')

# when in inline ccomment, a newline escapes the ccomment
def t_pythonccomment_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')

# when a ccomment begins, change state to ignore everthing but begin and end ccomment tokens
def t_INITIAL_ccomment_ccommentStart(t):
    r'/\*'
    t.lexer.push_state('ccomment')


def t_ccomment_ignore_text(t):
     r'(?!/\*|\*/).'
     pass


def t_ccomment_newline(t):
    r'\n+'
    pass


def t_ccomment_ccommentEnd(t):
    r'\*/'
    t.lexer.pop_state()


def t_ccomment_eof(t):
    raise lex.LexError("ccomment not closed")

lexer = lex.lex()


