# # print(help("modules"))

# class Car:
#     color = "white"

#     def __init__(self , model , price):
#         self.model = model
#         self.price = price
    
#     def getColor(self):
#         return self.colorr
    
#     def setColor(self , color):
#         car1.price=12
#         self.colorr = color
#         car1.colorr = color

# class Maruti(Car):
#     def __init__(self, model, price):
#         super().__init__(model, price)
#         self.drive = True
    
# car1 = Car("fortuner", 50)
# car2 = Car("fortuner",55)
# car2.setColor("black")
# print(car2.getColor())
# print(car1.getColor())
# print(car1.price)

# mar = Maruti("creta",12)
# print(mar.color ,"maruti")
# print(mar.drive ,"maruti")

class A:
    def first(self):
        print("first")

class B:
    def first(self):
        print("second")

class C(B,A):
    pass

a = C()
a.first()
