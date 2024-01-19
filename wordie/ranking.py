"""Choosing the next guess from letter statistics over the remaining words."""

from collections import Counter


def letter_frequencies(words):
    """Count how often each letter occurs across all the words."""
    counts = Counter()
    for word in words:
        counts.update(word)
    return counts


def rank(words):
    """Order the words from most to least promising.

    A word's score is the sum of the frequencies of its letters, so words made
    of common letters come first. Ties are broken alphabetically.
    """
    frequencies = letter_frequencies(words)

    def score(word):
        return sum(frequencies[letter] for letter in word)

    return sorted(words, key=lambda word: (-score(word), word))


def suggest(words, n=1):
    """Return the n best next guesses."""
    return rank(words)[:n]
