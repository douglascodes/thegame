class MyEmptyClass:
    pass

def initlog(*args):
    pass #implement this later.

def fib(n):
    a, b = 0, 1
    while a <n:
        print a,
        a, b = b, a + b

def fib2(n): # return fibonacci series up to None
    """"Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)    #see below
        a, b = b, a+b
    return result

def ask_ok(prompt, retries=4, complaint="Yes or no, please!"):
    while True:
        ok = raw_input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nope', 'nop'):
            return False
        retries = retries - 1
        if retries < 0:
            raise IOError('refusenik user')
        print complaint

def parrot(voltage, state='a stiff', action='voom', breed='Norwegian Blue'):
    print "-- This parrot wouldn't", action
    print "if you put", voltage, "volts through it."
    print "--Lovely plumage, the", breed
    print "--It's", state, "!"

def cheeseshop(kind, *arguments, **keywords):
    print "-- Do you have any", kind, "?"
    print "-- I'm sorry, we're all out of", kind
    for arg in arguments:
        print arg
    print "-" * 40
    keys = sorted(keywords.keys())
    for kw in keys:
        print kw, ":", keywords[kw]

#cheeseshop("Limburger", "It's very runny, sir.",
#           "It's really very VERY runny, sir.",
#           shopkeeper="Michael Palin",
#           client="John Cleese",
#           sketch="Cheese Shop Sketch")

#d = {"voltage": "four million", "state": "bleedin' deceased", "action": "fly"}
#parrot(**d)

a = [66.25, 333, 333, 1, 1234.5]
a.count(333), a.count(66.25), a.count('x')
a.insert(2,-1)
a.append(333)

a.index(333)
a.remove(333)

a.reverse()
a.sort()

stack = [3,4,5]
stack.append(6)
stack.append(7)

stack.pop()
stack.pop()
stack.pop()
stack

from collections import deque
queue = deque(["eric", "john", "michael"])
queue.append("Terry")
queue.append("Graham")

squares = [x**2 for x in range(10)]
squares

[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]

matrix = [
          [1,2,3,4],
          [5,6,7,8],
          [9,10,11,12],          
          ]

xmatrix = [[row[i] for row in matrix] for i in range(4)]

