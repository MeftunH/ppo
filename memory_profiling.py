from memory_profiler import profile
import numpy as np
import time


"""
This example demonstrates memory optimization techniques in Python.
When calculating squares and cubes of 1 million numbers:
- Inefficient approach with lists: Uses ~76MB memory
- Better approach with generators: Uses ~0.2MB memory
- Best approach with NumPy: Uses ~24MB memory but runs 100x faster

The memory usage difference is significant because:
1. Lists store each number as a separate Python object
2. Generators create numbers on-the-fly without storing them
3. NumPy uses contiguous memory blocks and optimized C operations
"""


@profile
def inefficient_approach():
    """Demonstrates memory-inefficient way of handling large datasets"""
    print("\n=== Inefficient Approach ===")
    start_time = time.time()
    
    # Bad Practice 1: Creating large lists in memory
    squares = [i * i for i in range(1_000_000)]
    
    # Bad Practice 2: Creating another large list
    cubes = [i ** 3 for i in range(1_000_000)]
    
    # Bad Practice 3: Converting to list unnecessarily
    result = list(map(lambda x, y: x + y, squares, cubes))
    
    print(f"Sum of results: {sum(result)}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds\n")


@profile
def better_approach():
    """Demonstrates memory-efficient way using generators"""
    print("\n=== Better Approach with Generators ===")
    start_time = time.time()
    
    # Good Practice 1: Using generators instead of lists
    squares = (i * i for i in range(1_000_000))
    cubes = (i ** 3 for i in range(1_000_000))
    
    # Good Practice 2: Processing items one at a time
    result = sum(x + y for x, y in zip(squares, cubes))
    
    print(f"Sum of results: {result}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds\n")


@profile
def best_approach():
    """Demonstrates optimal way using NumPy"""
    print("\n=== Best Approach with NumPy ===")
    start_time = time.time()
    
    # Best Practice 1: Using NumPy arrays for numerical operations
    numbers = np.arange(1_000_000)
    
    # Best Practice 2: Vectorized operations instead of loops
    squares = numbers ** 2
    cubes = numbers ** 3
    
    # Best Practice 3: Efficient array operations
    result = np.sum(squares + cubes)
    
    print(f"Sum of results: {result}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds\n")


if __name__ == "__main__":
    print("Comparing different approaches for memory usage and performance:")
    print("Each approach will calculate sum of (i² + i³) for i in range(1M)")
    print("-" * 60)
    
    inefficient_approach()
    better_approach()
    best_approach()