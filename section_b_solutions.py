"""
Section B — Python Programming: Reference Solutions
====================================================
Five short, self-contained programs matching Q6–Q10 of the assignment.
Run directly:  python section_b_solutions.py
"""


# ---------------------------------------------------------------------------
# Q6 — Variables & Data Types: swap two variables without a third variable
# ---------------------------------------------------------------------------
def swap_variables():
    a, b = 5, 10
    print(f"Before swap: a = {a}, b = {b}")
    a, b = b, a
    print(f"After swap:  a = {a}, b = {b}")


# ---------------------------------------------------------------------------
# Q7 — Loops: print all even numbers between 1 and 50
# ---------------------------------------------------------------------------
def print_even_numbers():
    evens = [n for n in range(1, 51) if n % 2 == 0]
    print("Even numbers between 1 and 50:")
    print(evens)


# ---------------------------------------------------------------------------
# Q8 — Functions: check whether a number is prime
# ---------------------------------------------------------------------------
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def demo_is_prime():
    for num in [1, 2, 17, 20, 29]:
        print(f"is_prime({num}) -> {is_prime(num)}")


# ---------------------------------------------------------------------------
# Q9 — Lists & Dictionaries: word frequency counter
# ---------------------------------------------------------------------------
def word_frequency(sentence: str) -> dict:
    words = sentence.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def demo_word_frequency():
    sentence = "the cat sat on the mat"
    print(f"Input: {sentence!r}")
    print(f"Output: {word_frequency(sentence)}")


# ---------------------------------------------------------------------------
# Q10 — String Manipulation: palindrome check (ignore case & spaces)
# ---------------------------------------------------------------------------
def is_palindrome(text: str) -> bool:
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def demo_is_palindrome():
    for text in ["Nurses Run", "Hello World", "A man a plan a canal Panama"]:
        print(f"is_palindrome({text!r}) -> {is_palindrome(text)}")


if __name__ == "__main__":
    print("=" * 60)
    print("Q6 — Swap two variables")
    print("=" * 60)
    swap_variables()

    print("\n" + "=" * 60)
    print("Q7 — Even numbers between 1 and 50")
    print("=" * 60)
    print_even_numbers()

    print("\n" + "=" * 60)
    print("Q8 — Prime number check")
    print("=" * 60)
    demo_is_prime()

    print("\n" + "=" * 60)
    print("Q9 — Word frequency counter")
    print("=" * 60)
    demo_word_frequency()

    print("\n" + "=" * 60)
    print("Q10 — Palindrome check")
    print("=" * 60)
    demo_is_palindrome()
