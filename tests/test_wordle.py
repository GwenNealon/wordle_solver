"""Tests for wordle_2.py."""

# Module imports
import pytest

# Module imports
import wordle_solver


@pytest.fixture
def solver() -> wordle_solver.solver.WordleSolver:
    """Fixture to create a WordleSolver instance with sample words."""
    with wordle_solver.GUESS_WORDS_FILE.open(encoding="utf-8") as f:
        guess_words = {line.strip() for line in f if line.strip()}
    with wordle_solver.TARGET_WORDS_FILE.open(encoding="utf-8") as f:
        target_words = {line.strip() for line in f if line.strip()}

    solver = wordle_solver.solver.WordleSolver(
        guess_words=guess_words,
        answer_words=target_words,
        hard_mode=False,
    )
    return solver


def test_all_guess_target_combinations(solver: wordle_solver.solver.WordleSolver) -> None:
    """Test that all guess and target combinations are valid."""
    for guess in solver.guess_words:
        for target in solver.answer_words:
            response = solver.get_response(guess, target)
            for index, letter_response in enumerate(response):
                match letter_response:
                    case wordle_solver.solver.GuessResult.CORRECT:
                        assert guess[index] == target[index]
                    case wordle_solver.solver.GuessResult.MISPLACED:
                        assert guess[index] != target[index]
                        assert any(
                            guess[index] == target[j] != guess[j]
                            for j in range(wordle_solver.solver.WORD_LENGTH)
                            if j != index
                        )
                    case wordle_solver.solver.GuessResult.INCORRECT:
                        assert guess[index] != target[index]
                        assert not any(
                            guess[index] == target[j] != guess[j]
                            for j in range(wordle_solver.solver.WORD_LENGTH)
                            if j != index
                        )
                    case _:
                        error_msg = f"Unexpected response letter: {letter_response}"
                        raise ValueError(error_msg)
