"""Wordle solver package."""

# Standard library imports
import pathlib

# Module imports
from . import solver

DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
GUESS_WORDS_FILE = DATA_DIR.joinpath("allowed.txt")
TARGET_WORDS_FILE = DATA_DIR.joinpath("answers.txt")

__all__ = [
    "solver",
]
