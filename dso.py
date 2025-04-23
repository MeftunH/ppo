from collections import defaultdict
import time

# Measuring list vs set performance
def find_duplicates_list(numbers):
    seen = []
    duplicates = []
    for num in numbers:
        if num in seen:  # O(n) operation
            duplicates.append(num)
        seen.append(num)
    return duplicates

def find_duplicates_set(numbers):
    seen = set()
    duplicates = []
    for num in numbers:
        if num in seen:  # O(1) operation
            duplicates.append(num)
        seen.add(num)
    return duplicates

# Real-world test
numbers = list(range(10000)) + list(range(5000))
start = time.time()
find_duplicates_list(numbers)
print(f"List time: {time.time() - start:.4f} seconds")

start = time.time()
find_duplicates_set(numbers)
print(f"Set time: {time.time() - start:.4f} seconds")