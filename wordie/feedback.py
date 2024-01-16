"""Scoring a guess against an answer, and reading the pattern the game shows."""

GREEN = "G"
YELLOW = "Y"
BLACK = "B"
WORD_LENGTH = 5


def score_guess(guess, answer):
    """Return the five-letter pattern for a guess against a known answer.

    A letter in the right place is G. A letter that appears somewhere else in
    the answer is Y. Any other letter is B.
    """
    guess = guess.lower()
    answer = answer.lower()
    if len(guess) != WORD_LENGTH or len(answer) != WORD_LENGTH:
        raise ValueError(f"Both words need exactly {WORD_LENGTH} letters.")
    pattern = []
    for position, letter in enumerate(guess):
        if answer[position] == letter:
            pattern.append(GREEN)
        elif letter in answer:
            pattern.append(YELLOW)
        else:
            pattern.append(BLACK)
    return "".join(pattern)


def parse_pattern(text):
    """Turn what the user typed into a pattern of exactly five G, Y, or B letters."""
    pattern = text.strip().upper()
    if len(pattern) != WORD_LENGTH:
        raise ValueError(f"A pattern needs exactly {WORD_LENGTH} letters, got {text!r}.")
    for letter in pattern:
        if letter not in (GREEN, YELLOW, BLACK):
            raise ValueError(f"Patterns use only the letters G, Y, and B, got {text!r}.")
    return pattern
