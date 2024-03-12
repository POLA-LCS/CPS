# CPS - Command Prompt Saver
This is software designed for those who are accustomed to the command console to minimize command repetition or at least make it more dynamic. The program comes integrated with basic functions such as creating aliases for code blocks, quick ways to modify these blocks, and more specific ones like typing character by character in a command. It can call itself and can become very powerful if used skillfully. I'm open to proposals for the software as it will be open-source.
## Just available in Windows 10+
It uses batch commands and it is created with Python "subprocess", "os" and "sys" so maybe it isn't compatible with Linux or other OS. 

## Usage
- Set a directory for CPS (make sure it's not read-only).
- Run `cps.py` without parameters (this might create the `cps.json` file and fill it with default values).
- Add the directory to PATH.
- Type `cps --help` in another directory to make sure it works.
- Start creating your first function.
- - -
### CODE: This is the view when you run `cps --help` or `cps -h`
```
[CPS] Help:
Nomenclature:
    F = Function   :    The name of a function
    V = Value      :    A string value
    %%V = F values :    The code of a function
Info:
    [--help, -h]    Display this text
    [--info, -i]    Display all the user keys info
    F [--info, -i]  Display key info
Run:
                  Run 0 with default arguments
    F             Run F with default arguments
    F % <p...>    Run F with arguments <p>
    
    Tip: Dot (.) skips argument assign
Set:
    F = V    Set V to F
    F + V    Append V with the same logic as set
    F - V    Prepend V with the same logic as set
    F ^ F2   Switch F with F2
    
    Tip: "%%V" = The values of a function (cps F = %%V)
Delete:
    F = .    Deletes F
    F + .    Deletes the last command of F
    F - .    Deletes the first command of F
Arguments:
    F %% A V       Set function F argument A value to V
    F %% A .       Deletes argument A from F
```