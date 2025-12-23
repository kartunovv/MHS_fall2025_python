from matrix_lib import find_hash_collision
import os

ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

A, C, B, D = find_hash_collision()
AB = A @ B
CD = C @ D

A.to_file(os.path.join(ARTIFACTS_DIR, "A.txt"))
C.to_file(os.path.join(ARTIFACTS_DIR, "C.txt"))
B.to_file(os.path.join(ARTIFACTS_DIR, "B.txt"))
D.to_file(os.path.join(ARTIFACTS_DIR, "D.txt"))
AB.to_file(os.path.join(ARTIFACTS_DIR, "AB.txt"))
CD.to_file(os.path.join(ARTIFACTS_DIR, "CD.txt"))

with open(os.path.join(ARTIFACTS_DIR, "hash.txt"), "w") as f:
    f.write(f"{hash(A)}\n{hash(C)}\n{hash(AB)}\n{hash(CD)}\n")