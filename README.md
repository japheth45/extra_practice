# Wordie

Wordie is a small command-line helper for Wordle-style five-letter word games. You tell it what you guessed and what the game showed, and it tells you which words are still possible. I wrote it to beat the rest of the team in our daily game chat. Now that everyone has a copy, nobody can call it cheating.

## The pattern letters

After each guess the game colors the five letters. Wordie reads that as five letters typed on the keyboard:

- `G` for a green square: the letter is in the right place.
- `Y` for a yellow square: the letter is in the answer but somewhere else.
- `B` for a black (or gray) square: the letter is not in the answer.

So if you guessed CRANE and the game showed black, black, yellow, black, green, the pattern is `BBYBG`. Wordie reads letters rather than the colored squares because the squares don't paste reliably into a terminal.

## The word list

`data/words.txt` holds the 8,636 five-letter words from the ENABLE word list (Enhanced North American Benchmark Lexicon), which is in the public domain. The game's own answer list is not included.

## License

MIT. See `LICENSE`.
