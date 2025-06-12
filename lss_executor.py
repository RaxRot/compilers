import json

DATA_FILE = 'lss-backend/data_store.json'  # Путь к файлу, в котором будут храниться все расписания и недоступности

variables = {}  # Здесь будут сохраняться пользовательские функции, созданные через def


def load_data():
    try:
        with open(DATA_FILE, 'r') as f:  # Пытаемся открыть файл для чтения
            return json.load(f)          # Преобразуем содержимое из текста JSON в обычный Python-словарь
    except:
        # Если файл не найден или пустой — возвращаем пустую структуру с двумя списками
        return {'schedule': [], 'unavailable': []}


def save_data(data):
    with open(DATA_FILE, 'w') as f:     # Открываем файл для записи (старое содержимое будет удалено)
        json.dump(data, f, indent=2)    # Преобразуем словарь в текст JSON и сохраняем с отступами (чтобы было красиво видно)


def execute_command(cmd, data=None):
    if data is None:
        data = load_data()

    ctype = cmd.get("type")

    if ctype == 'schedule':
        if 'filter' not in cmd:
            data['schedule'].append(cmd)

    elif ctype == 'unavailable':
        data['unavailable'].append(cmd)

    elif ctype == 'def':
        variables[cmd['name']] = cmd['body']

    elif ctype == 'call':
        block = variables.get(cmd['name'])
        if block:
            for sub in block:
                data = execute_command(sub, data)  # ✅ ОБЯЗАТЕЛЬНО вернуть обновлённые данные

    elif ctype == 'if':
        branch = cmd['then'] if eval_condition(cmd['cond']) else cmd['else']
        for sub in branch:
            data = execute_command(sub, data)

    elif ctype == 'batch':
        for sub in cmd['commands']:
            data = execute_command(sub, data)

    elif ctype == 'query':
        results = data.get(cmd['type'], [])
        filt = cmd.get('filter')
        if filt:
            field, op, value = filt
            if op == '==':
                results = [r for r in results if r.get(field) == value]
            print("\n🔎 Query results:", results)

    return data  # ✅ ОБЯЗАТЕЛЬНО: всегда возвращай обновлённые данные


def eval_condition(cond):
    left, op, right = cond  # Разбиваем условие на три части

    if op == '==': return left == right      # Проверка: равно
    if op == '!=': return left != right      # Проверка: не равно
    if op == '<': return left < right        # Меньше
    if op == '>': return left > right        # Больше

    return False  # Если условие не распознано — возвращаем False (как будто условие ложное)

