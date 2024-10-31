import math
import matplotlib.pyplot as plt

# class Dog:
#     def __init__(self, name, age, breed) -> None:
#         self.name = name
#         self.age = age
#         self.breed = breed
    
#     def desc(self):
#         return f"{self.name} is a {self.age}-year-old {self.breed}."
    
#     def speak(self, sound):
#         return f"{self.name} says, \"{sound}\""

# my_dog = Dog("Ollie", 17, "Corgi")
# your_dog = Dog("Oliver", 17, "Terrier")

# print(my_dog.speak("bark bark bark"))

class Quadratic:
    def __init__(self, a, b ,c) -> None:
        self.a = a
        self.b = b
        self.c = c

        self.x_values = []
        self.y_values = []
        self.d = self.discrim()
        self.xs = self.x_inter()
        self.v = self.vertex()

    def value(self,x):
        v = (self.a * (x**2)) + (self.b * x) + self.c
        self.x_values.append(x)
        self.y_values.append(v)
        return v
    
    def discrim(self):
        num = ((self.b)**2 - (4*self.a*self.c))
        # >0, 2    =0, 1    <0, 0
        return num
    
    def x_inter(self):
        self.discrim()
        if self.d < 0:
            return "No real solutions"
        pos = (-1*self.b + math.sqrt(self.d)) / (2*self.a)
        neg = (-1*self.b - math.sqrt(self.d)) / (2*self.a)
        return pos, neg
    
    def vertex(self):
        x = (-1*self.b)/(2* self.a)
        y = self.a *(x**2) + self.b * x + self.c
        return x ,y
    
    def graph(self):
        self.vertex()
        plt.title(f"f(X) = {self.a}X^2 + {self.b}X + {self.c}")
        plt.xlabel("X")
        plt.ylabel("f(X)")
        plt.plot([f for f in range(self.v[0]-10, self.v[0]+10)], [self.value(f) for f in range(self.v[0]-10, self.v[0]+10)])
        plt.show()
    
quad = Quadratic(1,0,-4)
# print(quad.value(5))
# print(quad.discrim())
# print(quad.x_inter())
# print(quad.vertex())
quad.graph()