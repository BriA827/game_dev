#imports
import math
import random

# functions

#Activity 1
def temp_convert():
    f_temp = input("Enter temperature in Fahrenheit: ")
    c_temp = round((float(f_temp) -32) * (5/9), 1)
    print(f"The temperature in Celsius is: {c_temp}")
    return c_temp

def trape_area():
    height = input("Enter the height of the trapezoid: ")
    bb = input("Enter the length of the bottom base: ")
    tb = input("Enter the length of the top base: ")
    t_area = .5 * (float(bb) + float(tb)) * float(height)
    print(f"The area is: {t_area}")
    return t_area

def card_tester():
    c_num = input("Enter your card number: ")
    c_list = []
    for n in c_num:
        c_list.append(int(n))

    even_odd = 0

    for n in c_list:
        if even_odd%2 == 0:
            a = n *2
            c_list[even_odd] = a
        even_odd += 1

    i = 0
    for n in c_list:
        if len(str(n)) > 1:
            two_digits = []
            for a in str(n):
                two_digits.append(int(a))
            c_list[i] = sum(two_digits)
        i += 1

    final = sum(c_list)

    if final%10 == 0:
        print("This is a real card number.")
    else:
        print("This is a fake card number")


#Activity 2
def quiz():
    print('\nWelcome to the Ultimate Scaramouche Quiz!!\n')
    ques = {0:"What is Scaramouche's rank in the Fatui Harbingers (number)?", 
           1:"Who is Scaramouche's mother?\n1. Raiden Shogun\n2. Ei/Beelzebul\n3. Makoto\n4. No one, he doesn't deserve a mother", 
           2:"What was the name of the second person to betray Scaramouche?", 
           3:"What does Scaramouche steal from his mother?\n1. The throne\n2. His Anemo Vision\n3. Her Gnosis\n4. Nothing, he loves her",
           4:"Correctly spell Scaramouche's boss title."}
    ans = {0:"6", 1:"2", 2:"Niwa", 3:"3", 4:"The Everlasting Lord of Arcane Wisdom, Shouki no Kami, the Prodigal"}
   
    correct = 0
    question = 0

    for n in range(0,len(ques)):
        print(ques[question])
        user_answer = input("")
        if user_answer == ans[question]:
            print("Correct!\n")
            correct+= 1
        else:
            print("Incorrect :(\n")
        question += 1
    
    score = round((correct/len(ques)) * 100, 2)

    if score >= 80:
        print(f"\nCongratulations, you passed with {correct} questions right!\nThat's a score of {score} percent!")
    else: 
        print(f"\nYou FAILED. You got {correct} questions right.\nThat's a score of {score} percent.")


#Activity 3
def name_print(name, count):
    for n in range(0, count):
        print(name)
    print('Done')

def red_gold(count):
    for n in range(0, count):
        print("Red")
        print("Gold")

def even_nums(limit):
    for n in range(2, limit+2, 2):
        print(n)

def even_nums_while(limit):
    counter = 2
    while counter <= limit:
        print(counter)
        counter += 2

def count_down(count):
    counter = count
    while counter >= 0:
        print(counter)
        counter -= 1

    print("Blast off!")

def seven_nums(numbers):
    print(f"The sum of the {len(numbers)} numbers is: {sum(numbers)}")

    positive = 0
    negative = 0
    zeros = 0

    for n in numbers:
        if n > 0:
            positive +=1
        elif n < 0:
            negative += 1
        else:
            zeros += 1
    
    print(f"There are {positive} positive numbers, {negative} negative numbers, and {zeros} zeros!")

def coin_toss(count):
    heads = 0
    tails = 0
    for n in range(0, count):
        coin = random.randint(0,1)
        if coin == 1:
            heads += 1
        else:
            tails +=1
    print(f"In {count} tosses, there were {heads} heads and {tails} tails")

#code

#Activity 1
# conversion = temp_convert()
# trapezoid = trape_area()
# card_tester()

#Activity 2
# quiz()

#Activity 3
# name_print('Bri', 10)
# red_gold(20)
# even_nums(100)
# even_nums_while(100)
# count_down(10)

# print(random.randint(0,10))
##im sorry i took the easy way for these two but i did make everything else a function and i knwo that you know that i know how to make a variable and print
# print(round(random.uniform(1,10), 1))

# seven_nums([-1,2,3,0,0,6,-7])
coin_toss(50)