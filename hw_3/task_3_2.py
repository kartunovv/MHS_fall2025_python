import numpy as np
from matrix_lib import SmartMatrix
import os

ARTIFACTS_DIR = "artifacts"

np.random.seed(0)
A = SmartMatrix(np.random.randint(0, 10, (10, 10)))
B = SmartMatrix(np.random.randint(0, 10, (10, 10)))

os.makedirs(ARTIFACTS_DIR, exist_ok=True)
(A + B).to_file(os.path.join(ARTIFACTS_DIR, "matrix+.txt"))
(A * B).to_file(os.path.join(ARTIFACTS_DIR, "matrix*.txt"))
(A @ B).to_file(os.path.join(ARTIFACTS_DIR, "matrix@.txt"))