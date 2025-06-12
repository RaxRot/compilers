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
        data = load_data()  # Если данные не переданы — загружаем из файла

    ctype = cmd.get("type")  # Определяем, какой тип команды (например: schedule, call, if, query и т.д.)


    # === schedule ===
    if ctype == 'schedule':
        if 'filter' not in cmd:  # Если это не запрос (query), а обычная задача
            data['schedule'].append(cmd)  # Добавляем задачу в список
            save_data(data)  # Сохраняем изменения в файл



    # === unavailable ===
    # Добавляем новую запись о недоступности
    elif ctype == 'unavailable':
        data['unavailable'].append(cmd)  # Добавляем событие в список недоступностей
        save_data(data)  # Сохраняем файл




    # === def ===
    elif ctype == 'def':
        variables[cmd['name']] = cmd['body']  # Сохраняем имя функции и её команды (в виде списка)




    # === call ===
    # Выполняем ранее определённую функцию
    elif ctype == 'call':
        block = variables.get(cmd['name'])  # Получаем команды, которые хранятся под этим именем
        if block:  # Если нашли такую функцию —
            for sub in block:  # Проходимся по всем её командам
                execute_command(sub, data)  # И выполняем их



        # === if ===
        # Выполняем then или else в зависимости от условия
        elif ctype == 'if':
            # Выбираем ветку then или else в зависимости от результата условия
            branch = cmd['then'] if eval_condition(cmd['cond']) else cmd['else']
            for sub in branch:  # Выполняем все команды в выбранной ветке
                execute_command(sub, data)

        # === batch ===
        # Выполняем список команд подряд
        elif ctype == 'batch':
            for sub in cmd['commands']:  # Получаем список команд
                execute_command(sub, data)  # Выполняем каждую

        # === query ===
        # Выполняем поиск в данных по фильтру
        elif ctype == 'query':
            results = data.get(cmd['type'], [])  # Получаем нужный список (например: schedule)
            filt = cmd.get('filter')  # Проверяем, есть ли фильтр

            if filt:
                field, op, value = filt  # Разбиваем фильтр на 3 части: поле, оператор и значение
                if op == '==':  # Сейчас поддерживается только "равно"
                    results = [r for r in results if r.get(field) == value]  # Оставляем только совпадающие

            print("\n🔎 Query results:", results)  # Выводим результаты на экран


def eval_condition(cond):
    left, op, right = cond  # Разбиваем условие на три части

    if op == '==': return left == right      # Проверка: равно
    if op == '!=': return left != right      # Проверка: не равно
    if op == '<': return left < right        # Меньше
    if op == '>': return left > right        # Больше

    return False  # Если условие не распознано — возвращаем False (как будто условие ложное)

