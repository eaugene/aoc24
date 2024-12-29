import time
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        runtime = end_time - start_time
        print(f"Function '{func.__name__}' executed in {runtime:.4f} seconds")
        return result
    return wrapper