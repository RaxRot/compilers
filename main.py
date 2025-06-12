from lss_parser import parser
from lss_executor import execute_command, save_data, load_data
import os

# Создаем папку для данных
if not os.path.exists('lss-backend'):
    os.makedirs('lss-backend')

if __name__ == "__main__":
    # Инициализируем чистые данные
    initial_data = {'schedule': [], 'unavailable': []}
    save_data(initial_data)

    file_path = "test.lss"
    print("📂 Reading file from:", os.path.abspath(file_path))

    with open(file_path, "r", encoding="utf-8") as f:
        script = f.read()
        print("=== SCRIPT CONTENT ===\n", script)

        result = parser.parse(script)

        if result:
            print("\n🚀 EXECUTING COMMANDS:")
            current_data = load_data()  # Загружаем текущие данные

            for i, cmd in enumerate(result, 1):
                print(f"\n➡️ Command {i}: {cmd}")
                current_data = execute_command(cmd, current_data)  # Передаем данные между командами

            # ⬇️⬇️⬇️ ДОБАВЬ ЭТУ СТРОКУ ЗДЕСЬ
            save_data(current_data)  # Сохраняем результат в файл

            print("\n✅ Execution complete.")
            print("Final data state:", current_data)  # Показываем конечное состояние данных
