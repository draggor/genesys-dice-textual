# Genesys Dice
A python utility for rolling the Genesys role playing game system dice.

# Installation
This project uses [uv](https://docs.astral.sh/uv/) as its package manager and runner.  You can also figure it out yourself.

Otherwise, just clone the repo and follow the usages below.

# CLI (non TUI) Usage
```
$ uv run dice.py --help

Usage: dice.py [OPTIONS] DICE

  A dice roller and probablity calculator for the Genesys RPG system

  The dice short codes are:

  BOOST = B SETBACK = S ABILITY = A DIFFICULTY = D PROFICIENCY = P CHALLENGE =
  C PERCENTILE = "%"

  1 Proficiency (yellow) 2 Ability (green) against 2 Difficulty (purple) is:
  PAADD

Options:
  -t      Print all rolls with probabilities
  -s      Print the success rate of a roll
  --help  Show this message and exit.
```
