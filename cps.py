import json
import os
from subprocess import run
from sys import argv

PATH = os.path.dirname(os.path.abspath(__file__))
INDENT = 4

def read_cps() -> dict:
    try:
        with open(os.path.join(PATH, 'cps.json'), 'r') as file:
            data = json.load(file)
            data.setdefault('!default', "echo Hello, CPS!")
            data.setdefault('!first', "cls")
            data.setdefault('!last', "")
            for key, value in data.items():
                if not isinstance(value, list):
                    data[key] = [value]
        return data
    except FileNotFoundError:
        return {'!default': ["echo Hello, CPS!"], '!first': ["cls"], '!last': [""]}

def update_cps():
    data = read_cps()
    with open(os.path.join(PATH, 'cps.json'), 'w') as file:
        json.dump(data, file, indent=INDENT)
    return data

def set_key(key: str, value: list[str] | None):
    data = update_cps()
    with open(os.path.join(PATH, 'cps.json'), 'w') as file:
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
  (--clean | -c) expects !first and !last to be executed.
    cps                   Run !first, !default and !last
    cps .                 Run !first and !last
    cps a                 Run !first, "a" key and !last

Binary operators:
  Dot (.) is used to delete in case of assign or pop in case of append or prepend.
    =     Set a string or another key
    +     Append a string or another key
    *     Prepend a command or another key
    #     Switch a key with another key
    ++    Append to the last command a string
    +*    Prepend to the last command a string
    *+    Append to the first command a string
    **    Prepend to the first command a string""")

if __name__ == '__main__':
    try:
        argc = len(argv)

        data = update_cps()
        if argc == 1:  # cps
            run_commands(data['!first'])
            run_commands(data['!default'])
            run_commands(data['!last'])
        elif argc == 2:  # cps (<flag> | <key>)
            if argv[1] in ['--help', '-h']:
                HELP()
            elif argv[1] in ['--open', '-o']:
                print("[CPS] Opening cps.json...")
                run_commands(['cps.json'])
                print("[CPS] cps.json was closed.")
            elif argv[1] in ['--info', '-i']:
                for key, value in data.items():
                    print(f'{key}:  \t{value}')
            elif argv[1] in ['--clean', '-c']:
                run_commands(data['!default'])
            elif argv[1] == '.':
                run_commands(data['!first'])
                run_commands(data['!last'])
            else:
                call = data[argv[1]]
                run_commands(data['!first'])
                run_commands(call)
                run_commands(data['!last'])
        elif argc == 3:  # cps <key> <flag>
            if argv[2] in ['--info', '-i']:
                print(f'[CPS] Info: {argv[1]}')
                for com in data[argv[1]]:
                    print('  -  ', com)
            elif argv[2] in ['--clean', '-c']:
                if argv[1] != '.':
                    run_commands(data[argv[1]])
        elif argc >= 4:  # cps <key> <op> (<key> | <val>)
            record = ''
            if argv[3].startswith("\'"):
                record = ' '.join(argv[3:])
            first = data.get(argv[1])
            if record:
                if argv[2] == '++':
                    set_key(argv[1], first[:-1] + [first[-1] + record[1:-1]])
                elif argv[2] == '**':
                    set_key(argv[1], [record[1:-1] + first[0]] + first[1:])
                elif argv[2] == '+*':
                    set_key(argv[1], first[:-1] + [record[1:-1] + first[-1]])
                elif argv[2] == '*+':
                    set_key(argv[1], [first[0] + record[1:-1]] + first[1:])
                elif argv[2] == '=':
                    set_key(argv[1], [record[1:-1]])
                elif argv[2] == '+':
                    set_key(argv[1], first + [record[1:-1]])
                elif argv[2] == '*':
                    set_key(argv[1], [record[1:-1]] + first)
            else:
                second = None if argv[3] == '.' else data[argv[3]]    
                if argv[2] == '#':
                    a, b = first, second
                    set_key(argv[1], b)
                    set_key(argv[3], a)
                elif argv[2] == '++':
                    set_key(argv[1], first[:-1] + [first[-1][:-1]])
                elif argv[2] == '+*':
                    set_key(argv[1], first[:-1] + [first[-1][1:]])
                elif argv[2] == '*+':
                    set_key(argv[1], [first[0][:-1]] + first[1:])
                elif argv[2] == '**':
                    set_key(argv[1], [first[0][1:]] + first[1:])
                elif argv[2] == '=':
                    if argv[3] == '.':
                        set_key(argv[1], None)
                    else:
                        set_key(argv[1], second)
                elif argv[2] == '+':
                    if argv[3] == '.':
                        set_key(argv[1], first[:-1])
                    else:
                        set_key(argv[1], first + second)
                elif argv[2] == '*':
                    if argv[3] == '.':
                        set_key(argv[1], first[1:])
                    else:
                        set_key(argv[1], second + first)

    except KeyError as err:
        print(f"[ERROR] Doesn't exist: {err.args[0]}")
    except AssertionError as ass:
        print(ass)
    except json.decoder.JSONDecodeError as err:
        print(err)
        print('[ERROR] You probably forgot or add an extra comma...')