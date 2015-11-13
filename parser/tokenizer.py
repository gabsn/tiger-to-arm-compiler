import ply.lex as lex

states = (
        ('pythoncomment', 'exclusive'),
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
          'FUNCTION', 'INT',
          'WHILE', 'FOR', 'TO', 'DO', 'BREAK') 

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

t_ignore = ' \t'
t_pythoncomment_ignore = ''
t_ccomment_ignore = ''

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

def t_pythoncomment_ccomment_error(t):
    raise lex.LexError("error in tokenizer")

############## Implémentation des commentaires ###################

def t_pythoncommentStart(t):
    r'//.*'
    t.lexer.begin('pythoncomment')

def t_pythoncomment_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')

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


