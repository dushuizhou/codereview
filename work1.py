class PeanoNumber:
    def __init__(self, value=0):
        self.value = value

    def successor(self):
        return PeanoNumber(self.value + 1)

    def predecessor(self):
        if self.value == 0:
            raise ValueError("Cannot find predecessor of 0")
        return PeanoNumber(self.value - 1)

    def is_zero(self):
        return self.value == 0

def add(a, b):
    if b.is_zero():
        return a
    return add(a.successor(), b.predecessor())

def subtract(a, b):
    if b.is_zero():
        return a
    if a.is_zero():
        raise ValueError("Result is negative")
    return subtract(a.predecessor(), b.predecessor())

def multiply(a, b):
    if b.is_zero():
        return PeanoNumber()
    return add(a, multiply(a, b.predecessor()))

def divide(a, b):
    if b.is_zero():
        raise ValueError("Cannot divide by zero")
    if a.is_zero():
        return PeanoNumber()
    quotient = PeanoNumber()
    remainder = a
    while compare(remainder, b) >= 0:
        quotient = quotient.successor()
        remainder = subtract(remainder, b)
    return quotient

def is_even(n):
    if n.is_zero():
        return True
    return is_odd(n.predecessor())

def is_odd(n):
    if n.is_zero():
        return False
    return is_even(n.predecessor())

def compare(a, b):
    if a.is_zero() and b.is_zero():
        return 0
    elif a.is_zero():
        return -1
    elif b.is_zero():
        return 1
    else:
        return compare(a.predecessor(), b.predecessor())
if __name__ == '__main__':

    a = PeanoNumber(9)
    b = PeanoNumber(2)
    print("Addition:", add(a, b).value)
    print("Subtraction:", subtract(a, b).value)
    print("Multiplication:", multiply(a, b).value)
    print("Division:", divide(a, b).value)
    print("Is 5 even?", is_even(a))
    print("Is 5 odd?", is_odd(a))
    print("Comparison (5, 3):", compare(a, b))
