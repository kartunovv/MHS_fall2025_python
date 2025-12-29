# rot13_pipeline.py
import multiprocessing
import threading
import time
import sys
import codecs

def clean_ascii(s: str) -> str:
    return ''.join(c if c.isascii() and (c.isalnum() or c in ' _-') else '?' for c in s)

def process_a(q_in, q_out):
    while True:
        msg = q_in.get()
        if msg is None:
            break
        lower = msg.lower()
        q_out.put((msg, lower))
        time.sleep(5)

def process_b(q_in, q_out):
    while True:
        orig, lower = q_in.get()
        if orig is None:
            break
        rot = codecs.encode(clean_ascii(lower), 'rot_13')
        print(rot, flush=True)
        q_out.put((time.time(), orig, lower, rot))

def stdin_reader(q):
    for line in sys.stdin:
        q.put(line.rstrip('\n'))
    q.put(None)

def main():
    q_a = multiprocessing.Queue()
    q_b = multiprocessing.Queue()
    q_main = multiprocessing.Queue()

    p_a = multiprocessing.Process(target=process_a, args=(q_a, q_b))
    p_b = multiprocessing.Process(target=process_b, args=(q_b, q_main))
    p_a.start()
    p_b.start()

    threading.Thread(target=stdin_reader, args=(q_a,), daemon=True).start()

    with open("artifacts/rot13_log.txt", "w", encoding="utf-8") as f:
        f.write("Время → Исходная → lower → rot13\n")
        f.write("-" * 50 + "\n")
        try:
            while True:
                ts, orig, lower, rot = q_main.get()
                safe_orig = orig.encode('utf-8', errors='replace').decode('utf-8')
                safe_lower = lower.encode('utf-8', errors='replace').decode('utf-8')
                safe_rot = rot.encode('utf-8', errors='replace').decode('utf-8')
                t_str = time.strftime("%H:%M:%S", time.localtime(ts))
                f.write(f"[{t_str}] '{safe_orig}' → '{safe_lower}' → '{safe_rot}'\n")
                f.flush()
        except KeyboardInterrupt:
            pass

    p_a.join(timeout=1)
    p_b.join(timeout=1)
    p_a.terminate()
    p_b.terminate()

if __name__ == "__main__":
    main()