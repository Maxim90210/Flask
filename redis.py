import redis
from functools import wraps

r = redis.Redis(host='localhost', port=6379, db=0)


def cache_fibonacci(func):
    @wraps(func)
    def wrapper(n):
        cached_result = r.get(f"fibonacci:{n}")
        if cached_result is not None:
            print(f"Взято з кешу: {n}")
            return int(cached_result)

        result = func(n)

        r.set(f"fibonacci:{n}", result)
        return result

    return wrapper


@cache_fibonacci
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    print(fibonacci(10))
    print(fibonacci(10)) 
