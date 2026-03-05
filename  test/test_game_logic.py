import pytest
from logic_utils import generate_secret, calculate_score, validate_guess


# ─── generate_secret tests ───

def test_secret_in_range():
    """The secret number should always be between 1 and 100."""
    for _ in range(50):
        secret = generate_secret()
        assert 1 <= secret <= 100


# ─── calculate_score tests ───

def test_score_decreases_after_guess():
    """Score should go DOWN (not explode) after each wrong guess."""
    score = calculate_score(100, 1)
    assert 0 <= score < 100, f"Expected score between 0 and 100, got {score}"


def test_score_never_negative():
    """Score should never drop below zero."""
    score = 100
    for attempt in range(1, 11):
        score = calculate_score(score, attempt)
    assert score >= 0, f"Score should not be negative, got {score}"


# ─── validate_guess tests ───

def test_valid_guess_in_range():
    """A guess within 1–100 should be valid."""
    assert validate_guess(50) is True


def test_boundary_low():
    """Guessing exactly 1 should be valid."""
    assert validate_guess(1) is True


def test_boundary_high():
    """Guessing exactly 100 should be valid."""
    assert validate_guess(100) is True


def test_out_of_range_low():
    """A guess below 1 should be invalid."""
    assert validate_guess(0) is False


def test_out_of_range_high():
    """A guess above 100 should be invalid."""
    assert validate_guess(101) is False
