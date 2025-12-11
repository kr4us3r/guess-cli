import random
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

PROMPTS = [
    "\nVent thy conjecture: ",
    "\nWhat number dare thee name? ",
    "\nSpeak thy guess boldly: ",
    "\nHurl thy shaft at the mark: "
]

def main():
    print("Hail, good wanderer! Welcome to this merry trial of wit.\n"
          "I have conceivèd in my mind a secret number betwixt one and a full hundred."
          "\nThou shalt divine it with but few guesses, ere fortune turn her wheel against thee.\n\n"
          
          "Now choose thy path upon this stage of chance:\n"
          f"1. Easy ({MAX_TRIES[Diff.EASY]} guesses, for the gentle novice)\n"
          f"2. Medium ({MAX_TRIES[Diff.MEDIUM]} guesses, for the steadfast heart)\n"
          f"3. Hard ({MAX_TRIES[Diff.HARD]} guesses, for the bold and valiant soul)\n")
    secret: int = random.randint(1, 100)

    print("Speak thy choice, fair guesser: ", end='')
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
                print("Nay, good friend, thy choice must be 1, 2, or 3: ", end='')
                continue
        break

    attempts: int = 0
    start_time: float = time()
    while attempts < MAX_TRIES[diff]:
        guess = input(random.choice(PROMPTS))
        if not guess.isdigit():
            print("Nay, that is no number! Speak digits alone, I beseech thee.")
            continue

        guess = int(guess)
        if guess < 1 or guess > 100:
            print("My secret dwelleth betwixt one and a hundred - no more, no less.")
            continue

        attempts += 1
        if guess > secret:
            print(f"Alas, too high! My number lieth lower than {guess}, in humbler fields.")
        elif guess < secret:
            print(f"Too low, good soul! It dwelleth higher than {guess}, upon loftier ground.")
        elif guess == secret:
            total = time() - start_time
            print(f"Triumph! Thou hast divined my secret in but {attempts} ventures!\n" \
                  f"Thy wit hath conquered in {total:.2f} fleeting seconds of mortal time.")
            handle_best_score(diff, attempts)
            offer_rematch()

        if diff == Diff.EASY and attempts == 8 or \
           diff == Diff.MEDIUM and attempts == 4 or \
           diff == Diff.HARD and attempts == 2:
            give_hint(guess, secret)

    print(f"\nAlack and well-a-day! Thy {MAX_TRIES[diff]} guesses "
          "are spent and the secret yet eludes thee.\n"
          f"The number was {secret}. Fortune hath frowned this time - but courage, try again!")
    offer_rematch()

def offer_rematch() -> None:
    print("\nShall we tread this stage once more? "
          "Wilt thou hazard fortune again? [Y/n]: ", end='')
    while True:
        yes_no: str = input()
        if yes_no.lower() in ["", "y", "yes", "yea"]:
            print('\nBrave heart! The wheel turns anew...\n')
            main()
        elif yes_no.lower() in ["n", "no", "nay"]:
            print("\nFare thee well, noble guesser. Till next we meet upon the boards!")
            exit(1)
        else:
            print("\nI pray thee, speak plainer - yea or nay? ", end='')

def handle_best_score(diff: Diff, attempts: int) -> None:
    score: dict[Diff, int] = {Diff.EASY: 0, Diff.MEDIUM: 0, Diff.HARD: 0}
    try:
        with open("score.json", "r") as file:
            score = json.load(file)
    except:
        with open("score.json", "w") as file:
            json.dump(score, file)
    if attempts < score[diff] or score[diff] == 0:
        print(f"\nA new laurel crowns thy brow! Thou hast surpassed all former feats "
              f"at {diff} difficulty with mere {attempts} guesses!")
        score[diff] = attempts
    else:
        print(f"\nThy noblest deed remaineth {score[diff]} guesses upon {diff} ground. "
              "This time thou hast matched valor, though not eclipsed it.")

    with open("score.json", "w") as file:
        json.dump(score, file)

def give_hint(guess: int, secret: int) -> None:
    if secret == 42:
        print("\nIn Belmont’s caskets, mercy droppeth as the gentle rain,"
              "yet some deeper jest—born of stars and wandering knights—mocks"
              "the seeker with a sum that answers all and nothing.")
    elif guess == secret + 13:
        print("Nay, 'tis close, but hie thee higher by a baker's dozen.")
    else:
        left: int = random.randint(0, 2)
        right: int = 4 - left
        print("\nI shall lend thee aid: the number lieth in the "
              f"narrower strait [{secret-left}, {secret+right}].")

if __name__ == "__main__":
    main()
