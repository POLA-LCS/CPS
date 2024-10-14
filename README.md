# CPS: Command Prompt Saver

CPS is a script designed to optimize the use of the terminal commands (Either Windows or Linux).
It allows users to create, save, and run macros (blocks of commands), minimizing repetitive tasks.
The script supports dynamic argument substitution, macro management, and command organization.

## Features
- **Macro Management**: Save, delete, append, and prepend commands to macros.
- **Argument Substitution**: Customize macros with dynamic arguments.
- **Macro Copying**: Switch or copy commands between macros.
- **Command Execution**: Run predefined macros or ad-hoc commands easily.

## Requirements
- Python 3.x

## Installation
1. Clone this repository or download the `cps.py` file.
2. Ensure that `cps.json` (the macro storage file) exists in the same directory as the script. If not, CPS will prompt you to create one.

## Usage
Run the script from the command prompt using Python:

### Help and Info
- `cps.py --help` or `cps.py -h`  
  Display help information.

- `cps.py --info` or `cps.py -i`  
  Display all saved macros.

- `cps.py <macro> --info` or `cps.py <macro> -i`  
  Show details of a specific macro.

### Run Macros
- `cps.py`  
  Run the default macro (named `0`).

- `cps.py <macro>`  
  Run the specified macro.

- `cps.py <macro> % <params>`  
  Run the specified macro with the provided arguments.

### Manage Macros
- `cps.py <macro> = <command>`  
  Set or overwrite a macro with the given command.

- `cps.py <macro> = <%%macro2>`
  Set a macro to another macro2.

- `cps.py <macro> + <command>`  
  Append a command to the macro.

- `cps.py <macro> - <command>`  
  Prepend a command to the macro.

- `cps.py <macro> # <macro2>`  
  Switch the commands of `macro` and `macro2`.

### Delete Macros or Commands
- `cps.py <macro> = .`  
  Delete the macro.

- `cps.py <macro> + .`  
  Delete the last command from the macro.

- `cps.py <macro> - .`  
  Delete the first command from the macro.

### Manage Parameters
- `cps.py <macro> %% <param> <value>`  
  Set a parameter for the macro.

- `cps.py <macro> %% <param> .`  
  Delete a parameter from the macro.

## File Structure
- **cps.json**: This file stores macros in JSON format. Each macro has a name and a list of commands associated with it.

## Error Handling
- **Missing File**: If `cps.json` is not found, CPS will prompt you to create it.
- **Key Errors**: If a macro or parameter doesn't exist, an error message will be displayed.
- **Invalid JSON**: If the JSON data is corrupted, CPS will notify you.
---

Enjoy automating your command prompt tasks with CPS!
