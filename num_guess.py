"""
+==================================================+
|   GUESS THE NUMBER  --  Python Mini-Project 4   |
+==================================================+

Guess the secret number! Choose your difficulty,
use hints wisely, and beat the leaderboard!
"""

import random
import os
import time


# ── Difficulty settings ───────────────────────────────────────────────────────

DIFFICULTIES = {
    "1": {"name": "Easy",   "range": (1, 50),   "attempts": 10, "hints": 3},
    "2": {"name": "Medium", "range": (1, 100),  "attempts": 7,  "hints": 2},
    "3": {"name": "Hard",   "range": (1, 200),  "attempts": 5,  "hints": 1},
    "4": {"name": "Expert", "range": (1, 1000), "attempts": 8,  "hints": 1},
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("""
+==================================================+
|   GUESS THE NUMBER  --  Python Mini-Project 4   |
+==================================================+
""")


def attempts_bar(used, total):
    remaining = total - used
    filled  = "O" * remaining
    empty   = "X" * used
    return f"[{filled}{empty}]  {remaining}/{total} left"


def score_calc(attempts_used, max_attempts, num_range, hints_used):
    """Higher score for fewer attempts, wider range, fewer hints."""
    base     = 1000
    range_bonus  = (num_range[1] - num_range[0]) // 10
    attempt_pen  = attempts_used * 80
    hint_pen     = hints_used * 150
    return max(0, base + range_bonus - attempt_pen - hint_pen)


def get_hint(number, low, high, hint_num):
    hints = []

    # Hint 1 — odd or even
    hints.append(f"The number is {'EVEN' if number % 2 == 0 else 'ODD'}.")

    # Hint 2 — divisibility
    for d in [3, 5, 7, 11]:
        if number % d == 0:
            hints.append(f"The number is divisible by {d}.")
            break
    else:
        hints.append("The number is not divisible by 3, 5, 7, or 11.")

    # Hint 3 — narrow the range
    quarter = (high - low) // 4
    if number <= low + quarter:
        hints.append(f"The number is in the LOWER quarter ({low}–{low+quarter}).")
    elif number <= low + 2 * quarter:
        hints.append(f"The number is in the SECOND quarter ({low+quarter+1}–{low+2*quarter}).")
    elif number <= low + 3 * quarter:
        hints.append(f"The number is in the THIRD quarter ({low+2*quarter+1}–{low+3*quarter}).")
    else:
        hints.append(f"The number is in the UPPER quarter ({low+3*quarter+1}–{high}).")

    return hints[hint_num % len(hints)]


# ── Leaderboard ───────────────────────────────────────────────────────────────

leaderboard = []   # (name, score, difficulty, attempts_used, number)

def add_score(name, score, diff_name, attempts, number):
    leaderboard.append((name, score, diff_name, attempts, number))
    leaderboard.sort(key=lambda x: -x[1])


def show_leaderboard():
    print("  LEADERBOARD (top 10)")
    print("  " + "-" * 56)
    print(f"  {'#':<4} {'Name':<14} {'Score':<8} {'Difficulty':<10} {'Attempts':<10} {'Number'}")
    print("  " + "-" * 56)
    if not leaderboard:
        print("  No scores yet — be the first!")
    for i, (n, s, d, a, num) in enumerate(leaderboard[:10], 1):
        print(f"  {i:<4} {n:<14} {s:<8} {d:<10} {a:<10} {num}")
    print()


# ── Game logic ────────────────────────────────────────────────────────────────

def play_round(player, difficulty):
    cfg         = DIFFICULTIES[difficulty]
    low, high   = cfg["range"]
    max_attempts = cfg["attempts"]
    max_hints    = cfg["hints"]
    diff_name    = cfg["name"]

    number      = random.randint(low, high)
    attempts    = 0
    hints_used  = 0
    history     = []

    clear()
    header()
    print(f"  Difficulty : {diff_name}")
    print(f"  Range      : {low} – {high}")
    print(f"  Attempts   : {max_attempts}")
    print(f"  Hints      : {max_hints}")
    print(f"\n  I'm thinking of a number between {low} and {high}.")
    print(f"  You have {max_attempts} attempts. Good luck, {player}!\n")
    time.sleep(0.5)

    while attempts < max_attempts:
        print(f"  Attempts : {attempts_bar(attempts, max_attempts)}")
        if history:
            print(f"  Guesses  : {', '.join(str(g) for g in history)}")
        print()

        raw = input(f"  Guess ({low}-{high}) or 'h' for hint, 'q' to quit: ").strip().lower()
        print()

        if raw == "q":
            print(f"  You quit. The number was {number}.")
            return None

        if raw == "h":
            if hints_used < max_hints:
                hint = get_hint(number, low, high, hints_used)
                print(f"  HINT {hints_used+1}: {hint}\n")
                hints_used += 1
            else:
                print(f"  No hints remaining!\n")
            continue

        try:
            guess = int(raw)
        except ValueError:
            print("  !! Please enter a whole number.\n")
            continue

        if guess < low or guess > high:
            print(f"  !! Out of range. Enter a number between {low} and {high}.\n")
            continue

        history.append(guess)
        attempts += 1

        if guess == number:
            final_score = score_calc(attempts, max_attempts, cfg["range"], hints_used)
            clear()
            header()
            print(f"  *** CORRECT! The number was {number}. ***\n")
            print(f"  Solved in  : {attempts} attempt(s)")
            print(f"  Hints used : {hints_used}")
            print(f"  Score      : {final_score} points")

            if attempts == 1:
                print("\n  WOW — first try! Incredible!")
            elif attempts <= max_attempts // 2:
                print("\n  Great job — very efficient!")
            else:
                print("\n  Made it! Close call!")

            add_score(player, final_score, diff_name, attempts, number)
            return final_score

        elif guess < number:
            gap = number - guess
            if gap <= 5:
                print(f"  >>> Too LOW — but very close! (within 5)\n")
            elif gap <= 20:
                print(f"  >> Too LOW — getting warmer.\n")
            else:
                print(f"  > Too LOW — think higher.\n")
        else:
            gap = guess - number
            if gap <= 5:
                print(f"  >>> Too HIGH — but very close! (within 5)\n")
            elif gap <= 20:
                print(f"  >> Too HIGH — getting warmer.\n")
            else:
                print(f"  > Too HIGH — think lower.\n")

    # Out of attempts
    print(f"\n  Out of attempts! The number was {number}. Better luck next time!\n")
    return 0


# ── Main menu ─────────────────────────────────────────────────────────────────

def main():
    clear()
    header()
    print("  Welcome to Guess the Number!\n")
    player = input("  Enter your name: ").strip() or "Player"

    while True:
        clear()
        header()
        print(f"  Hello, {player}!\n")
        print("  1. Play")
        print("  2. Leaderboard")
        print("  3. Change Name")
        print("  4. Quit")
        print()
        choice = input("  Choose: ").strip()

        if choice == "1":
            clear()
            header()
            print("  Choose difficulty:\n")
            for k, v in DIFFICULTIES.items():
                lo, hi = v["range"]
                print(f"    {k}. {v['name']:<8}  Range: {lo}-{hi:<5}  "
                      f"Attempts: {v['attempts']}  Hints: {v['hints']}")
            print()
            diff = input("  Enter number (1-4): ").strip()
            if diff not in DIFFICULTIES:
                print("  !! Invalid choice.")
                time.sleep(0.8)
                continue

            result = play_round(player, diff)
            print()
            input("  Press Enter to return to menu...")

        elif choice == "2":
            clear()
            header()
            show_leaderboard()
            input("  Press Enter to go back...")

        elif choice == "3":
            player = input("\n  Enter new name: ").strip() or player
            print(f"  Name set to: {player}")
            time.sleep(0.8)

        elif choice == "4":
            print(f"\n  Thanks for playing, {player}! Goodbye!\n")
            break
        else:
            print("  !! Invalid option.")
            time.sleep(0.8)


if __name__ == "__main__":
    main()