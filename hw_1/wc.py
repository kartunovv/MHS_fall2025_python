import sys

if len(sys.argv) == 1:
    lines = sys.stdin.readlines()
    lines_count = 0
    words_count = 0
    bytes_count = 0
    for line in lines:
        lines_count += 1
        words_count += len(line.split())
        bytes_count += len(line.encode('utf-8'))

    print(f"{lines_count} {words_count} {bytes_count}")

elif len(sys.argv) == 2:
    filename = sys.argv[1]
    lines_count = 0
    words_count = 0
    bytes_count = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            lines_count += 1
            words_count += len(line.split())
            bytes_count += len(line.encode('utf-8'))

    print(f"{lines_count} {words_count} {bytes_count} {filename}")

else:
    total_lines = 0
    total_words = 0
    total_bytes = 0
    for arg in sys.argv[1:]:
        filename = arg
        lines_count = 0
        words_count = 0
        bytes_count = 0
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                lines_count += 1
                words_count += len(line.split())
                bytes_count += len(line.encode('utf-8'))
            print(f"{lines_count} {words_count} {bytes_count} {filename}\n")

            total_lines += lines_count
            total_words += words_count
            total_bytes += bytes_count
            
    print(f"{total_lines} {total_words} {total_bytes} total")