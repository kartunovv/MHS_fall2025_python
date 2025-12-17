from pathlib import Path
from latexgen import generate_table

data = [
    ["Name", "Age", "City"],
    ["Alice", 23, "Berlin"],
    ["Bob", 30, "Paris"],
]

latex = generate_table(data)

artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
artifacts_dir.mkdir(exist_ok=True)

output_path = artifacts_dir / "table.tex"

with open(output_path, "w") as f:
    f.write(latex)