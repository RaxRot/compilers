from lss_parser import parser
from lss_executor import execute_command, save_data
import os


# Эта строка запускает код, ТОЛЬКО если мы запускаем main.py напрямую
# (а не просто импортируем его в другой файл)
if __name__ == "__main__":

    file_path = "test.lss"  # Указываем имя LSS-файла, из которого будем читать команды
    print("📂 Reading file from:", os.path.abspath(file_path))  # Показываем полный путь к файлу


    # 💥 Перед запуском очищаем старые данные (перезаписываем пустыми списками)
    save_data({'schedule': [], 'unavailable': []})

    # Открываем файл "test.lss" и читаем его содержимое (весь текст)
    with open(file_path, "r", encoding="utf-8") as f:
        script = f.read()  # Читаем весь файл как строку
        print("=== SCRIPT CONTENT ===\n", script)  # Показываем, что там написано

        result = parser.parse(script)  # Передаём текст в парсер — он превратит текст в список команд (в виде словарей)

        if result:  # Если парсер вернул какие-то команды (т.е. файл был правильный)
            print("\n🚀 EXECUTING COMMANDS:")  # Готовимся к выполнению

            for i, cmd in enumerate(result, 1):  # Перебираем команды по очереди с номерами (1, 2, 3...)
                print(f"\n➡️ Command {i}: {cmd}")  # Показываем, что за команда
                execute_command(cmd)  # Выполняем эту команду (например: добавить расписание)

        print("\n✅ Parsing complete.")  # В самом конце выводим сообщение, что всё прошло успешно

