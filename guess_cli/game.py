from random import randint
from time import time
from enum import StrEnum
import json

class Diff(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

MAX_TRIES = {
    Diff.EASY: 10,
    Diff.MEDIUM: 5,
    Diff.HARD: 3
}

def main():
    print("Welcome to the game of guessing numbers.\n" \
          "I'm pondering a number betwixt 1 and 100 inclusively." \
          "\nThou art to guess it in N tries.\n\n" \
          
          "Select the difficulty thou desirest:\n" \
          f"1. Easy ({MAX_TRIES[Diff.EASY]} tries)\n"
          f"2. Medium ({MAX_TRIES[Diff.MEDIUM]} tries)\n"
          f"3. Hard ({MAX_TRIES[Diff.HARD]} tries)\n")
    secret: int = randint(1, 100)

    print("Enter thy choice: ", end='')
    while True:
        choice = input()
        match choice:
            case "1":
                diff = Diff.EASY
            case "2":
                diff = Diff.MEDIUM
            case "3":
                diff = Diff.HARD
            case _:
                print("Choose from the numbers 1, 2, and 3: ", end='')
                continue
        break

    attempts: int = 0
    start_time: float = time()
    while attempts < MAX_TRIES[diff]:
        guess = input("\nEnter thy guess: ")
        if not guess.isdigit():
            print("It ought to be a number.")
            continue

        guess = int(guess)
        if guess < 1 or guess > 100:
            print("The number lieth in the range [1, 100].")
            continue

        attempts += 1
        if guess > secret:
            print(f"Incorrect. The number is less than {guess}.")
        elif guess < secret:
            print(f"Incorrect. The number is greater than {guess}.")
        elif guess == secret:
            print(f"Correct. Thou guess'd the number in {attempts} attempts.\n" \
                  f"It took thee {time() - start_time:.2f} seconds.")
            handle_best_score(diff, attempts)
            offer_rematch()

        if diff == Diff.EASY and attempts == 8:
            give_hint(secret)
        elif diff == Diff.MEDIUM and attempts == 4:
            give_hint(secret)
        elif diff == Diff.HARD and attempts == 2:
            give_hint(secret)

    print(f"\nThou fail'd to guess the number in {MAX_TRIES[diff]} attempts. Too bad!")
    offer_rematch()

def offer_rematch() -> None:
    print("\nWishest thou to play another round? [Y/n]: ", end='')
    while True:
        yes_no: str = input()
        if yes_no.lower() in ["", "y", "yes"]:
            print('\n')
            main()
        elif yes_no.lower() in ["n", "no"]:
            exit(1)
        else:
            print("\nI understood not thy answer. Try again: ", end='')

def handle_best_score(diff: Diff, attempts: int) -> None:
    score: dict[Diff, int] = {Diff.EASY: 0, Diff.MEDIUM: 0, Diff.HARD: 0}
    try:
        with open("score.json", "r") as file:
            score = json.load(file)
    except:
        with open("score.json", "w") as file:
            json.dump(score, file)
    if attempts < score[diff] or score[diff] == 0:
        score[diff] = attempts

    print(f"\nThy best score at {diff} difficulty is {score[diff]} tries.")

    with open("score.json", "w") as file:
        json.dump(score, file)

def give_hint(num: int) -> None:
    shift_left: int = randint(0, 2)
    shift_right: int = 4 - shift_left
    print(f"\nI shall give thee a hint: the number lieth in the range [{num-shift_left}, {num+shift_right}].")

if __name__ == "__main__":
    main()
