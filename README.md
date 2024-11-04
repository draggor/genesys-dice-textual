# Genesys Dice
A python utility for rolling the Genesys role playing game system dice.

# Installation
This project uses [uv](https://docs.astral.sh/uv/) as its package manager and runner.  You can also figure it out yourself.

Otherwise, just clone the repo and follow the usages below.

# Usage
```
$ uv run src/cli.py --help

Usage: dice.py [OPTIONS] [DICE]

  A dice roller and probablity calculator for the Genesys RPG system.
  If run without any arguments, it loads the interactive TUI.

  The dice short codes are:

  BOOST = B
  SETBACK = S
  ABILITY = A
  DIFFICULTY = D
  PROFICIENCY = P
  CHALLENGE = C
  PERCENTILE = T

  1 Proficiency (yellow) 2 Ability (green) against 2 Difficulty (purple) is:
  PAADD

Options:
  -d      Print the details of the roll
  -t      Print all rolls with probabilities
  -s      Print the success rate of a roll
  -f      Print the faces of the dice
  --help  Show this message and exit.
```
