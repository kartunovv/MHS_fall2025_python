import sys

if len(sys.argv) == 1:
    lines = sys.stdin.readlines()
    print()
    for line in lines[-17:]:
        print (line, end = '')

elif len(sys.argv) == 2 :
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines[-10:]:
        print (line, end = '' if line.endswith('\n') else '\n')

else:
    for i, arg in enumerate(sys.argv[1:]):
        if i > 0:
            print()
        filename = arg
        with open(filename, 'r') as file:
            print(f'==> {filename} <==')
            lines = file.readlines()
            for line in lines[-10:]:
                print(line, end='' if line.endswith('\n') else '\n')