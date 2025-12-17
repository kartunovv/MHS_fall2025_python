def generate_table(data):
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("На вход должен быть подан двойной список")

    cols = len(data[0])
    col_format = "|".join(["c"] * cols)

    lines = [
        "\\begin{tabular}{" + f"|{col_format}|" + "}",
        "\\hline"
    ]

    for row in data:
        line = " & ".join(map(str, row)) + " \\\\ \\hline"
        lines.append(line)

    lines.append("\\end{tabular}")

    return "\n".join(lines)


def generate_image(image_path, width="0.5\\textwidth"):
    return "\n".join([
        "\\begin{figure}[h]",
        "\\centering",
        f"\\includegraphics[width={width}]{{{image_path}}}",
        "\\end{figure}"
    ])
