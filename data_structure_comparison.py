import time
import matplotlib.pyplot as plt
from collections import defaultdict
import random

def find_duplicates_list(numbers):
    seen = []
    duplicates = []
    for num in numbers:
        if num in seen:
            duplicates.append(num)
        seen.append(num)
    return duplicates

def find_duplicates_set(numbers):
    seen = set()
    duplicates = []
    for num in numbers:
        if num in seen:
            duplicates.append(num)
        seen.add(num)
    return duplicates

def measure_performance(sizes):
    list_times = []
    set_times = []
    
    for size in sizes:
        # Create test data with duplicates
        numbers = list(range(size)) + list(range(size//2))
        random.shuffle(numbers)
        
        # Measure list performance
        start = time.time()
        find_duplicates_list(numbers)
        list_times.append(time.time() - start)
        
        # Measure set performance
        start = time.time()
        find_duplicates_set(numbers)
        set_times.append(time.time() - start)
    
    return list_times, set_times

def plot_results(sizes, list_times, set_times):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, list_times, 'b-', label='List Implementation')
    plt.plot(sizes, set_times, 'r-', label='Set Implementation')
    plt.xlabel('Input Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison: List vs Set')
    plt.legend()
    plt.grid(True)
    plt.savefig('performance_comparison.png')
    plt.close()

if __name__ == "__main__":
    # Test with different input sizes
    sizes = [1000, 2000, 5000, 10000, 20000]
    list_times, set_times = measure_performance(sizes)
    
    # Print results
    print("\nPerformance Results:")
    print("-" * 50)
    print(f"{'Input Size':<15} {'List Time':<15} {'Set Time':<15}")
    print("-" * 50)
    for i, size in enumerate(sizes):
        print(f"{size:<15} {list_times[i]:.4f}s{' '*8} {set_times[i]:.4f}s")
    
    # Create visualization
    plot_results(sizes, list_times, set_times)
    print("\nVisualization saved as 'performance_comparison.png'")
