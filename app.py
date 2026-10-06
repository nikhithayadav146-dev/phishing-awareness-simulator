import streamlit as st
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Phishing Awareness Simulator",
    page_icon="🎣",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🎣 Phishing Awareness Simulator")
st.write(
    "Test your ability to identify phishing messages and learn how to stay safe online."
)

# ---------------- QUESTIONS ----------------
questions = [
    {
        "message": "🚨 URGENT: Your bank account will be blocked today! "
                   "Click here immediately to verify your account.",
        "answer": "Phishing",
        "reason": "The message creates urgency and asks you to click a suspicious link."
    },
    {
        "message": "🎉 Congratulations! You have won ₹50,000. "
                   "Send your OTP to claim your prize now!",
        "answer": "Phishing",
        "reason": "Legitimate organizations never ask you to share your OTP."
    },
    {
        "message": "📦 Your delivery is scheduled for tomorrow between 10 AM and 12 PM.",
        "answer": "Safe",
        "reason": "This message does not request sensitive information or suspicious actions."
    },
    {
        "message": "🔐 Your password has expired. "
                   "Click this unknown link to reset it immediately.",
        "answer": "Phishing",
        "reason": "The unknown link and urgent password request are warning signs."
    },
    {
        "message": "🏫 Your college has announced that tomorrow's class will begin at 9 AM.",
        "answer": "Safe",
        "reason": "This is a normal informational message and does not request sensitive information."
    },
    {
        "message": "💳 Your credit card has been suspended. "
                   "Reply with your card number, CVV and OTP to reactivate it.",
        "answer": "Phishing",
        "reason": "Never share your card details, CVV or OTP through messages."
    },
    {
        "message": "📧 Your teacher has shared the assignment deadline through the official college portal.",
        "answer": "Safe",
        "reason": "The message directs you to an official portal rather than requesting private information."
    },
    {
        "message": "⚠️ You have been selected for a FREE iPhone! "
                   "Pay ₹999 delivery charges to receive it.",
        "answer": "Phishing",
        "reason": "Fake prizes and unexpected payment requests are common phishing tricks."
    },
    {
        "message": "🔔 Your library book is due next Monday. Please return it on time.",
        "answer": "Safe",
        "reason": "This is a normal reminder and does not ask for sensitive information."
    },
    {
        "message": "🚨 Your social media account will be permanently deleted. "
                   "Verify your password using this unknown website.",
        "answer": "Phishing",
        "reason": "Threats, urgency and requests for passwords are common phishing indicators."
    }
]

# ---------------- SESSION STATE ----------------
if "started" not in st.session_state:
    st.session_state.started = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current" not in st.session_state:
    st.session_state.current = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ---------------- START BUTTON ----------------
if not st.session_state.started:

    st.subheader("🛡️ How does it work?")

    st.write("""
    You will see different messages and emails.
    
    Your task is to decide whether each message is:
    
    🔴 **Phishing** – suspicious or dangerous
    
    🟢 **Safe** – appears legitimate
    """)

    if st.button("🚀 Start Simulator", use_container_width=True):

        st.session_state.questions = random.sample(questions, len(questions))
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.last_result = None
        st.session_state.started = True

        st.rerun()


# ---------------- QUIZ ----------------
else:

    total = len(st.session_state.questions)
    current = st.session_state.current

    # Finished
    if current >= total:

        st.success("🎉 Simulation Completed!")

        st.subheader("📊 Your Results")

        score = st.session_state.score
        percentage = (score / total) * 100

        st.metric("Your Score", f"{score}/{total}")
        st.metric("Accuracy", f"{percentage:.0f}%")

        if percentage >= 80:
            st.balloons()
            st.success(
                "🏆 Excellent! You have a strong understanding of phishing attacks."
            )

        elif percentage >= 50:
            st.warning(
                "👍 Good job! You understand some phishing signs, "
                "but there is still room to improve."
            )

        else:
            st.error(
                "⚠️ Be careful! You should learn more about common phishing warning signs."
            )

        st.subheader("🛡️ Remember")

        st.write("""
        • Never share your OTP or password.

        • Check links before clicking them.

        • Be careful with urgent messages.

        • Don't trust unexpected prizes or offers.

        • Verify suspicious messages with the official organization.
        """)

        if st.button("🔄 Restart Simulator", use_container_width=True):
            st.session_state.started = False
            st.session_state.questions = []
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.last_result = None

            st.rerun()

    # Question
    else:

        question = st.session_state.questions[current]

        st.progress((current + 1) / total)

        st.write(f"### Question {current + 1} of {total}")

        st.info(question["message"])

        st.write("### What do you think?")

        col1, col2 = st.columns(2)

        with col1:
            phishing_button = st.button(
                "🔴 Phishing",
                use_container_width=True,
                disabled=st.session_state.answered
            )

        with col2:
            safe_button = st.button(
                "🟢 Safe",
                use_container_width=True,
                disabled=st.session_state.answered
            )

        # Check answer
        if phishing_button or safe_button:

            selected = "Phishing" if phishing_button else "Safe"

            st.session_state.answered = True

            if selected == question["answer"]:
                st.session_state.score += 1
                st.session_state.last_result = "correct"
            else:
                st.session_state.last_result = "wrong"

            st.rerun()

        # Show result
        if st.session_state.answered:

            if st.session_state.last_result == "correct":
                st.success("✅ Correct!")

            else:
                st.error(
                    f"❌ Incorrect! The correct answer is **{question['answer']}**."
                )

            st.write("### 💡 Why?")

            st.write(question["reason"])

            if st.button("➡️ Next Question", use_container_width=True):

                st.session_state.current += 1
                st.session_state.answered = False
                st.session_state.last_result = None

                st.rerun()