

def add(a: int, b: int):
    print()
    return a + b


def subtract(a: int, b: int):
    print()
    return a - b


def multiply(a: int, b: int):
    print()
    return a * b


def divide(a: int, b: int):
    print()
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero. final answer is 0")
        return int(0)
    
if __name__ == "__main__":
    ...
