# fibonacci numbers module

def fib(n):
    a, b = 0, 1
    while b < n:
        print b
        a, b = b, a+b
            
def fibo2(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = a+b
    return result

        