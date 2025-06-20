import ply.lex as lex


# Это "ключевые слова" языка. Например, если в тексте встречается слово "schedule" —
# мы помечаем его как особое слово (SCHEDULE), а не как обычное имя.
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


# Это список всех "типов слов", которые может встретить программа.
# Например: ID — имя, STRING — строка в кавычках, COLON — символ двоеточие и т.д.
tokens = [
    'ID', 'STRING', 'COLON',   # ID = просто слово, STRING = текст в кавычках, COLON = :
    'EQ', 'NEQ', 'LT', 'GT',   # EQ = ==, NEQ = !=, LT = <, GT = >
    'LPAREN', 'RPAREN'         # Скобки ( и )
] + list(reserved.values())    # Добавляем также все ключевые слова (schedule, call и т.п.)

# Теперь мы говорим: если встретится двоеточие ":" — это токен COLON
t_COLON = r':'
# Если встретится == — это токен EQ (равенство)
t_EQ = r'=='
# != — это NEQ (не равно)
t_NEQ = r'!='
# < — это LT (меньше), > — GT (больше)
t_LT = r'<'
t_GT = r'>'
# Скобки
t_LPAREN = r'\('     # Левая скобка (
t_RPAREN = r'\)'     # Правая скобка )
# Пропускаем пробелы и табы (они не нужны)
t_ignore = ' \t'


# Если в тексте встретится строка в кавычках, например: "hello"
def t_STRING(t):
    r'"[^"\n]*"'                   # Это правило: строка в двойных кавычках, без перехода на новую строку
    t.value = t.value.strip('"')   # Убираем кавычки, чтобы оставить только текст внутри
    print(f"🎯 STRING: {t.value}")  # Показываем, что нашли строку
    return t                        # Возвращаем токен (один кусочек текста)


# Если встретилось обычное слово (например, task или person)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'       # Это правило: слово должно начинаться с буквы или подчёркивания
    t.type = reserved.get(t.value, 'ID')  # Проверяем: может быть это ключевое слово (например, 'def')?
    print(f"🆔 {t.type}: {t.value}")       # Показываем, что нашли слово и его тип
    return t                        # Возвращаем токен


# Если встретили перевод строки — увеличиваем счётчик строк (для отладки ошибок)
def t_newline(t):
    r'\n+'                          # Ищем один или несколько переводов строки
    t.lexer.lineno += len(t.value) # Увеличиваем номер текущей строки


# Если встретился непонятный символ — сообщаем об ошибке
def t_error(t):
    print(f"Illegal character: {t.value[0]}")  # Показываем, какой символ был ошибочным
    t.lexer.skip(1)                            # Пропускаем этот символ и идём дальше


# Включаем лексер (запускаем "мозг", который будет читать текст по правилам выше)
lexer = lex.lex()
