import random
from time import time
from enum import StrEnum
import json

class Difficulty(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

MAX_TRIES = {
    Difficulty.EASY: 10,
    Difficulty.MEDIUM: 5,
    Difficulty.HARD: 3
}

HINT_THRESHOLD = {
    Difficulty.EASY: 8,
    Difficulty.MEDIUM: 4,
    Difficulty.HARD: 2
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
          f"1. Easy ({MAX_TRIES[Difficulty.EASY]} guesses, for the gentle novice)\n"
          f"2. Medium ({MAX_TRIES[Difficulty.MEDIUM]} guesses, for the steadfast heart)\n"
          f"3. Hard ({MAX_TRIES[Difficulty.HARD]} guesses, for the bold and valiant soul)\n")
    secret: int = random.randint(1, 100)

    print("Speak thy choice, fair guesser: ", end='')
    while True:
        choice = input()
        match choice:
            case "1":
                diff = Difficulty.EASY
            case "2":
                diff = Difficulty.MEDIUM
            case "3":
                diff = Difficulty.HARD
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

        if attempts == HINT_THRESHOLD[diff]:
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

def handle_best_score(diff: Difficulty, attempts: int) -> None:
    try:
        with open("score.json", "r") as file:
            score = json.load(file)
    except FileNotFoundError:
        score: dict[Difficulty, int] = {Difficulty.EASY: 0,
                                        Difficulty.MEDIUM: 0,
                                        Difficulty.HARD: 0}
    except json.JSONDecodeError:
        print("Alack! Thy scroll of triumphs is foully writ - its letters twisted by some scribbler's spite!")
        return
    except Exception:
        print("Fie on't! Some Puckish sprite hath bedevil'd the fetch - thy deeds elude the light!")
        return

    if attempts < score[diff] or score[diff] == 0:
        print(f"\nA new laurel crowns thy brow! Thou hast surpassed all former feats "
              f"at {diff} difficulty with mere {attempts} guesses.")
        score[diff] = attempts
    else:
        print(f"\nThy noblest deed remaineth {score[diff]} guesses upon {diff} ground. "
              "This time thou hast matched valor, though not eclipsed it.")

    try:
        with open("score.json", "w") as file:
            json.dump(score, file)
    except Exception:
        print("O cruel stars! Thy laurels cannot be graven - fortune denies the quill its ink!")

def give_hint(guess: int, secret: int) -> None:
    if secret == 42:
        print("\nIn Belmont's caskets, mercy droppeth as the gentle rain,"
              "yet some deeper jest - born of stars and wandering knights - mocks "
              "the seeker with a sum that answers all and nothing.")
    elif guess == secret - 13:
        print("Nay, 'tis close, but hie thee higher by a baker's dozen.")
    else:
        left: int = random.randint(0, 2)
        right: int = 4 - left
        print("\nI shall lend thee aid: the number lieth in the "
              f"narrower strait [{secret-left}, {secret+right}].")

if __name__ == "__main__":
    main()
