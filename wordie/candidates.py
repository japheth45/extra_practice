"""Loading the word list and narrowing it down from the game's feedback."""

from wordie.feedback import score_guess


def load_words(path):
    """Read one word per line, lowercased, skipping blank lines."""
    words = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            word = line.strip().lower()
            if word:
                words.append(word)
    return words


def filter_candidates(words, guess, pattern):
    """Keep the words that would have produced this pattern for this guess.

    A word is still possible if scoring the guess against it gives exactly the
    pattern the game showed.
    """
    guess = guess.lower()
    return [word for word in words if score_guess(guess, word) == pattern]
