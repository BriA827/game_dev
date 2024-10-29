import math

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
        self.d = None
        self.xs = None

    def value(self,x):
        v = (self.a * (x**2)) + (self.b * x) + self.c
        self.x_values.append(x)
        self.y_values.append(v)
        return v
    
    def discrim(self):
        num = ((self.b)**2 - (4*self.a*self.c))
        # >0, 2    =0, 1    <0, 0
        self.d = num
        return num
    
    def x_inter(self):
        if self.d < 0:
            return "No real solutions"
        pos = (-1*self.b + math.sqrt(self.d)) / (2*self.a)
        neg = (-1*self.b - math.sqrt(self.d)) / (2*self.a)
        self.xs = [pos,neg]
        return pos, neg
    
    def vertex(self):
        y = (self.a * (self.d)**2) + (self.b * self.d) + self.c
        return y
    
quad = Quadratic(1,0,-4)
print(quad.value(5))
print(quad.discrim())
print(quad.x_inter())
print(quad.vertex())