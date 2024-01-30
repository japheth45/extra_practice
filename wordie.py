#!/usr/bin/env python3
"""Wordie: a command-line helper for five-letter word games.

Commands:
  suggest [GUESS=PATTERN ...]  count the words still possible and suggest the next guess
  score GUESS ANSWER           show the pattern Wordie computes for a guess against an answer
  play                         work through a game one guess at a time
"""

import argparse
import sys
from pathlib import Path

from wordie.candidates import filter_candidates, load_words
from wordie.feedback import WORD_LENGTH, parse_pattern, score_guess
from wordie.ranking import suggest

WORDS_PATH = Path(__file__).resolve().parent / "data" / "words.txt"
BANNER = "Wordie: a helper for five-letter word games."


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
    noun = "candidate remains" if len(words) == 1 else "candidates remain"
    return f"{len(words)} {noun}. Suggested guess: {best}"


def cmd_suggest(args):
    words = load_words(WORDS_PATH)
    pairs = [parse_pair(text) for text in args.pairs]
    print(summary(narrow(words, pairs)))


def cmd_score(args):
    print(score_guess(parse_guess(args.guess), parse_guess(args.answer)))


def cmd_play(args):
    words = load_words(WORDS_PATH)
    print(BANNER)
    print("Type each guess, then the pattern the game showed (G green, Y yellow, B black).")
    print("Press Enter on an empty guess to stop.")
    print()
    guesses = 0
    while True:
        print(summary(words))
        guess_text = input("Guess: ")
        if not guess_text.strip():
            return
        pattern_text = input("Pattern: ")
        try:
            guess = parse_guess(guess_text)
            pattern = parse_pattern(pattern_text)
        except ValueError as error:
            print(error)
            continue
        guesses += 1
        if pattern == "GGGGG":
            print(f"Solved in {guesses} guesses. The answer was {guess.upper()}.")
            return
        words = filter_candidates(words, guess, pattern)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordie", description=BANNER)
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

    score_parser = subparsers.add_parser(
        "score", help="show the pattern Wordie computes for a guess against a known answer"
    )
    score_parser.add_argument("guess")
    score_parser.add_argument("answer")
    score_parser.set_defaults(func=cmd_score)

    play_parser = subparsers.add_parser("play", help="work through a game one guess at a time")
    play_parser.set_defaults(func=cmd_play)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print()
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
