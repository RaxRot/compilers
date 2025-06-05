import json

DATA_FILE = 'data_store.json'
variables = {}

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'schedule': [], 'unavailable': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def execute_command(cmd, data=None):
    if data is None:
        data = load_data()

    ctype = cmd.get("type")

    if ctype == 'schedule':
        if 'filter' not in cmd:  # Игнорируем "фейковые" schedule в query
            data['schedule'].append(cmd)
            save_data(data)

    elif ctype == 'unavailable':
        data['unavailable'].append(cmd)
        save_data(data)

    elif ctype == 'def':
        variables[cmd['name']] = cmd['body']

    elif ctype == 'call':
        block = variables.get(cmd['name'])
        if block:
            for sub in block:
                execute_command(sub, data)

    elif ctype == 'if':
        branch = cmd['then'] if eval_condition(cmd['cond']) else cmd['else']
        for sub in branch:
            execute_command(sub, data)

    elif ctype == 'batch':
        for sub in cmd['commands']:
            execute_command(sub, data)

    elif ctype == 'query':
        results = data.get(cmd['type'], [])
        filt = cmd.get('filter')
        if filt:
            field, op, value = filt
            if op == '==':
                results = [r for r in results if r.get(field) == value]
        print("\n🔎 Query results:", results)


def eval_condition(cond):
    left, op, right = cond
    if op == '==': return left == right
    if op == '!=': return left != right
    if op == '<': return left < right
    if op == '>': return left > right
    return False