import time
import threading
import multiprocessing

def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

N = 500_000
RUNS = 10

def sync_run():
    start = time.perf_counter()
    results = [fib(N) for _ in range(RUNS)]
    return time.perf_counter() - start, results

def thread_worker(n, results, idx):
    results[idx] = fib(n)

def threading_run():
    threads = []
    results = [None] * RUNS
    start = time.perf_counter()
    for i in range(RUNS):
        t = threading.Thread(target=thread_worker, args=(N, results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start, results

def multiprocessing_run():
    with multiprocessing.Pool(processes=RUNS) as pool:
        start = time.perf_counter()
        results = pool.map(fib, [N] * RUNS)
        return time.perf_counter() - start, results

if __name__ == "__main__":
    t_sync, res_sync = sync_run()

    t_thread, res_thread = threading_run()

    t_proc, res_proc = multiprocessing_run()

    assert res_sync == res_thread == res_proc, "Результаты не совпадают!"
    
    with open("artifacts/fib_results.txt", "w", encoding="utf-8") as f:
        f.write("=== 4.1: fib(n=500_000), 10 запусков ===\n")
        f.write(f"sync:           {t_sync:7.3f} с\n")
        f.write(f"threading:      {t_thread:7.3f} с\n")
        f.write(f"multiprocessing: {t_proc:7.3f} с\n")
        f.write("\nВывод: threading почти не ускоряет (GIL), multiprocessing — да.\n")
    
    print("\n📁 Артефакт сохранён: artifacts/fib_results.txt")