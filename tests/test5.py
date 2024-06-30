import time
import random

from curby.generate.compilationsonggenerator import optimizied_sponsors, get_extract_zone

a_list = [1, 2, 3, 4, 5]
del a_list[-1]
print(a_list)

"""
segments = [(1, 5), (2, 6), (10, 12), (16, 19), (17, 20)]
print(segments)
"""

segments = []
last_number = 0
for i in range(10):
    first = random.randint(0, i)
    segments.append((first, first + random.randint(5, 5 + i)))

print(segments)

start_time = time.perf_counter()
sponsors = optimizied_sponsors(segments, lambda element : element[0], lambda element : element[1])
end_time = time.perf_counter()
print(end_time - start_time)
print(sponsors)

start_time = time.perf_counter()
sponsors = []
for zone in get_extract_zone(segments, lambda element : element[0], lambda element : element[1]):
    sponsors.append(zone)
end_time = time.perf_counter()
print(end_time - start_time)
print(sponsors)

start_time = time.perf_counter()
end_time = time.perf_counter()
print(end_time - start_time)
print(sponsors)