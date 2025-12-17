from pathlib import Path
from latexgen import generate_table, generate_image

data = [
    ["Name", "Age", "City"],
    ["Alice", 23, "Berlin"],
    ["Bob", 30, "Paris"],
]

table = generate_table(data)
image_path = Path(__file__).parent.parent / "artifacts" / "image.png"
image = generate_image(str(image_path))

document = f"""
\\documentclass{{article}}
\\usepackage{{graphicx}}

\\begin{{document}}

\\section*{{Generated Table}}
{table}

\\section*{{Generated Image}}
{image}

\\end{{document}}
"""

artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
artifacts_dir.mkdir(exist_ok=True)

output = artifacts_dir / "document.tex"
output.write_text(document)
