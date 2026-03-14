"""
╔══════════════════════════════════════════════╗
║        🎲  SNAKE & LADDERS  🎲               ║
║         Python Mini-Project #1               ║
╚══════════════════════════════════════════════╝

A classic 2-player Snake & Ladders game.
Roll the dice, climb ladders, avoid snakes!
"""

import random
import time
import os


# ── Board configuration ──────────────────────────────────────────────────────

SNAKES = {
    99: 7,
    95: 75,
    92: 88,
    89: 68,
    74: 53,
    64: 60,
    62: 19,
    49: 11,
    46: 25,
    16: 6,
}

LADDERS = {
    2:  38,
    7:  14,
    8:  31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
}

BOARD_SIZE = 100


# ── Helpers ───────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def roll_dice():
    return random.randint(1, 6)


def dice_face(n):
    faces = {
        1: ["+---------+", "|         |", "|    *    |", "|         |", "+---------+"],
        2: ["+-------- +", "|  *      |", "|         |", "|      *  |", "+---------+"],
        3: ["+---------+", "|  *      |", "|    *    |", "|      *  |", "+---------+"],
        4: ["+---------+", "|  *   *  |", "|         |", "|  *   *  |", "+---------+"],
        5: ["+---------+", "|  *   *  |", "|    *    |", "|  *   *  |", "+---------+"],
        6: ["+---------+", "|  *   *  |", "|  *   *  |", "|  *   *  |", "+---------+"],
    }
    return faces[n]


def print_dice(n):
    print()
    for row in dice_face(n):
        print(f"    {row}")
    print()


def draw_board(positions):
    """Draw a 10x10 board with player positions marked."""
    print()
    print("  +" + "-----+" * 10)

    for row in range(9, -1, -1):
        if row % 2 == 0:
            cells = range(row * 10 + 1, row * 10 + 11)
        else:
            cells = range(row * 10 + 10, row * 10, -1)

        row_str = "  |"
        for cell in cells:
            markers = ""
            if positions.get("P1") == cell:
                markers += "1"
            if positions.get("P2") == cell:
                markers += "2"
            if cell in SNAKES and not markers:
                tag = " S  "
            elif cell in LADDERS and not markers:
                tag = " L  "
            elif markers:
                tag = f"[{markers}] " if len(markers) == 1 else f"[{markers}]"
                tag = tag[:4].center(4)
            else:
                tag = f"{cell:^4}"
            row_str += tag + "|"
        print(row_str)
        print("  +" + "-----+" * 10)

    print()
    print("  LEGEND: [1]=Player1  [2]=Player2  S=Snake  L=Ladder")
    print()


# ── Game logic ────────────────────────────────────────────────────────────────

def move_player(name, pos, roll):
    new_pos = pos + roll
    print(f"\n  >> {name} rolled a {roll}!")
    time.sleep(0.4)

    if new_pos > BOARD_SIZE:
        print(f"  !! Needs exact roll to reach 100. Stay at {pos}.")
        return pos

    if new_pos == BOARD_SIZE:
        return new_pos

    if new_pos in SNAKES:
        tail = SNAKES[new_pos]
        print(f"  SNAKE at {new_pos}! Slide down to {tail}. Hisssss!")
        time.sleep(0.6)
        new_pos = tail

    elif new_pos in LADDERS:
        top = LADDERS[new_pos]
        print(f"  LADDER at {new_pos}! Climb up to {top}. Woohoo!")
        time.sleep(0.6)
        new_pos = top

    else:
        print(f"  --> {name} moves to square {new_pos}.")

    return new_pos


def header():
    print("""
+==================================================+
|     SNAKE & LADDERS  --  Python Mini-Project 1  |
+==================================================+
""")


def get_player_names():
    print("  Enter player names (press Enter for defaults):\n")
    p1 = input("  Player 1 name [Alice]: ").strip() or "Alice"
    p2 = input("  Player 2 name [Bob]  : ").strip() or "Bob"
    return p1, p2


def play_again():
    ans = input("\n  Play again? (y/n): ").strip().lower()
    return ans == "y"


# ── Main game loop ────────────────────────────────────────────────────────────

def game():
    clear()
    header()
    p1_name, p2_name = get_player_names()

    players = {p1_name: 0, p2_name: 0}
    turn_order = [p1_name, p2_name]
    markers = {p1_name: "P1", p2_name: "P2"}
    turn = 0

    while True:
        name = turn_order[turn % 2]
        pos  = players[name]

        clear()
        header()

        board_positions = {markers[n]: players[n] for n in players}
        draw_board(board_positions)

        print(f"  Positions  ->  {p1_name}: {players[p1_name]}  |  {p2_name}: {players[p2_name]}")
        print(f"\n  -- {name}'s turn (currently on square {pos}) --")

        input("\n  Press Enter to roll the dice...")

        roll = roll_dice()
        print_dice(roll)
        time.sleep(0.3)

        players[name] = move_player(name, pos, roll)

        if players[name] == BOARD_SIZE:
            clear()
            header()
            board_positions = {markers[n]: players[n] for n in players}
            draw_board(board_positions)
            print(f"\n  *** {name} reached square 100 and WINS! Congratulations! ***\n")
            break

        turn += 1
        time.sleep(1.0)

    if play_again():
        game()
    else:
        print("\n  Thanks for playing Snake & Ladders! Goodbye!\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    game()