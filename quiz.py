"""
+==================================================+
|        QUIZ GAME  --  Python Mini-Project 3     |
+==================================================+

A multiple-choice quiz game with categories,
scoring, timer, and a high score leaderboard!
"""

import os
import time
import random


# ── Question Bank ─────────────────────────────────────────────────────────────

QUESTIONS = {
    "Science": [
        {
            "q": "What is the chemical symbol for Gold?",
            "options": ["A) Gd", "B) Go", "C) Au", "D) Ag"],
            "answer": "C",
            "fact": "Au comes from the Latin word 'Aurum'."
        },
        {
            "q": "How many bones are in the adult human body?",
            "options": ["A) 196", "B) 206", "C) 216", "D) 226"],
            "answer": "B",
            "fact": "Babies are born with ~270 bones; many fuse as we grow."
        },
        {
            "q": "What planet is known as the Red Planet?",
            "options": ["A) Venus", "B) Jupiter", "C) Mars", "D) Saturn"],
            "answer": "C",
            "fact": "Mars looks red due to iron oxide (rust) on its surface."
        },
        {
            "q": "What is the speed of light (approx)?",
            "options": ["A) 300,000 km/s", "B) 150,000 km/s", "C) 500,000 km/s", "D) 1,000,000 km/s"],
            "answer": "A",
            "fact": "Light travels 299,792,458 metres per second."
        },
        {
            "q": "What gas do plants absorb from the atmosphere?",
            "options": ["A) Oxygen", "B) Nitrogen", "C) Carbon Dioxide", "D) Hydrogen"],
            "answer": "C",
            "fact": "Plants use CO2 + water + sunlight to make glucose via photosynthesis."
        },
    ],
    "History": [
        {
            "q": "In what year did World War II end?",
            "options": ["A) 1943", "B) 1944", "C) 1945", "D) 1946"],
            "answer": "C",
            "fact": "WWII ended in Europe on May 8 and in the Pacific on Sep 2, 1945."
        },
        {
            "q": "Who was the first President of the United States?",
            "options": ["A) John Adams", "B) Thomas Jefferson", "C) Benjamin Franklin", "D) George Washington"],
            "answer": "D",
            "fact": "Washington served two terms from 1789 to 1797."
        },
        {
            "q": "Which ancient wonder was located in Alexandria?",
            "options": ["A) The Colossus", "B) The Lighthouse", "C) The Hanging Gardens", "D) The Mausoleum"],
            "answer": "B",
            "fact": "The Lighthouse of Alexandria stood ~137 metres tall."
        },
        {
            "q": "The Berlin Wall fell in which year?",
            "options": ["A) 1987", "B) 1988", "C) 1989", "D) 1990"],
            "answer": "C",
            "fact": "The wall fell on November 9, 1989, ending the Cold War division."
        },
        {
            "q": "Who painted the Mona Lisa?",
            "options": ["A) Michelangelo", "B) Raphael", "C) Leonardo da Vinci", "D) Donatello"],
            "answer": "C",
            "fact": "Da Vinci painted it between 1503 and 1519. It hangs in the Louvre."
        },
    ],
    "Technology": [
        {
            "q": "What does 'HTTP' stand for?",
            "options": ["A) HyperText Transfer Protocol", "B) High Transfer Text Program", "C) Hyper Transfer Text Process", "D) HyperText Transmission Port"],
            "answer": "A",
            "fact": "HTTP is the foundation of data communication on the World Wide Web."
        },
        {
            "q": "Who co-founded Apple Inc.?",
            "options": ["A) Bill Gates", "B) Steve Jobs", "C) Elon Musk", "D) Jeff Bezos"],
            "answer": "B",
            "fact": "Steve Jobs, Steve Wozniak & Ronald Wayne founded Apple in 1976."
        },
        {
            "q": "What does 'CPU' stand for?",
            "options": ["A) Core Processing Unit", "B) Central Program Utility", "C) Central Processing Unit", "D) Computer Power Unit"],
            "answer": "C",
            "fact": "The CPU is the brain of a computer, executing program instructions."
        },
        {
            "q": "Which language is primarily used for web styling?",
            "options": ["A) HTML", "B) JavaScript", "C) Python", "D) CSS"],
            "answer": "D",
            "fact": "CSS (Cascading Style Sheets) controls layout, colour and fonts."
        },
        {
            "q": "What year was Python first released?",
            "options": ["A) 1985", "B) 1989", "C) 1991", "D) 1995"],
            "answer": "C",
            "fact": "Guido van Rossum released Python 0.9.0 in February 1991."
        },
    ],
    "Mixed": [],  # Filled dynamically
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("""
+==================================================+
|        QUIZ GAME  --  Python Mini-Project 3     |
+==================================================+
""")


def progress_bar(current, total, width=30):
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {current}/{total}"


def stars(score, total):
    pct = score / total if total else 0
    if pct == 1.0:   return "★★★★★  PERFECT!"
    elif pct >= 0.8: return "★★★★☆  Excellent!"
    elif pct >= 0.6: return "★★★☆☆  Good job!"
    elif pct >= 0.4: return "★★☆☆☆  Keep trying!"
    else:            return "★☆☆☆☆  Study more!"


# ── High scores (in-memory) ───────────────────────────────────────────────────

high_scores = []   # list of (name, score, total, category, time_secs)

def save_score(name, score, total, category, elapsed):
    high_scores.append((name, score, total, category, elapsed))
    high_scores.sort(key=lambda x: (-x[1], x[4]))  # sort by score desc, time asc

def show_leaderboard():
    print("\n  LEADERBOARD (top 10)")
    print("  " + "-" * 54)
    print(f"  {'#':<4} {'Name':<15} {'Score':<10} {'Category':<14} {'Time'}")
    print("  " + "-" * 54)
    if not high_scores:
        print("  No scores yet!")
    for i, (n, s, t, cat, sec) in enumerate(high_scores[:10], 1):
        print(f"  {i:<4} {n:<15} {s}/{t:<8} {cat:<14} {sec:.1f}s")
    print()


# ── Quiz engine ───────────────────────────────────────────────────────────────

def pick_category():
    categories = ["Science", "History", "Technology", "Mixed"]
    print("  Choose a category:\n")
    for i, cat in enumerate(categories, 1):
        print(f"    {i}. {cat}")
    print()
    while True:
        choice = input("  Enter number (1-4): ").strip()
        if choice in {"1", "2", "3", "4"}:
            return categories[int(choice) - 1]
        print("  !! Please enter 1, 2, 3, or 4.")


def pick_difficulty():
    print("\n  Choose difficulty:\n")
    print("    1. Easy   (5 questions, no timer)")
    print("    2. Medium (8 questions, 20s per question)")
    print("    3. Hard   (10 questions, 12s per question)")
    print()
    while True:
        choice = input("  Enter number (1-3): ").strip()
        if choice == "1": return 5,  None
        if choice == "2": return 8,  20
        if choice == "3": return 10, 12
        print("  !! Please enter 1, 2, or 3.")


def timed_input(prompt, seconds):
    """Simple timed input — falls back to untimed if not supported."""
    import sys, select
    print(prompt, end="", flush=True)
    start = time.time()
    if os.name == "nt":
        # Windows: no select on stdin, just regular input
        ans = input().strip().upper()
        elapsed = time.time() - start
        return ans, elapsed
    else:
        ready, _, _ = select.select([sys.stdin], [], [], seconds)
        elapsed = time.time() - start
        if ready:
            ans = sys.stdin.readline().strip().upper()
            return ans, elapsed
        else:
            print("\n  !! Time's up!")
            return None, seconds


def run_quiz(player_name, questions, time_limit):
    score = 0
    total = len(questions)
    start_time = time.time()
    wrong_answers = []

    for i, q in enumerate(questions, 1):
        clear()
        header()
        print(f"  Player: {player_name}   Score: {score}/{i-1}")
        print(f"  Progress: {progress_bar(i-1, total)}")
        if time_limit:
            print(f"  Time limit per question: {time_limit}s")
        print()
        print(f"  Q{i}: {q['q']}")
        print()
        for opt in q["options"]:
            print(f"    {opt}")
        print()

        if time_limit:
            prompt = f"  Your answer (A/B/C/D) [{time_limit}s]: "
            answer, q_time = timed_input(prompt, time_limit)
        else:
            answer = input("  Your answer (A/B/C/D): ").strip().upper()
            q_time = 0

        correct = q["answer"]

        if answer is None:
            print(f"  !! No answer in time. Correct answer was: {correct}")
            wrong_answers.append(q)
        elif answer == correct:
            print(f"  CORRECT! {q['fact']}")
            score += 1
        else:
            print(f"  WRONG. Correct answer: {correct}. {q['fact']}")
            wrong_answers.append(q)

        time.sleep(1.8)

    total_time = time.time() - start_time
    return score, total, total_time, wrong_answers


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    clear()
    header()

    print("  Welcome to the Quiz Game!\n")
    player_name = input("  Enter your name: ").strip() or "Player"

    while True:
        clear()
        header()
        print(f"  Hello, {player_name}!\n")
        print("  1. Start Quiz")
        print("  2. View Leaderboard")
        print("  3. Change Name")
        print("  4. Quit")
        print()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            clear()
            header()
            category = pick_category()
            num_questions, time_limit = pick_difficulty()

            # Build question pool
            if category == "Mixed":
                pool = []
                for cat in ["Science", "History", "Technology"]:
                    pool.extend(QUESTIONS[cat])
            else:
                pool = QUESTIONS[category][:]

            random.shuffle(pool)
            selected = pool[:num_questions]

            input(f"\n  Ready? {num_questions} questions, category: {category}. Press Enter...")

            score, total, elapsed, wrong = run_quiz(player_name, selected, time_limit)
            save_score(player_name, score, total, category, elapsed)

            clear()
            header()
            print(f"\n  Quiz Over, {player_name}!\n")
            print(f"  Final Score:  {score} / {total}")
            print(f"  Time Taken:   {elapsed:.1f} seconds")
            print(f"  Rating:       {stars(score, total)}")

            if wrong:
                print(f"\n  You got {len(wrong)} question(s) wrong:")
                for w in wrong:
                    print(f"    - {w['q']}")
                    print(f"      Answer: {w['answer']}  |  {w['fact']}")

            print()
            input("  Press Enter to return to menu...")

        elif choice == "2":
            clear()
            header()
            show_leaderboard()
            input("  Press Enter to go back...")

        elif choice == "3":
            player_name = input("\n  Enter new name: ").strip() or player_name
            print(f"  Name updated to: {player_name}")
            time.sleep(1)

        elif choice == "4":
            print(f"\n  Thanks for playing, {player_name}! Goodbye!\n")
            break
        else:
            print("  !! Invalid choice.")
            time.sleep(0.8)


if __name__ == "__main__":
    main()