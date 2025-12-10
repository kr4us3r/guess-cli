from random import randint
from time import time
from enum import StrEnum
import json

class Difficulty(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

def main():
    print("Welcome to the game of guessing numbers.\n" \
          "I'm pondering a number betwixt 1 and 100 inclusively." \
          "\nThou art to guess it in N tries.\n\n" \
          
          "Select the difficulty thou desirest:\n" \
          "1. Easy (10 tries)\n"
          "2. Medium (5 tries)\n"
          "3. Hard (3 tries)\n"
    )
    secret = randint(1, 100)

    print("Enter thy choice: ", end='')
    while True:
        choice = int(input())
        match choice:
            case 1:
                diff = Difficulty.EASY
                n_tries = 10
            case 2:
                diff = Difficulty.MEDIUM
                n_tries = 5
            case 3:
                diff = Difficulty.HARD
                n_tries = 3
            case _:
                print("Choose from the numbers 1, 2, and 3.")
                continue
        break

    start_time = time()

    tries_left = n_tries
    attempts = 0
    while tries_left > 0:
        guess = int(input("\nEnter thy guess: "))
        if guess < 1 or guess > 100:
            print("The number lieth in the range [1, 100].")
            continue

        attempts += 1
        tries_left -= 1
        if guess > secret:
            print(f"Incorrect. The number is less than {guess}.")
        elif guess < secret:
            print(f"Incorrect. The number is greater than {guess}.")
        elif guess == secret:
            print(f"Correct. Thou guess'd the number in {attempts} attempts.\n" \
                  f"It took thee {time() - start_time:.2f} seconds.")
            handle_best_score(diff, attempts)
            offer_rematch()
    print(f"\nThou fail'd to guess the number in {n_tries} attempts. Too bad!")
    offer_rematch()

def offer_rematch():
    print("\nWishest thou to play another round? [Y/n]: ", end='')
    while True:
        yes_no = input()
        if yes_no in ['y', 'Y', 'yes', 'Yes', 'YES']:
            print('\n')
            main()
        elif yes_no in ['n', 'N', 'no', 'No', 'NO']:
            exit(1)
        else:
            print("\nI understood not thy answer. Try again: ", end='')

def handle_best_score(diff: Difficulty, attempts: int):
    score = {"Easy": 0, "Medium": 0, "Hard": 0}
    try:
        with open("score.json", "r") as file:
            score = json.load(file)
    except:
        with open("score.json", "w") as file:
            json.dump(score, file)

    if attempts < score[diff] or score[diff] == 0:
        score[diff] = attempts

    with open("score.json", "w") as file:
        json.dump(score, file)

main()
