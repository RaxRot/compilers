import ply.yacc as yacc
from lss_lexer import tokens
from lss_executor import execute_command

# === Главная программа: список команд ===
def p_program(p):
    'program : blocks'
    p[0] = p[1]

# === Последовательность блоков ===
def p_blocks(p):
    '''blocks : block blocks
              | block'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

# === Блоки-команды ===
def p_block_schedule(p):
    'block : SCHEDULE COLON field_lines'
    p[0] = {'type': 'schedule', **p[3]}

def p_block_unavailable(p):
    'block : UNAVAILABLE COLON field_lines'
    p[0] = {'type': 'unavailable', **p[3]}

def p_block_def(p):
    'block : DEF ID LPAREN RPAREN COLON blocks'
    p[0] = {'type': 'def', 'name': p[2], 'body': p[6]}

def p_block_call(p):
    'block : CALL ID'
    p[0] = {'type': 'call', 'name': p[2]}

def p_block_if(p):
    'block : IF condition COLON blocks ELSE COLON blocks'
    p[0] = {
        'type': 'if',
        'cond': p[2],
        'then': p[4],
        'else': p[7]
    }

def p_block_batch(p):
    'block : BATCH COLON blocks'
    p[0] = {'type': 'batch', 'commands': p[3]}

def p_block_query(p):
    'block : QUERY COLON query_fields'
    p[0] = {'type': 'query', **p[3]}

# === Поля query ===
def p_query_fields(p):
    '''query_fields : query_fields field
                    | query_fields filter_line
                    | field
                    | filter_line'''
    if len(p) == 3:
        p[0] = {**p[1], **p[2]}
    else:
        p[0] = p[1]

def p_filter_line(p):
    'filter_line : FILTER COLON ID EQ STRING'
    p[0] = {'filter': (p[3], '==', p[5])}

# === Общие поля: task, person, date, reason ===
def p_field_lines(p):
    '''field_lines : field_lines field
                   | field'''
    if len(p) == 3:
        p[0] = {**p[1], **p[2]}
    else:
        p[0] = p[1]

def p_field(p):
    'field : ID COLON STRING'
    p[0] = {p[1]: p[3]}

# === Условия в if ===
def p_condition(p):
    '''condition : STRING EQ STRING
                 | STRING NEQ STRING
                 | STRING LT STRING
                 | STRING GT STRING'''
    p[0] = (p[1], p[2], p[3])

# === Обработка ошибок ===
def p_error(p):
    print("❌ Syntax error:", p)

# === Построение парсера ===
parser = yacc.yacc()
