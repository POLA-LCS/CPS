import json
from subprocess import run
from os.path import dirname, abspath
from sys import argv
from typing import Any

PATH = dirname(abspath(__file__))
JSON_PATH = PATH + '\\cps.json'
INDENT = 4

O_PARAM = '%'
O_SET_PARAM = '%%'
VAR_TEMPLATE = f'{O_SET_PARAM}#'

O_SET = '='
O_APP = '+'
O_PRE = '-'
O_STC = '#'

C_INFO = ('--info', '-i')
C_HELP = ('--help', '-h')

codeType = list[str]
funcType = tuple[dict[str, str], codeType]
dataBase = dict[str, funcType]

def get_blocks() -> dataBase:
    with open(JSON_PATH, 'r') as file:
        return json.load(file)

def set_default(data: dataBase):
    with open(JSON_PATH, 'w') as file:
        data.setdefault('0', ({'name': 'CPS'}, ['cls', 'echo Hello, %%name!']))
        for key in data:
            block = data[key][1]
            if not isinstance(block, list):
                data[key[1]] = [block]
        json.dump(data, file, indent=INDENT)

def default_arguments(func: funcType) -> list[str]:
    param, code = func
    if len(param) == 0:
        return code
    new_code: list[str] = []
    for line in code:
        for i, name in enumerate(param):
            template = VAR_TEMPLATE.replace('#', name)
            line = line.replace(template, param[name])
        new_code.append(line)
    
    return new_code

def replace_arguments(func: funcType, input_param: list | None = None) -> list[str]:
    if not input_param:
        return default_arguments(func)
    param, code = func
    if len(param) == 0:
        return code
    new_code: list[str] = []
    for line in code:
        for i, name in enumerate(param):
            template = VAR_TEMPLATE.replace('#', name)
            if len(input_param) > i and input_param[i] != '.':
                val = input_param[i]
            else:
                val = param[name]
            line = line.replace(template, val)
        new_code.append(line)
    return new_code
    
def run_commands(func: list[str]):
    for comm in func:
        run(comm, shell=True)
    
def display_help():
    print(f"""[CPS] Help:
Nomenclature:
    F = Function  :    The name of a function
    V = Value     :    A string value
Info:
    cps ({C_HELP[0]} | {C_HELP[1]})    Display this text
    cps ({C_INFO[0]} | {C_INFO[1]})    Display all the user keys info
    cps F ({C_INFO[0]} | {C_INFO[1]})  Display key info
Run:
    cps               Run 0 with default arguments
    cps F             Run F with default arguments
    cps F % <p...>    Run F with arguments <p>
    
    Tip: Dot (.) skips argument assign
Set:
    cps F {O_SET} V    Set V to F
    cps F {O_APP} V    Append V with the same logic as set
    cps F {O_PRE} V    Prepend V with the same logic as set
    cps F {O_STC} F2   Switch F with F2
    
    Tip: "%%V" = The values of a function (cps F = %%V)
Delete:
    cps F {O_SET} .    Deletes F
    cps F {O_APP} .    Deletes the last command of F
    cps F {O_PRE} .    Deletes the first command of F
Arguments:
    cps F %% A V       Set function F argument A value to V
    cps F %% A .       Deletes argument A from F
    """)
    
