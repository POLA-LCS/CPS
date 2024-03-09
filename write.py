print("To stop writing send '.'")
name = input("Name -> ")
program = [
    input(">> ")
]
while program[-1] != '.':
    program.append(input(">> "))
    
if input("Confirm (Y) -> ") == 'Y':
    with open(name, 'w') as file:
        for prog in program[:-1]:
            file.write(prog)