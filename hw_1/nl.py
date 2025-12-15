import sys

count = 1
if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        for line in file:
            print (f"{count} {line}", end = '' if line.endswith('\n') else '\n')
            count +=1
else:
    for line in sys.stdin:
        print (f"{count} {line}", end = '' if line.endswith('\n') else '\n')
        count +=1