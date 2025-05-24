"""Methods to find the most efficient wordle guesses"""

from __future__ import annotations

# Standard library imports
import functools
import logging
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Set as AbstractSet

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GuessResult(Enum):
    """Enum to represent the result of a guess in Wordle."""

    INCORRECT = auto()
    """The letter is not in the word."""

    MISPLACED = auto()
    """The letter is in the word but in the wrong position."""

    CORRECT = auto()
    """The letter is in the word and in the correct position."""


Response = tuple[GuessResult, GuessResult, GuessResult, GuessResult, GuessResult]
"""Tuple to represent the response of a guess in Wordle, with each letter's result."""

Guesss = tuple[str, Response]
"""Tuple to represent a guess in Wordle, with the guessed word and its response."""

WORD_LENGTH = 5


class WordleSolver:
    """Class to find the most efficient wordle guesses."""

    guess_words: AbstractSet[str]
    """Set of words that can be used as guesses."""

    answer_words: AbstractSet[str]
    """Set of words that can be used as answers."""

    hard_mode: bool
    """Hard mode flag. In hard mode, you may only guess words that may be correct."""

    def __init__(
        self,
        guess_words: Iterable[str],
        answer_words: Iterable[str],
        *,
        hard_mode: bool = False,
    ) -> None:
        """
        Initialize the WordleSolver with a list of guess words and answer words.

        Args:
            guess_words (Iterable[str]): A list of words to use as guesses.
            answer_words (Iterable[str]): A list of words to use as answers.
            hard_mode (bool): If True, the solver will use hard mode rules. In hard mode, you may only guess words that
                may be correct.
        """

        # Save parameters
        self.answer_words = frozenset(answer_words)
        # Ensure that answer words are valid guesses
        self.guess_words = frozenset(guess_words).union(self.answer_words)
        self.hard_mode = hard_mode

        # Validate inputs
        for guess in guess_words:
            self.validate_guess(guess)
        for answer in answer_words:
            self.validate_answer(answer)
            if answer not in self.guess_words:
                error_msg = f"Answer word must be in the guess words: {answer=}"
                raise ValueError(error_msg)

    ### Validation methods ###

    def validate_word(self, word: str) -> None:
        """Check if a word is valid."""
        if len(word) != WORD_LENGTH:
            error_msg = f"Invalid Word length: {word=}"
            raise ValueError(error_msg)
        if not word.isalpha():
            error_msg = f"Word must contain only alphabetic characters: {word=}"
            raise ValueError(error_msg)

    def validate_guess(self, guess: str, valid_answers: AbstractSet[str] | None = None) -> None:
        """Check if a guess is valid."""
        self.validate_word(guess)
        if guess not in self.guess_words:
            error_msg = f"Guess not in valid words: {guess=}"
            raise ValueError(error_msg)
        if self.hard_mode and valid_answers is not None and guess not in valid_answers:
            error_msg = f"Hard mode guess not in valid answers: {guess=}"
            raise ValueError(error_msg)

    def validate_answer(self, target: str) -> None:
        """Check if a target word is valid."""
        self.validate_word(target)
        if target not in self.answer_words:
            error_msg = f"Target not in valid words: {target=}"
            raise ValueError(error_msg)

    ### Guessing methods ###

    @functools.cache  # noqa: B019
    def get_response(self, guess: str, target: str) -> Response:
        """Get the response for a guess against a target word."""
        self.validate_guess(guess)
        self.validate_answer(target)
        return (
            self._get_response_by_letter(guess, target, 0),
            self._get_response_by_letter(guess, target, 1),
            self._get_response_by_letter(guess, target, 2),
            self._get_response_by_letter(guess, target, 3),
            self._get_response_by_letter(guess, target, 4),
        )

    def _get_response_by_letter(self, guess: str, target: str, index: int) -> GuessResult:
        """Get the response for a single letter in a guess against a target word."""
        # Check if the letter is correct
        if guess[index] == target[index]:
            return GuessResult.CORRECT
        # Check if the letter is not in the word
        if guess[index] not in target:
            return GuessResult.INCORRECT
        # If the letter is in the word, but not in the correct position, and a guess in a correct position is not
        # correct, then it is misplaced
        if any(guess[index] == target[j] != guess[j] for j in range(WORD_LENGTH)):
            return GuessResult.MISPLACED
        # Otherwise, the letter is incorrect
        return GuessResult.INCORRECT
