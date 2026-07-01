import time

dtime = time.monotonic()
print(dtime)

onetime = time.monotonic()
print(onetime)

time.sleep(5)

twotime = time.monotonic()
print(twotime)

print("Elapsed time:", twotime - onetime)