if __name__ == '__main__':
    try:
        data = get_blocks()
        set_default(data)
        argc = len(argv[1:])
        
        if argc == 0:
            # DEFAULT RUN
            run_commands(replace_arguments(data['0']))
        elif argc == 1:
            if argv[1] in C_HELP: # cps --help 
                # DISPLAY HELP
                display_help()
            elif argv[1] in C_INFO: # cps --info
                # INFO (SKIPS 0 IF THERES MORE)
                if len(data) == 1:
                    print(f'[CPS] 0 {data['0'][0]}')
                    for line in data['0'][1]:
                        print(f'  - {line}')
                else:
                    print(f'[CPS] Info:')
                    for key in data:
                        if key == '0':
                            continue
                        print(f'  -  {key} {data[key][0]} : {data[key][1]}')
            else: # cps <k>
                # DEFAULT RUN
                run_commands(replace_arguments(data[argv[1]]))
        elif argc >= 3:
            if argv[2] == O_SET_PARAM: # cps <k> %% <param> <value>
                # SET A KEY PARAMETER
                if argv[4] == '.':
                    del data[argv[1]][0][argv[3]]
                    print(f'[CPS] {argv[1]} -> {argv[3]} was deleted.')
                else:
                    data[argv[1]][0][argv[3]] = argv[4]
            elif argv[2] == O_PARAM: # cps <k> % <p...>
                # RUN KEY WITH PARAMETERS
                run_commands(replace_arguments(data[argv[1]], argv[3:]))
            elif argc == 3:
                # check if the value is a key
                values = argv[3].split(' ')
                bar = None
                if len(values) == 1 and values[0].startswith(O_SET_PARAM):
                    bar = values[0][2:]
                if argv[2] == O_SET: # cps <k> = <value / key>
                    # SET TO KEY A VALUE
                    if argv[3] == '.': # deletes key
                        del data[argv[1]]
                        print(f'[CPS] Deleted: {argv[1]}')
                    elif data.get(argv[1]):
                        if bar: # set key values to key
                            data[argv[1]][1] = data[bar][1]
                        else: # set value to key
                            data[argv[1]][1] = [argv[3]]
                    elif bar: # create key with key values
                        data[argv[1]] = data[bar]
                        print(f'[CPS] Created: {argv[1]}')
                    else: # create key with value
                        data[argv[1]] = ({}, [argv[3]])
                        print(f'[CPS] Created: {argv[1]}')
                elif argv[2] == O_APP: # cps <k> + <value / key>
                    # APPEND TO KEY A VALUE
                    if argv[3] == '.': # deletes the last command
                        del data[argv[1]][1][-1]
                    elif bar: # appends a key values
                        data[argv[1]][1] += data[bar][1]
                    else: # appends a value
                        data[argv[1]][1].append(argv[3])
                elif argv[2] == O_PRE:
                    # PREPREND TO KEY A VALUE
                    if argv[3] == '.': # deletes the first command
                        del data[argv[1]][1][0]
                    elif bar: # prepends a key values
                        data[argv[1]][1] = data[bar][1] + data[argv[1]][1]
                    else: # preprends a value
                        data[argv[1]][1] = [argv[3]] + data[argv[1]][1]
                elif argv[2] == O_STC:
                    data[argv[1]], data[argv[3]] = data[argv[3]], data[argv[1]]
                    print(f'[CPS] Switched {argv[1]} with {argv[3]}')
        elif argc >= 2:
            if argv[1] == O_PARAM:
                # RUN DEFAULT WITH PARAMETERS
                run_commands(replace_arguments(data['0'], argv[2:]))
            elif argc == 2:
                first = data[argv[1]]
                if argv[2] in C_INFO: # cps <k> --info
                    # KEY INFO
                    print(f'[CPS] {argv[1]} {first[0]}:')
                    for line in first[1]:
                        print(f'  -  {line}')
        set_default(data) # FINISHED AND UPDATE
    except FileNotFoundError as not_found:
        print(f"[CPS] It seems there's is no data loaded")
        result = input("[CPS] Create new data file? (Y/...) >> ")
        if result == 'Y':
            with open(JSON_PATH, 'w') as file:
                file.write('{\n\n}')
                print('[CPS] New data file was successfully created.')
    except KeyError as kerr:
        print(f"[CPS ERROR] Doesn't exists: {kerr.args[0]}")
    except AssertionError as ass:
        print(ass)
    except json.decoder.JSONDecodeError as json_error:
        print(f"[CPS ERROR] File content not valid:")
        print(json_error, json_error)
        