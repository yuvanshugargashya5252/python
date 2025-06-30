# def second(func):
#     def test():
#         print("Second")
#         func()
#     return test

# @second
# def first():
#     print("first")

def addExtra(func):
    def extra(a,b):
        return func(a,b) + 2
    return extra

@addExtra
def addNum(a,b):
    return a+b

# first()
print(addNum(1,2))