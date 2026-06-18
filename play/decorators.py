import functools
from functools import wraps
# A simple decorator that logs the calls to a function, including its arguments and return value.
import time


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"-> {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"<- returned {result!r}")
        return result
    return wrapper


@log_calls
def add(a, b):
    return a + b


add(2, 3)
# A simple decorator that measures the execution time of a function.


def my_decorator(func):
    def wrapper():
        print("Something before the function.")
        result = func()
        print("Something after the function.")
        print(f"Function returned: {result}")
        return result
    return wrapper


@my_decorator
def say_hello():
    print("Hello!")
    return "Hello returned"


say_hello()


def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(2)
def hello():
    print('hello jarvis')


hello()


def debug_decorator(func):
    """
    Prints function arguments and return value.
    Great for debugging!
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        print(f"🔍 Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} returned {result!r}")

        return result
    return wrapper


def timing_decorator(func):
    """
    Measures and logs function execution time.
    One of the most common decorator patterns!
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️ {func.__name__} took {elapsed:.3f} seconds")
        return result
    return wrapper


def slow_down(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(2)
        return func(*args, **kwargs)
    return wrapper


@timing_decorator
@debug_decorator
@slow_down
def slowed_reverbed():
    print("this function have been slowed down")


slowed_reverbed()
