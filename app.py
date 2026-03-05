import streamlit as st
import random
from logic_utils import generate_secret, calculate_score

# ─── Page Config ───
st.set_page_config(page_title="🔢 Number Guessing Game", page_icon="🎯")
st.title("🎯 Number Guessing Game")
st.markdown("Guess the secret number between **1 and 100**. You have **10 attempts**!")

# ─── Session State Initialization ───
if "secret" not in st.session_state:
    st.session_state.secret = generate_secret()
    st.session_state.attempts = 0
    st.session_state.max_attempts = 10
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.score = 100

# ─── Helper: Check the player's guess ───
# BUG 1: The hints are reversed — "Too high" when guess is low, and vice versa.
def check_guess(guess, secret):
    """Compare the guess to the secret and return a hint string."""
    if guess < secret:
        return "📈 Too high! Try a lower number."
    elif guess > secret:
        return "📉 Too low! Try a higher number."
    else:
        return "🎉 Correct!"


# ─── Helper: Parse raw input into an integer ───
# BUG 2: This function doesn't handle non-integer input gracefully.
#         Entering a decimal like 50.5 or text like "abc" will crash the game.
def parse_guess(raw_input):
    """Convert raw input string to an integer guess."""
    return int(raw_input)


# ─── Game UI ───
if not st.session_state.game_over:
    with st.form("guess_form"):
        raw = st.text_input("Enter your guess (1–100):", key="guess_input")
        submitted = st.form_submit_button("Submit Guess")

    if submitted and raw:
        try:
            guess = parse_guess(raw)
        except ValueError:
            st.error("⚠️ Please enter a valid whole number.")
            st.stop()

        # BUG 3: Attempts counter never increments, so the game never ends.
        #         The line below is commented out by mistake.
        # st.session_state.attempts += 1

        result = check_guess(guess, st.session_state.secret)
        st.session_state.history.append((guess, result))

        # BUG 4: Score deduction uses the wrong operator — it multiplies
        #         instead of subtracting, so the score goes haywire.
        st.session_state.score = calculate_score(
            st.session_state.score, st.session_state.attempts
        )

        if guess == st.session_state.secret:
            st.session_state.game_over = True
            st.success(f"🎉 You guessed it! The number was **{st.session_state.secret}**.")
            st.balloons()
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.game_over = True
            st.error(
                f"💀 Game Over! You've used all {st.session_state.max_attempts} attempts. "
                f"The number was **{st.session_state.secret}**."
            )
        else:
            st.info(result)

# ─── Sidebar: Game Stats ───
st.sidebar.header("📊 Game Stats")
st.sidebar.metric("Attempts Used", st.session_state.attempts)
st.sidebar.metric("Score", st.session_state.score)

if st.session_state.history:
    st.sidebar.subheader("📝 Guess History")
    for i, (g, r) in enumerate(st.session_state.history, 1):
        st.sidebar.write(f"**#{i}:** Guessed `{g}` → {r}")

# ─── Reset Button ───
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
