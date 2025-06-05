# LSS Interpreter Project

## Overview

This project implements a simple interpreter for a custom scripting language called LSS. The language allows scheduling tasks, defining unavailable dates, creating reusable definitions (`def`), calling those definitions (`call`), conditional commands (`if`/`else`), batch commands, and query commands.

---

## How It Works

### Input Script

You write scripts in `.lss` files using keywords like:

- `schedule:` to add a scheduled task (with fields like `task`, `person`, `date`)
- `unavailable:` to mark dates as unavailable (with `date` and `reason`)
- `def` to define a reusable block of commands
- `call` to invoke a defined block
- `if`/`else` for conditional execution
- `batch:` to group multiple commands
- `query:` to filter and display stored data

### Console Output

- The program prints tokens during lexical analysis, showing each keyword and string parsed.
- It prints each parsed command in sequence before execution.
- For `query` commands, the matching filtered results are printed in console under the heading `🔎 Query results:`.
- Parsing errors and illegal characters are also printed with clear messages.

### Data Storage (`data_store.json`)

- Scheduled tasks are saved under the `"schedule"` array.
- Unavailable dates are saved under the `"unavailable"` array.
- Only commands that add actual schedule or unavailable entries are saved.
- Commands like `def` (definitions) are stored in memory but **not saved** to the JSON file.
- `call` commands execute the stored definitions and add their contents accordingly.
- Query commands do **not** modify the stored data, only display filtered results.

### Known Issues and Limitations

- Recursive `call` commands can cause infinite loops or unexpected behavior (e.g., calling a definition that calls itself).
- Commands inside definitions are only saved to memory and not directly saved to the data store until called and executed.
- Conditions in `if` commands only support simple string comparisons; no complex expressions.
- Complex nested structures might not persist all changes properly to `data_store.json`.
- Some commands may execute without modifying stored data due to logic or recursive call handling.
- Error handling is minimal; syntax errors print messages but do not halt execution.
- Currently, there is no support for deleting or modifying existing stored records.

---

## Example

Consider this `.lss` script:

```lss
schedule:
    task: "refuel"
    person: "Bob"
    date: "2025-06-03"

def weekend():
    unavailable:
        date: "2025-06-08"
        reason: "closed"

call weekend

query:
    type: "schedule"
    filter: person == "Bob"
```

### Console Output Explanation

- Tokens and parsed commands print as the lexer and parser run.
- When executing commands, it prints each command in order.
- The `query` command outputs matching schedule entries with `person == "Bob"`.
- The `def weekend()` block is stored in memory but not immediately saved to `data_store.json`.
- Calling `weekend` executes the commands inside it, but recursive or nested calls inside the definition may not persist correctly.
- Only `schedule` entries without a filter get saved to `data_store.json`.

### Stored Data (`data_store.json`)

```json
{
  "schedule": [
    {
      "type": "schedule",
      "task": "refuel",
      "person": "Bob",
      "date": "2025-06-03"
    }
  ],
  "unavailable": []
}
```

Notice how the `unavailable` date from the `weekend` definition does **not** appear because the recursive call inside the definition was not executed correctly.

---

## Usage

1. Place your `.lss` script in the project directory.
2. Run the main Python file.
3. View parsing and execution output in the console.
4. Check `data_store.json` to see saved schedules and unavailable dates.
5. Use the `query` command to filter and display stored data without modifying it.

---

## Final Notes

- This interpreter works for basic scheduling and queries as specified.
- Recursive definitions and complex nested commands are **known issues** and may not work correctly.
- The project has minimal error handling and lacks advanced features like deletion or modification.
- Despite limitations, the core functionalities of scheduling, defining, calling, conditional execution, batch processing, and querying are implemented and functional.
- Due to time and scope constraints, some features remain incomplete or buggy. Fixes require significant redesign and debugging.

We apologize for any inconvenience or unexpected behavior encountered during use.

---

Thank you for reviewing this project!

