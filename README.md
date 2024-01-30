# Wordie

Wordie is a small command-line helper for Wordle-style five-letter word games. You tell it what you guessed and what the game showed, and it tells you which words are still possible and which one to try next. I wrote it to beat the rest of the team in our daily game chat. Now that everyone has a copy, nobody can call it cheating.

## Running it

Wordie needs Python 3 and nothing else.

    python wordie.py suggest
    python wordie.py suggest SLATE=BBGBG
    python wordie.py suggest SLATE=BBGBG CRANE=BGGBG

With no arguments, `suggest` ranks the whole list and proposes an opening word. Each `GUESS=PATTERN` pair narrows the list down. Suggestions come from letter frequencies over the words that are still possible: words made of the most common remaining letters rank first.

    python wordie.py score SLATE CRANE

`score` prints the pattern Wordie would compute for a guess against a known answer (here `BBGBG`), which is handy for checking the tool after a game.

    python wordie.py play

`play` walks through a game one guess at a time: type the guess, type the pattern, and Wordie shows how many words are still possible and what to try next. Press Enter on an empty guess to stop.

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
