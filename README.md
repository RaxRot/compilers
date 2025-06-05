# LSS Interpreter

## 📖 Overview

This project implements an interpreter for a simple domain-specific scripting language called **LSS** (Language for Scheduling Scripts). It allows users to:

- 📅 Schedule tasks using `schedule`
- 🚫 Mark unavailable dates using `unavailable`
- 🔁 Define reusable blocks using `def` and invoke them via `call`
- ❓ Execute conditionals with `if` / `else`
- 📦 Group commands in `batch` blocks
- 🔍 Query stored data using `query`

---

## 🧪 Example Script

```lss
schedule:
    task: "refuel"
    person: "Bob"
    date: "2025-06-03"

schedule:
    task: "service"
    person: "Julia"
    date: "2025-06-25"

unavailable:
    date: "2025-06-05"
    reason: "training"

def weekend():
    unavailable:
        date: "2025-06-08"
        reason: "closed"
    batch:
        schedule:
            task: "cleanup"
            person: "Mike"
            date: "2025-06-09"
        unavailable:
            date: "2025-06-10"
            reason: "holiday"

call weekend

if "day" == "saturday":
    unavailable:
        reason: "weekend"
else:
    schedule:
        task: "inspection"
        person: "Ana"
        date: "2025-06-10"

batch:
    schedule:
        task: "wash"
        person: "Lucas"
        date: "2025-06-12"

    unavailable:
        date: "2025-06-14"
        reason: "maintenance"

query:
    type: "schedule"
    filter: person == "Bob"
```

---

## 🖥️ Console Output

When running the interpreter:

- Tokens and keywords are printed
- Parsed commands are shown
- Execution logs appear
- Query results are printed

Example output:

```yaml
📂 Reading file from: C:\Univer\Compilers\fromjptv2\test.lss
🆔 SCHEDULE: schedule
🎯 STRING: refuel
🆔 ID: person
🎯 STRING: Bob
...
🚀 EXECUTING COMMANDS:
➡️ Command 1: {'type': 'schedule', 'task': 'refuel', 'person': 'Bob', 'date': '2025-06-03'}
...
🔎 Query results: [{'type': 'schedule', 'task': 'refuel', 'person': 'Bob', 'date': '2025-06-03'}]
```

---

## 💾 Stored Data (data_store.json)

After running, the stored file may look like:

```json
{
  "schedule": [
    {
      "type": "schedule",
      "task": "refuel",
      "person": "Bob",
      "date": "2025-06-03"
    },
    {
      "type": "schedule",
      "task": "service",
      "person": "Julia",
      "date": "2025-06-25"
    }
  ],
  "unavailable": [
    {
      "type": "unavailable",
      "date": "2025-06-05",
      "reason": "training"
    }
  ]
}
```

---

## ✅ Features

- 🗂 Tokenization and parsing using PLY
- 📅 `schedule` and `unavailable` persist to JSON
- 🔁 `def` stores reusable blocks
- 📞 `call` invokes user-defined blocks
- ❓ `if` / `else` logic works
- 📦 `batch` executes multiple commands
- 🔍 `query` filters and prints from data store

---

## ⚠️ Known Issues

- ❗ Nested `call` may cause infinite recursion
- ❌ Commands inside `def` blocks often don’t persist
- 🔁 No protection from cyclic `call`s
- 🐞 Minimal error handling
- 🛠 Complex logic may not save correctly

---

## ▶️ Usage Instructions

1. Write your `.lss` script.
2. Place it in the project directory.
3. Run the interpreter script (`python main.py`).
4. Check the console for logs and `data_store.json` for output.
5. Use `query` to print results to console.

---

## 🔚 Final Notes

This is a simplified prototype interpreter for learning purposes. Some advanced features like full nested execution or updates/deletes are intentionally incomplete.

---

Thank you for using **LSS Interpreter**! 🚀