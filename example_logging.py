from libs.log import *


@track(level=info)
def euler(n=100):
    return sum(range(1, n+1))


if __name__ == "__main__":
    success("Hello world!")

    n = 100
    success(f"Sum of integers from 1 to {n}: {euler(n)}.")
