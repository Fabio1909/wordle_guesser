# Wordle Solver and Console Game

This project implements a Wordle game that can be played manually in the terminal or solved automatically using a guesser algorithm. It includes three core components:

- **wordle.py** which handles the game logic
- **guesser.py** which selects guesses either manually or programmatically
- **game.py** which runs full game sessions and optional multiple automated rounds

---

## Features

- Play Wordle directly in your terminal
- Run automatic solving over multiple rounds
- View statistics such as success rate, average guesses, and runtime
- Easily switch between manual and automatic modes

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

⸻

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

.
├── game.py        Main script that runs manual or automated games
├── wordle.py      Wordle game engine
└── guesser.py     Logic for manual or automatic guessing


