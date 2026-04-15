# Command-Line Quiz Game 🎯

A Python quiz game that runs in the terminal. Choose a difficulty, answer multiple choice questions, and see if you can top the leaderboard!

## Features

- Multiple difficulty levels (easy, medium, hard)
- Randomised question and answer order each game
- Timer — your speed counts toward the leaderboard
- Top 5 leaderboard per difficulty, saved between sessions

## How to Run

No external libraries required — just Python 3.

```bash
git clone https://github.com/emsipop/command-line-quiz-game.git
cd command-line-quiz-game
python quiz_game.py
```

## Folder Structure

```
command-line-quiz-game/
│
├── quiz_game.py
│
└── questions/
    ├── easy.json
    ├── medium.json
    └── hard.json
```

Leaderboard files (`score_tracker_*.json`) are created automatically when you first complete a quiz.

## Adding Your Own Questions

Questions are stored as JSON files in the `questions/` folder. Each file represents a difficulty level — the filename becomes the difficulty name shown in the menu.

Each file should be a JSON array of objects in this format:

```json
[
  {
    "question": "What is the capital of France?",
    "options": ["Berlin", "Paris", "Madrid", "Rome"],
    "answer": "Paris"
  }
]
```

Add as many questions as you like — the game picks 5 at random each time.

## Controls

- Enter a number to select an option
- `Ctrl+C` to quit at any time
