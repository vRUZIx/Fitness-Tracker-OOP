import time
from pathlib import Path

print('Diagnostics script')

# Python environment
import sys
print('Python executable:', sys.executable)
print('Platform:', sys.platform)

# File I/O benchmark
root = Path(__file__).resolve().parents[1]
file_path = root / 'io_test.txt'

ITER = 200
write_start = time.perf_counter()
for i in range(ITER):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('x' * 1024)  # 1KB
write_end = time.perf_counter()

read_start = time.perf_counter()
for i in range(ITER):
    with open(file_path, 'r', encoding='utf-8') as f:
        _ = f.read()
read_end = time.perf_counter()

print(f'Wrote {ITER} x 1KB files in {write_end - write_start:.4f}s')
print(f'Read {ITER} x 1KB files in {read_end - read_start:.4f}s')

# Clean up
try:
    file_path.unlink()
except Exception:
    pass

print('Diagnostics complete')
