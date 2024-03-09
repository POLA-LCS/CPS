import json
from subprocess import run
from sys import argv
import os
        
PATH = os.path.dirname(os.path.abspath(__file__))
INDENT = 4

def read_cps() -> dict:
    data = {}
    with open(PATH + '\\cps.json', 'r') as file:
        data = json.load(file)
        data.setdefault('!default', "echo Hello, CPS!")
        data.setdefault('!first', "cls")
        data.setdefault('!last', "")
        for key in data:
            if not isinstance(data[key], list):
                data[key] = [data[key]]
    return data

def update_cps(): 
    data = read_cps()
    with open(PATH + '\\cps.json', 'w') as file:
        json.dump(data, file, indent=INDENT)
    return data
        
def set_key(key: str, value: list[str] | None):
    data = update_cps()
    with open(PATH + '\\cps.json', 'w') as file:
        if not value:
            del data[key]
        else:
            data[key] = value
        json.dump(data, file, indent=INDENT)
                    
def run_commands(comms: list):
    for com in comms:
        run(com, shell=True)

def HELP():
    print("""Info:
    cps (--help | -h)     Display help text
    cps (--info | -i)     Display all the key infos
    cps a (--info | -i)   Display "a" key info

Run:
  (--clean | -c) excepts !first and !last to be executed.
    cps                   Run !first, !default and !last
    cps .                 Run !first and !last
    cps a                 Run !first, "a" key and !last

Binary operators:
  Dot (.) is used to delete in case of assign or pop in case of append or prepend.
    =     Set a string or another key
    +     Append a string or another key
    *     Prepend a command or another key
    |     Switch a key with another key
    ++    Append to the last command a string
    +*    Prepend to the last command a string
    *+    Append to the first command a string
    **    Prepend to the first command a string""")

if __name__ == '__main__':
    try:
        argc = len(argv)
        
        data = update_cps()
        if argc == 1: # cps
            run_commands(data['!first'])
            run_commands(data['!default'])
            run_commands(data['!last'])
        elif argc == 2: # cps (<flag> | <key>)
            if argv[1] in ['--help', '-h']:
                HELP()
            elif argv[1] in ['--open', '-o']:
                run_commands(['cps.json'])
            elif argv[1] in ['--info', '-i']:
                for key in data:
                    print(f'{key}:  \t{data[key]}')
            elif argv[1] in ['--clean', '-c']:
                run_commands(data['!default'])
            elif argv[1] == '.':
                run_commands(data['!first'])
                run_commands(data['!last'])
            else:
                _ = data[argv[1]]
                run_commands(data['!first'])
                run_commands(data[argv[1]])
                run_commands(data['!last'])
        elif argc == 3: # cps <key> <flag>
            if argv[2] in ['--info', '-i']:
                print(f'{argv[1]}:  \t{data[argv[1]]}')
            elif argv[2] in ['--clean', '-c']:
                if argv[1] != '.':
                    run_commands(data[argv[1]])
        elif argc >= 4: # cps <key> <op> (<key> | <val>)
            record = ''
            if argv[3].startswith("\'"):
                for i in range(3, argc):
                    record += argv[i] + ' '
            if record:
                if argv[2] == '++':
                    set_key(argv[1], data[argv[1]][:-1] + [data[argv[1]][-1] + record[1:-2]])
                elif argv[2] == '**':
                    set_key(argv[1], [record[1:-2] + data[argv[1]][0]] + data[argv[1]][1:])
                elif argv[2] == '+*':
                    set_key(argv[1], data[argv[1]][:-1] + [record[1:-2] + data[argv[1]][-1]])
                elif argv[2] == '*+':
                    set_key(argv[1], [data[argv[1]][0] + record[1:-2]] + data[argv[1]][1:])
                elif argv[2] == '=':
                    set_key(argv[1], [record[1:-2]])
                elif argv[2] == '+':
                    set_key(argv[1], data[argv[1]] + [record[1:-2]])
                elif argv[2] == '*':
                    set_key(argv[1], [record[1:-2]] + data[argv[1]])
            else:
                if argv[2] == '|':
                    a, b = data[argv[1]], data[argv[3]]
                    set_key(argv[1], b)
                    set_key(argv[3], a)
                elif argv[2] == '++':
                    if argv[3] == '.':
                        set_key(argv[1], data[argv[1]][:-1] + [data[argv[1]][-1][:-1]])
                    else:
                        assert False, "[NOT IMPLEMENTED] a ++ b"
                elif argv[2] == '+*':
                    if argv[3] == '.':
                        set_key(argv[1], data[argv[1]][:-1] + [data[argv[1]][-1][1:]])
                    else:
                        assert False, "[NOT IMPLEMENTED] a *+ b"
                elif argv[2] == '*+':
                    if argv[3] == '.':
                        set_key(argv[1], [data[argv[1]][0][:-1]] + data[argv[1]][1:])
                    else:
                        assert False, "[NOT IMPLEMENTED] a *+ b"
                elif argv[2] == '**':
                    if argv[3] == '.':
                        set_key(argv[1], [data[argv[1]][0][1:]] + data[argv[1]][1:])
                    else:
                        assert False, "[NOT IMPLEMENTED] a ** b"
                elif argv[2] == '=':
                    if argv[3] == '.':
                        set_key(argv[1], None)
                    else:
                        set_key(argv[1], data[argv[3]])
                elif argv[2] == '+':
                    if argv[3] == '.':
                        set_key(argv[1], data[argv[1]][:-1])
                    else:
                        set_key(argv[1], data[argv[1]] + data[argv[3]])
                elif argv[2] == '*':
                    if argv[3] == '.':
                        set_key(argv[1], data[argv[1]][1:])
                    else:
                        set_key(argv[1], data[argv[3]] + data[argv[1]])
    except KeyError as err:
        print(f"[ERROR] Doesn't exists: {err.args[0]}")
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("Getting ready cps.json file...")
        with open(PATH + '\\cps.json', 'w') as file:
            file.write('{}')
        update_cps()
        print("Finished.")
    except AssertionError as ass:
        print(ass)