import ply.lex as lex

reserved = {
    'schedule': 'SCHEDULE',
    'unavailable': 'UNAVAILABLE',
    'def': 'DEF',
    'call': 'CALL',
    'batch': 'BATCH',
    'if': 'IF',
    'else': 'ELSE',
    'query': 'QUERY',
    'filter': 'FILTER'
}

tokens = [
    'ID', 'STRING', 'COLON',
    'EQ', 'NEQ', 'LT', 'GT',
    'LPAREN', 'RPAREN'
] + list(reserved.values())

t_COLON = r':'
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value.strip('"')
    print(f"🎯 STRING: {t.value}")
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    print(f"🆔 {t.type}: {t.value}")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
