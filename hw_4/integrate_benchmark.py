import time
import math
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def integrate_chunk(args):
    start, end, count, func_name = args
    if count == 0:
        return 0.0
    local_step = (end - start) / count
    acc = 0.0
    x = start
    if func_name == "cos":
        f = math.cos
    else:
        raise ValueError(f"Неизвестная функция: {func_name}")
    for _ in range(count):
        acc += f(x) * local_step
        x += local_step
    return acc

def integrate(a, b, *, n_jobs=1, n_iter=10_000_000, func_name="cos"):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    chunks = []
    for i in range(n_jobs):
        start_i = i * chunk_size
        end_i = n_iter if i == n_jobs - 1 else (i + 1) * chunk_size
        start_x = a + start_i * step
        end_x = a + end_i * step
        count = end_i - start_i
        chunks.append((start_x, end_x, count, func_name))

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=n_jobs) as ex:
        res_thread = sum(ex.map(integrate_chunk, chunks))
    t_thread = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=n_jobs) as ex:
        res_process = sum(ex.map(integrate_chunk, chunks))
    t_process = time.perf_counter() - start

    assert abs(res_thread - res_process) < 1e-3, "Результаты расходятся"
    return t_thread, t_process

def main():
    cpu_count = multiprocessing.cpu_count()
    n_jobs_list = list(range(1, cpu_count * 2 + 1))
    a, b = 0, math.pi / 2

    lines = ["n_jobs | ThreadPool (с) | ProcessPool (с)", "-" * 42]
    for n_jobs in n_jobs_list:
        t_thread, t_proc = integrate(a, b, n_jobs=n_jobs)
        lines.append(f"{n_jobs:6} | {t_thread:15.3f} | {t_proc:15.3f}")

    with open("artifacts/integrate_results.txt", "w", encoding="utf-8") as f:
        f.write("=== 4.2: integrate(cos, 0, π/2), n_iter=10_000_000 ===\n")
        f.write("\n".join(lines))
        f.write("\n\nВывод: ProcessPool эффективнее при росте n_jobs (CPU-bound задача).\n")

if __name__ == "__main__":
    main()