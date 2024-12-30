import time
import threading

# Thread-local storage to track call stack depth
thread_local = threading.local()

def timeit(func):
    def wrapper(*args, **kwargs):
        # Initialize call depth counter if not already set
        if not hasattr(thread_local, 'call_depth'):
            thread_local.call_depth = 0

        # Check if we're at the first level of the call stack
        is_first_level = thread_local.call_depth == 0
        thread_local.call_depth += 1

        try:
            if is_first_level:
                start_time = time.time()  # Record the start time
                result = func(*args, **kwargs)  # Call the original function
                end_time = time.time()  # Record the end time
                runtime = (end_time - start_time) * 1000  # Convert to milliseconds
                print(f"Function '{func.__name__}' executed in {runtime:.4f} ms")
                return result
            else:
                # Call the function normally if it's not first level
                return func(*args, **kwargs)
        finally:
            # Decrement the call depth counter
            thread_local.call_depth -= 1

    return wrapper