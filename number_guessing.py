import random

guesses  =0
lower_range=1
higher_range=10
number = random.randint(lower_range, higher_range)

isRunning = True

while isRunning:
    guess = input(f"Enter your number between {lower_range} and {higher_range} : ")

    if guess.isdigit():
        guess = int(guess)
        guesses += 1

        if guess < lower_range or guess > higher_range:
            print(f"This is out of range , guess in between {lower_range} and {higher_range}")
            continue

        if guess < number:
            print("too low")

            continue
        elif guess > number:
            print("too high")
            continue
        else:
            print("that's correct")
            print(f'number of guesses {guesses}')
            isRunning = False

    else:
        guesses += 1
        print(f"This is out of range , guess in between {lower_range} and {higher_range}")
        continue
