
print(1/0)

import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # 共享资源，没有同步机制

threads = [threading.Thread(target=increment) for _ in range(10)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {counter}")
