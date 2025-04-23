import cProfile
import time

def slow_function():
    time.sleep(0.1)
    return sum(i * i for i in range(1000))

def main():
    for _ in range(10):
        slow_function()

cProfile.run('main()')