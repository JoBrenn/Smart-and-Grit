import copy

"""
from code.modules.district import District 
from code.modules.house import House
from code.modules.battery import Battery"""

def playground(district):
    
    pass

def test_depth():
    depth = 3
    stack = [""]
    while len(stack) > 0:
        state = stack.pop()
        print(state)
        if len(state) < depth:
            for i in ['L', 'R']:
                child = copy.deepcopy(state)
                child += i
                stack.append(child)

oo = [1,2,3,4,5]
print(oo.pop())
#test_depth()