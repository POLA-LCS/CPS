import json
from subprocess import run
from os.path import dirname, abspath
from sys import argv
from platform import system

PATH = dirname(abspath(__file__))
JSON_PATH = PATH + '/cps.json'
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

CodeType = list[str]
MacroType = tuple[dict[str, str], CodeType]
DataBase = dict[str, MacroType]

def get_blocks() -> DataBase:
    with open(JSON_PATH, 'r') as file:
        return json.load(file)

DEFAULT_MACRO: tuple[str, MacroType] = ('0', ({'name': 'CPS'}, ['cls' if system() == 'Windows' else 'clear', 'echo Hello, %%name!']))
def set_default(data: DataBase):
    with open(JSON_PATH, 'w') as file:
        data.setdefault(*DEFAULT_MACRO)
        for macro in data:
            block = data[macro][1]
            if not isinstance(block, list):
                data[macro] = (data[macro][0], [block])
        json.dump(data, file, indent=INDENT)

def default_arguments(func: MacroType) -> CodeType:
    param, code = func
    if len(param) == 0:
        return code
    new_code: CodeType = []
    for line in code:
        for i, name in enumerate(param):
            template = VAR_TEMPLATE.replace('#', name)
            line = line.replace(template, param[name])
        new_code.append(line)
    
    return new_code

def replace_arguments(func: MacroType, input_param: list[str] | None = None) -> CodeType:
    if not input_param:
        return default_arguments(func)
    param, code = func
    if len(param) == 0:
        return code
    new_code: CodeType = []
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
    
def run_commands(func: CodeType):
    for comm in func:
        run(comm, shell=True)
    
def display_help():
    print(f"""[CPS] Help:
          
Nomenclature:
    M = Macro     :    The name of a macro
    P = Prompt    :    A command prompt
Info:
    ({C_HELP[0]} | {C_HELP[1]})    Display this text
    ({C_INFO[0]} | {C_INFO[1]})    Display all the user MACROs info
    M ({C_INFO[0]} | {C_INFO[1]})  Display macro info
Run:
    <nothing>     Run default macro with default arguments
    M             Run M with default arguments
    M % <p...>    Run M with arguments <p>
    
    Tip: Dot (.) skips argument assign
Set:
    M {O_SET} P    Set P to M
    M {O_APP} P    Append P with the same logic as set
    M {O_PRE} P    Prepend P with the same logic as set
    M {O_STC} M2   Switch M with M2
    
    Tip: To copy macros use (M = %%M2)
Delete:
    M {O_SET} .    Deletes M
    M {O_APP} .    Deletes the last command of M
    M {O_PRE} .    Deletes the first command of M
Arguments:
    M %% A P       Set macro M argument A prompt to P
    M %% A .       Deletes argument A from M
    """)

def print_cps(message: str):
    print(f"[CPS] {message}")

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
                # INFO (SKIPS 0 IF THERE'S MORE)
                if len(data) == 1:
                    print_cps(f"0 {data['0'][0]}")
                    for line in data['0'][1]:
                        print(f"  - {line}")
                else:
                    print_cps("Info:")
                    for macro in data:
                        if macro == '0':
                            continue
                        print(f"  -  {macro} {data[macro][0]} : {data[macro][1]}")
            else: # cps <m>
                # DEFAULT RUN
                run_commands(replace_arguments(data[argv[1]]))
        elif argc >= 3:
            if argv[2] == O_SET_PARAM: # cps <m> %% <param> <prompt>
                # SET A MACRO PARAMETER
                if argv[4] == '.':
                    del data[argv[1]][0][argv[3]]
                    print(f"[CPS] {argv[1]} -> {argv[3]} was deleted.")
                else:
                    data[argv[1]][0][argv[3]] = argv[4]
            elif argv[2] == O_PARAM: # cps <m> % <p...>
                # RUN MACRO WITH PARAMETERS
                run_commands(replace_arguments(data[argv[1]], argv[3:]))
            elif argc == 3:
                # check if the prompt is a macro
                prompts = argv[3].split(' ')
                bar = None
                if len(prompts) == 1 and prompts[0].startswith(O_SET_PARAM):
                    bar = prompts[0][2:]
                if argv[2] == O_SET: # cps <m> = <prompt / macro>
                    # SET TO macro A prompt
                    if argv[3] == '.': # deletes macro
                        del data[argv[1]]
                        print(f"[CPS] Deleted: {argv[1]}")
                    elif data.get(argv[1]):
                        if bar: # set macro prompts to macro
                            data[argv[1]][1] = data[bar][1]
                        else: # set prompt to macro
                            data[argv[1]][1] = [argv[3]]
                    elif bar: # create macro with macro prompts
                        data[argv[1]] = data[bar]
                        print(f"[CPS] Created: {argv[1]}")
                    else: # create macro with prompt
                        data[argv[1]] = ({}, [argv[3]])
                        print(f"[CPS] Created: {argv[1]}")
                elif argv[2] == O_APP: # cps <m> + <prompt / macro>
                    # APPEND TO macro A prompt
                    if argv[3] == '.': # deletes the last command
                        del data[argv[1]][1][-1]
                    elif bar: # appends a macro prompts
                        data[argv[1]][1] += data[bar][1]
                    else: # appends a prompt
                        data[argv[1]][1].append(argv[3])
                elif argv[2] == O_PRE:
                    # PREPEND TO macro A prompt
                    if argv[3] == '.': # deletes the first command
                        del data[argv[1]][1][0]
                    elif bar: # prepends a macro prompts
                        data[argv[1]][1] = data[bar][1] + data[argv[1]][1]
                    else: # prepends a prompt
                        data[argv[1]][1] = [argv[3]] + data[argv[1]][1]
                elif argv[2] == O_STC:
                    data[argv[1]], data[argv[3]] = data[argv[3]], data[argv[1]]
                    print(f"[CPS] Switched {argv[1]} with {argv[3]}")
        elif argc >= 2:
            if argv[1] == O_PARAM:
                # RUN DEFAULT WITH PARAMETERS
                run_commands(replace_arguments(data['0'], argv[2:]))
            elif argc == 2:
                first = data[argv[1]]
                if argv[2] in C_INFO: # cps <m> --info
                    # MACRO INFO
                    print(f"[CPS] {argv[1]} {first[0]}:")
                    for line in first[1]:
                        print(f"  -  {line}")
        set_default(data)
    except FileNotFoundError as not_found:
        print(f"[CPS] It seems there's is no data loaded")
        result = input("[CPS] Create new data file? (Y/...) >> ")
        if result == 'Y':
            with open(JSON_PATH, 'w') as file:
                file.write('{\n\n}')
                print('[CPS] New data file was successfully created.')
    except KeyError as kerr:
        print(f"[CPS ERROR] Doesn't exist: {kerr.args[0]}")
    except AssertionError as ass:
        print(ass)
    except json.decoder.JSONDecodeError as json_error:
        print(f"[CPS ERROR] File content not valid:")
        print(json_error, json_error)
