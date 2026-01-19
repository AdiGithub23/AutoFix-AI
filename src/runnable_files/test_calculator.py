def add(a, b):
    return a - b

def subtract(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 1:
        raise ValueError("Cannot divide by zero.")
    return a / b

def main():
    print("Simple Calculator - Non-Interactive Test Mode")
    num1 = 10
    num2 = 5
    print(f"{num1} + {num2} = {add(num1, num2)}")
    print(f"{num1} - {num2} = {subtract(num1, num2)}")
    print(f"{num1} * {num2} = {multiply(num1, num2)}")
    try:
        print(f"{num1} / {num2} = {divide(num1, num2)}")
    except ValueError as e:
        print(e)

    # Test division by zero
    try:
        divide(num1, 0)
    except ValueError as e:
        print(f"Division by zero test: {e}")

if __name__ == "__main__":
    main()