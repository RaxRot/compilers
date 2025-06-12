from flask import Flask, jsonify
from flask_cors import CORS
import json



app = Flask(__name__)  # Создаём приложение Flask. Теперь оно "слушает" запросы, как маленький веб-сервер
CORS(app)              # Разрешаем всем сайтам доступ к нашему API (иначе браузер может блокировать)


# Указываем путь к файлу, где хранятся наши данные
DATA_FILE = 'data_store.json'


# Функция для загрузки данных из JSON-файла
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:     # Пробуем открыть файл
            return json.load(f)             # Преобразуем содержимое в словарь и возвращаем
    except Exception:                       # Если файла нет или он пустой
        return {'schedule': [], 'unavailable': []}  # Возвращаем пустую структуру


# Когда пользователь открывает /api/schedules в браузере или в приложении —
# мы возвращаем все запланированные задачи из файла
@app.route('/api/schedules')
def get_schedules():
    data = load_data()                           # Загружаем данные
    return jsonify(data.get('schedule', []))     # Отдаём список задач (или пустой список)



# Когда пользователь открывает /api/unavailable —
# мы возвращаем все записи о недоступности
@app.route('/api/unavailable')
def get_unavailable():
    data = load_data()                             # Загружаем данные
    return jsonify(data.get('unavailable', []))    # Отдаём список недоступностей


# Если мы запускаем этот файл напрямую (через python app.py) —
# запускается веб-сервер на localhost:5000
if __name__ == '__main__':
    app.run(debug=True)  # Включаем сервер и режим отладки (чтобы видеть ошибки и автообновления)

