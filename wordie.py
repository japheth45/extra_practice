#!/usr/bin/env python3
"""Wordie: a command-line helper for five-letter word games."""

import argparse
import sys
from pathlib import Path

from wordie.candidates import filter_candidates, load_words
from wordie.feedback import WORD_LENGTH, parse_pattern
from wordie.ranking import suggest

WORDS_PATH = Path(__file__).resolve().parent / "data" / "words.txt"


def parse_guess(text):
    """Clean up a typed guess and make sure it is five letters."""
    guess = text.strip().lower()
    if len(guess) != WORD_LENGTH or not guess.isalpha():
        raise ValueError(f"A guess needs exactly {WORD_LENGTH} letters, got {text!r}.")
    return guess


def parse_pair(text):
    """Split 'CRANE=BBYBG' into ('crane', 'BBYBG')."""
    guess, separator, pattern = text.partition("=")
    if not separator:
        raise ValueError(f"Expected GUESS=PATTERN, for example CRANE=BBYBG, got {text!r}.")
    return parse_guess(guess), parse_pattern(pattern)


def narrow(words, pairs):
    """Apply each guess-and-pattern pair in turn."""
    for guess, pattern in pairs:
        words = filter_candidates(words, guess, pattern)
    return words


def summary(words):
    """One line: how many words are still possible and what to guess next."""
    best = suggest(words)[0].upper()
    return f"{len(words)} candidates remain. Suggested guess: {best}"


def cmd_suggest(args):
    words = load_words(WORDS_PATH)
    pairs = [parse_pair(text) for text in args.pairs]
    print(summary(narrow(words, pairs)))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordie", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    suggest_parser = subparsers.add_parser(
        "suggest", help="count the words still possible and suggest the next guess"
    )
    suggest_parser.add_argument(
        "pairs",
        nargs="*",
        metavar="GUESS=PATTERN",
        help="a guess and the pattern the game showed for it, for example CRANE=BBYBG",
    )
    suggest_parser.set_defaults(func=cmd_suggest)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
