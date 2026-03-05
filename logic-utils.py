import random


def generate_secret(low=1, high=100):
    """Generate a random secret number between low and high (inclusive)."""
    return random.randint(low, high)


def calculate_score(current_score, attempts):
    """Reduce the player's score after each wrong guess.

    Intended behavior: subtract 10 points per attempt.
    """
    # BUG: Uses multiplication instead of subtraction.
    #      After a few guesses the score explodes or goes negative in weird ways.
    new_score = current_score * (1 - attempts)
    return new_score


def validate_guess(guess, low=1, high=100):
    """Return True if the guess is within the valid range, False otherwise."""
    # BUG: Uses <= instead of <, so guessing exactly 1 or 100
    #      is incorrectly rejected as out of range.
    if guess <= low or guess >= high:
        return False
    return True
