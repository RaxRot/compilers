from lss_parser import parser
from lss_executor import execute_command, save_data
import os

if __name__ == "__main__":
    file_path = "test.lss"
    print("📂 Reading file from:", os.path.abspath(file_path))

    # 💥 Очищаем базу перед запуском
    save_data({'schedule': [], 'unavailable': []})

    with open(file_path, "r", encoding="utf-8") as f:
        script = f.read()
        print("=== SCRIPT CONTENT ===\n", script)

        result = parser.parse(script)

        if result:
            print("\n🚀 EXECUTING COMMANDS:")
            for i, cmd in enumerate(result, 1):
                print(f"\n➡️ Command {i}: {cmd}")
                execute_command(cmd)

        print("\n✅ Parsing complete.")
