"""
+==================================================+
|       CALCULATOR  --  Python Mini-Project 2     |
+==================================================+

A fully-featured terminal calculator.
Supports basic ops, memory, history & more!
"""

import os
import math


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("""
+==================================================+
|       CALCULATOR  --  Python Mini-Project 2     |
+==================================================+
""")


def print_menu():
    print("  OPERATIONS")
    print("  ----------")
    print("  +    Addition           -    Subtraction")
    print("  *    Multiplication     /    Division")
    print("  %    Modulus            **   Power")
    print("  //   Floor Division     sqrt Square Root")
    print()
    print("  MEMORY")
    print("  ------")
    print("  ms   Memory Store       mr   Memory Recall")
    print("  mc   Memory Clear       m+   Memory Add")
    print()
    print("  OTHER")
    print("  -----")
    print("  h    History            c    Clear screen")
    print("  q    Quit")
    print()


def format_result(n):
    if n == int(n) and abs(n) < 1e15:
        return str(int(n))
    return f"{n:.10g}"


def calculate(op, a, b=None):
    if op == "+":   return a + b
    elif op == "-": return a - b
    elif op == "*": return a * b
    elif op == "/":
        if b == 0: raise ZeroDivisionError("Cannot divide by zero!")
        return a / b
    elif op == "%":
        if b == 0: raise ZeroDivisionError("Cannot modulo by zero!")
        return a % b
    elif op == "**":  return a ** b
    elif op == "//":
        if b == 0: raise ZeroDivisionError("Cannot floor-divide by zero!")
        return a // b
    elif op == "sqrt":
        if a < 0: raise ValueError("Cannot take square root of a negative number!")
        return math.sqrt(a)
    else:
        raise ValueError(f"Unknown operation: {op}")


TWO_OPERAND_OPS = {"+", "-", "*", "/", "%", "**", "//"}
ONE_OPERAND_OPS = {"sqrt"}


def run():
    clear()
    header()
    print_menu()

    history = []
    memory = 0.0
    last_result = None

    while True:
        print("-" * 52)
        status = []
        if memory != 0:
            status.append(f"M: {format_result(memory)}")
        if last_result is not None:
            status.append(f"ANS: {format_result(last_result)}")
        if status:
            print("  [" + "  |  ".join(status) + "]")

        op = input("\n  Enter operation (or h/c/q): ").strip().lower()

        if op == "q":
            print("\n  Goodbye! Keep calculating!\n")
            break

        elif op == "c":
            clear()
            header()
            print_menu()
            continue

        elif op == "h":
            print()
            if not history:
                print("  No history yet.")
            else:
                print("  HISTORY (last 10):")
                for i, entry in enumerate(history[-10:], 1):
                    print(f"  {i:>2}. {entry}")
            print()
            continue

        elif op == "ms":
            if last_result is not None:
                memory = last_result
                print(f"  >> Memory stored: {format_result(memory)}")
            else:
                print("  !! No result to store yet.")
            continue

        elif op == "mr":
            print(f"  >> Memory recall: {format_result(memory)}")
            last_result = memory
            continue

        elif op == "mc":
            memory = 0.0
            print("  >> Memory cleared.")
            continue

        elif op == "m+":
            if last_result is not None:
                memory += last_result
                print(f"  >> Memory updated: {format_result(memory)}")
            else:
                print("  !! No result to add.")
            continue

        elif op in TWO_OPERAND_OPS:
            print()
            raw_a = input("  First number (or 'ans'): ").strip().lower()
            if raw_a == "ans" and last_result is not None:
                a = last_result
                print(f"  Using ANS = {format_result(a)}")
            else:
                try:
                    a = float(raw_a)
                except ValueError:
                    print("  !! Invalid number.\n")
                    continue

            raw_b = input("  Second number (or 'ans'): ").strip().lower()
            if raw_b == "ans" and last_result is not None:
                b = last_result
                print(f"  Using ANS = {format_result(b)}")
            else:
                try:
                    b = float(raw_b)
                except ValueError:
                    print("  !! Invalid number.\n")
                    continue

            try:
                result = calculate(op, a, b)
                entry = f"{format_result(a)} {op} {format_result(b)} = {format_result(result)}"
                print(f"\n  ==>  {entry}")
                history.append(entry)
                last_result = result
            except (ZeroDivisionError, ValueError) as e:
                print(f"\n  !! Error: {e}")

        elif op in ONE_OPERAND_OPS:
            print()
            raw_a = input("  Number (or 'ans'): ").strip().lower()
            if raw_a == "ans" and last_result is not None:
                a = last_result
                print(f"  Using ANS = {format_result(a)}")
            else:
                try:
                    a = float(raw_a)
                except ValueError:
                    print("  !! Invalid number.\n")
                    continue

            try:
                result = calculate(op, a)
                entry = f"{op}({format_result(a)}) = {format_result(result)}"
                print(f"\n  ==>  {entry}")
                history.append(entry)
                last_result = result
            except (ZeroDivisionError, ValueError) as e:
                print(f"\n  !! Error: {e}")

        else:
            print(f"  !! Unknown operation '{op}'. Type 'h' for help.")


if __name__ == "__main__":
    run()