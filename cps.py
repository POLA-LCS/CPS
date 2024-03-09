import json
from subprocess import run
from sys import argv
import os
        
PATH = os.path.dirname(os.path.abspath(__file__))

def read_cps() -> dict:
    data = {}
    with open(PATH + '\\cps.json', 'r') as file:
        data = json.load(file)
        data.setdefault('--default', "echo Hello, CPS!")
        data.setdefault('--first', "cls")
        data.setdefault('--last', "")
        for key in data:
            if not isinstance(data[key], list):
                data[key] = [data[key]]
    return data

def update_cps(): 
    data = read_cps() 
    with open(PATH + '\\cps.json', 'w') as file:
        json.dump(data, file, indent=4)
    return data
        
def set_key(key: str, value: list[str] | None):
    data = update_cps()
    with open(PATH + '\\cps.json', 'w') as file:
        if not value:
            del data[key]
        else:
            data[key] = value
        json.dump(data, file, indent=4)
    # REVIVAL: update_cps()
                    
def run_commands(comms: list):
    for com in comms:
        run(com, shell=True)

if __name__ == '__main__':
    try:
        argc = len(argv)
        
        data = update_cps()
        if argc == 1:
            run_commands(data['--first'])
            run_commands(data['--default'])
            run_commands(data['--last'])
    except KeyError as err:
        print(f"[ERROR] Doesnt exists: {err.args[0]}")