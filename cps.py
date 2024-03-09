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
    print("""[USAGE] CPS:
    Info:
    - cps (--help | -h)     Display help text
    - cps (--info | -i)     Display all the key infos
    - cps a (--info | -i)   Display "a" key info

    Run:
    - cps                   Run !first, !default and !last
    - cps a                 Run !first, "a" key and !last
    - cps (--clean | -c)    Run !default
    - cps a (--clean | -c)  Run "a" key

    Set (prefixed by cps):
    - a = 'b'    Set "a" key to 'b' command
    - a = b      Set "a" key yo "b" key
    - a + 'b'    Append 'b' command to the bottom of "a" key
    - a + b      Append "b" key commands to the bottom of "a" key
    - a * 'b'    Append 'b' command to the top of "a" key
    - a * b      Append "b" key commands to the top of "a" key
    - a = .      Delete "a" key
    - a + .      Pop the last element of "a" key
    - a * .      Pop the first element of "a" key
    - a | b      Switch "a" key with "b" key""")

if __name__ == '__main__':
    try:
        argc = len(argv)
        
        data = update_cps()
        print(argv)
        if argc == 1:
            run_commands(data['!first'])
            run_commands(data['!default'])
            run_commands(data['!last'])
        elif argc == 2:
            if argv[1] in ['--help', '-h']:
                HELP()
    except KeyError as err:
        print(f"[ERROR] Doesnt exists: {err.args[0]}")