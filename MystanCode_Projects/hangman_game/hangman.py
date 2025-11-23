"""
File: hangman.py
Name:
-----------------------------
This program plays hangman game.
Users see a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    There are 7 chances to guess incorrectly before losing the game.
    The game ends when the user guesses the word or runs out of chances.
    """

    answer = random_word()
    dashed = ''
    for ch in answer:
        dashed += '-'
    left = N_TURNS

    while dashed != answer:
        if left > 0:
            print('The word looks like: ' + dashed)
            print('You have ' + str(left) + ' wrong guesses left')
            guess = input('Your guess: ')
            guess = guess.upper()

            #illegal
            if len(guess)!=1:
                print('illegal format')
            elif not guess.isalpha():
                print('illegal format')
            else:
                if guess in answer:
                    print('You are correct!')
                    new_dashed=''
                    i=0
                    for ch in answer:
                        if ch == guess:
                            new_dashed += guess
                        else:
                            new_dashed += dashed[i]
                    i += 1
                    dashed = new_dashed
    if dashed == answer:
        print('You win!!')
        print('The word was:' + answer)
    else:
        print('You are completely hung :(')
        print('The word was: ' + answer)












def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == '__main__':
    main()
