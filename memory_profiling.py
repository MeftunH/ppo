from memory_profiler import profile
import numpy as np


@profile
def memory_hungry_function():
    # Bad practice: Creating large lists in memory
    big_list = [i * i for i in range(1000000)]

    # Better practice: Using generators
    better_approach = (i * i for i in range(1000000))

    # Best practice: Using NumPy for numerical operations
    numpy_array = np.arange(1000000) ** 2

    return sum(numpy_array)