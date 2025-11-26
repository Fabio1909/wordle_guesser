# Wordle Guesser (Entropy Based Solver)

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Repo](https://img.shields.io/badge/GitHub-Fabio1909%2Fwordle_guesser-black)](https://github.com/Fabio1909/wordle_guesser)

A Wordle console game plus an automatic solver that chooses guesses using entropy (expected information gain). This was built for a university NLP course module on entropy and evaluation, with the goal of performing well on a new, previously unseen word list.

## Why entropy?

Given a candidate set of possible answers, each guess produces a feedback pattern (greens, yellows, grays). A good guess splits the remaining candidates into many evenly sized groups. Entropy is a natural way to score that, because higher entropy means higher expected information and faster elimination of impossible words.

## Project structure

* `wordle.py` handles core Wordle rules and feedback.
* `guesser.py` selects the next guess, either manually or via the entropy strategy.
* `game.py` runs interactive games and can run many automated rounds for evaluation.
* `wordlist.yaml` contains test wordlist to calculate accuracy and speed metrics
* `wordlist_dev.yaml` contains a smaller list for development.
---

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---
## Manual Mode

Start the game without arguments. You will enter guesses yourself.

```bash
python game.py
```

This launches an interactive Wordle session in the terminal.

---
## Automatic Mode

Run the game with the --r flag followed by the number of rounds you want to simulate. The automatic solver will play Wordle repeatedly and print statistics at the end.

Example:

```bash
python game.py --r 10000
```

This runs 10000 rounds automatically and prints:
- Percent of words solved 
- Average number of guesses for successful games
- Total runtime in minutes and seconds


```bash
You correctly guessed 98.46000000000001% of words.
Average number of guesses:  3.747511679869998
Runtime: 0 minutes : 22.13 seconds
```

