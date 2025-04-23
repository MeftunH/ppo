import time
from typing import List, Tuple
import numpy as np

def find_closest_pairs_naive(points: List[Tuple[float, float]], target_distance: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Find pairs of points with distance close to target (naive approach)"""
    result = []
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            distance = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            if abs(distance - target_distance) < 0.1:
                result.append((p1, p2))
    return result

def find_closest_pairs_optimized(points: List[Tuple[float, float]], target_distance: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Find pairs of points with distance close to target (optimized approach)"""
    result = []
    points_array = np.array(points)
    
    # Use broadcasting for vectorized distance calculation
    distances = np.sqrt(((points_array[:, np.newaxis] - points_array) ** 2).sum(axis=2))
    
    # Find pairs with distances close to target
    close_pairs = np.where(np.abs(distances - target_distance) < 0.1)
    
    # Filter out duplicates and self-pairs
    for i, j in zip(*close_pairs):
        if i < j:  # Avoid duplicates and self-pairs
            result.append((tuple(points[i]), tuple(points[j])))
    
    return result

def benchmark_comparison(n_points: int = 1000):
    """Compare performance of both implementations"""
    # Generate random points
    points = [(float(x), float(y)) for x, y in np.random.rand(n_points, 2)]
    target = 0.5  # Target distance
    
    # Test naive implementation
    start = time.time()
    naive_result = find_closest_pairs_naive(points, target)
    naive_time = time.time() - start
    
    # Test optimized implementation
    start = time.time()
    optimized_result = find_closest_pairs_optimized(points, target)
    optimized_time = time.time() - start
    
    print(f"\nBenchmark Results (n={n_points} points):")
    print(f"Naive implementation: {naive_time:.4f} seconds")
    print(f"Optimized implementation: {optimized_time:.4f} seconds")
    print(f"Speedup factor: {naive_time/optimized_time:.2f}x")
    print(f"Pairs found: {len(naive_result)} (naive) vs {len(optimized_result)} (optimized)")

if __name__ == "__main__":
    benchmark_comparison(1000)
    benchmark_comparison(2000)
