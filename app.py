import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from openai import OpenAI


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Physics AI Lab",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Physics AI Lab")
st.caption("Experiment. Observe. Understand. Test yourself.")


# --------------------------------------------------
# OPENAI
# --------------------------------------------------

def get_ai_response(question, mass, force, friction, acceleration):

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
You are an expert but beginner-friendly physics tutor.

The student is performing a Newton's Second Law experiment.

Experiment data:
Mass = {mass} kg
Applied Force = {force} N
Friction = {friction} N
Net Force = {force - friction} N
Acceleration = {acceleration:.2f} m/s²

Student question:
{question}

Explain the answer clearly and briefly.
Use the experiment data when useful.
Do not perform unnecessary calculations.
Help the student understand the physics concept.
"""

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI Tutor error: {e}"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🔬 Choose Experiment")

experiment = st.sidebar.selectbox(
    "Physics Experiment",
    [
        "Newton's Second Law",
        "Projectile Motion"
    ]
)


# ==================================================
# NEWTON'S SECOND LAW
# ==================================================

if experiment == "Newton's Second Law":

    st.header("Newton's Second Law")
    st.write(
        "Investigate how force and mass affect acceleration."
    )

    st.latex(r"F = ma")

    # ----------------------------------------------
    # CONTROLS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        mass = st.slider(
            "Mass (kg)",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.5
        )

    with col2:
        force = st.slider(
            "Applied Force (N)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0
        )

    with col3:
        friction = st.slider(
            "Friction (N)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=1.0
        )

    # ----------------------------------------------
    # CALCULATIONS
    # ----------------------------------------------

    net_force = force - friction
    acceleration = net_force / mass

    # ----------------------------------------------
    # RESULTS
    # ----------------------------------------------

    st.subheader("📊 Results")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Mass", f"{mass:.1f} kg")

    with c2:
        st.metric("Net Force", f"{net_force:.1f} N")

    with c3:
        st.metric("Acceleration", f"{acceleration:.2f} m/s²")

    # ----------------------------------------------
    # VISUAL EXPERIMENT
    # ----------------------------------------------

    st.subheader("🚀 Run the Experiment")

    time = st.slider(
        "Experiment Time (seconds)",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    position = 0.5 * acceleration * time**2

    # Object gets visually larger with mass
    object_size = 0.5 + mass * 0.04

    fig, ax = plt.subplots(figsize=(10, 3))

    ax.set_xlim(-1, max(10, position + 3))
    ax.set_ylim(-1.5, 1.5)

    ax.set_xlabel("Position (m)")
    ax.set_yticks([])

    # Ground
    ax.axhline(
        y=-object_size / 2,
        linewidth=2
    )

    # Object
    rectangle = plt.Rectangle(
        (position, -object_size / 2),
        object_size,
        object_size
    )

    ax.add_patch(rectangle)

    ax.set_title(
        f"Object position: {position:.2f} m | "
        f"Acceleration: {acceleration:.2f} m/s²"
    )

    st.pyplot(fig)

    st.info(
        f"At {time:.1f} seconds, the object has moved "
        f"approximately {position:.2f} meters."
    )

    # ----------------------------------------------
    # OBSERVATION
    # ----------------------------------------------

    st.subheader("🔎 What did you observe?")

    if force > friction:
        st.write(
            f"With a net force of **{net_force:.1f} N**, "
            f"the object accelerates at **{acceleration:.2f} m/s²**."
        )

    elif force == friction:
        st.write(
            "The applied force and friction are balanced, "
            "so the net force is zero."
        )

    else:
        st.write(
            "Friction is greater than the applied force, "
            "so the net force acts in the opposite direction."
        )

    # ----------------------------------------------
    # AI TUTOR
    # ----------------------------------------------

    st.divider()

    st.subheader("🤖 Ask the AI Physics Tutor")

    question = st.text_input(
        "Ask something about this experiment:",
        placeholder="Why does increasing mass decrease acceleration?"
    )

    if st.button("Ask GPT"):

        if question.strip():

            with st.spinner("GPT is thinking..."):

                answer = get_ai_response(
                    question,
                    mass,
                    force,
                    friction,
                    acceleration
                )

            st.success(answer)

        else:
            st.warning("Please enter a question.")

    # ----------------------------------------------
    # MCQ TEST
    # ----------------------------------------------

    st.divider()

    st.header("🧠 Test Your Understanding")

    st.write(
        "Answer these questions based on the experiment."
    )

    q1 = st.radio(
        "1. According to Newton's Second Law, what happens "
        "to acceleration when force increases while mass stays constant?",
        [
            "Acceleration decreases",
            "Acceleration increases",
            "Acceleration stays the same",
            "Acceleration becomes zero"
        ],
        key="q1"
    )

    q2 = st.radio(
        "2. If the same force is applied to a heavier object, "
        "what happens to its acceleration?",
        [
            "It increases",
            "It stays the same",
            "It decreases",
            "It becomes infinite"
        ],
        key="q2"
    )

    q3 = st.radio(
        "3. What is the correct formula for Newton's Second Law?",
        [
            "F = m / a",
            "F = ma",
            "F = m + a",
            "F = a / m"
        ],
        key="q3"
    )

    q4 = st.radio(
        "4. If applied force and friction are equal, "
        "what is the net force?",
        [
            "The net force is zero",
            "The net force is equal to the mass",
            "The net force doubles",
            "The net force becomes negative"
        ],
        key="q4"
    )

    q5 = st.radio(
        "5. If mass = 5 kg and net force = 20 N, "
        "what is the acceleration?",
        [
            "2 m/s²",
            "4 m/s²",
            "10 m/s²",
            "25 m/s²"
        ],
        key="q5"
    )

    if st.button("🎯 Submit Test"):

        score = 0

        if q1 == "Acceleration increases":
            score += 1

        if q2 == "It decreases":
            score += 1

        if q3 == "F = ma":
            score += 1

        if q4 == "The net force is zero":
            score += 1

        if q5 == "4 m/s²":
            score += 1

        st.subheader(f"🏆 Your Score: {score}/5")

        if score == 5:
            st.success(
                "Excellent! You understand Newton's Second Law very well. 🎉"
            )

        elif score >= 3:
            st.info(
                "Good job! You understand the main idea, "
                "but review the concepts you missed."
            )

        else:
            st.warning(
                "Keep practicing! Try changing the mass and force "
                "in the experiment and observe what happens."
            )


# ==================================================
# PROJECTILE MOTION
# ==================================================

elif experiment == "Projectile Motion":

    st.header("🏹 Projectile Motion")

    st.write(
        "Explore how launch velocity and angle affect projectile motion."
    )

    velocity = st.slider(
        "Initial Velocity (m/s)",
        5.0,
        50.0,
        20.0,
        1.0
    )

    angle = st.slider(
        "Launch Angle (degrees)",
        0.0,
        90.0,
        45.0,
        1.0
    )

    gravity = 9.81

    angle_rad = np.radians(angle)

    vx = velocity * np.cos(angle_rad)
    vy = velocity * np.sin(angle_rad)

    t_flight = 2 * vy / gravity

    t = np.linspace(0, max(t_flight, 0.01), 200)

    x = vx * t
    y = vy * t - 0.5 * gravity * t**2

    y = np.maximum(y, 0)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(x, y)

    ax.set_title("Projectile Trajectory")
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.grid(True)

    st.pyplot(fig)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Maximum Height",
            f"{(vy**2)/(2*gravity):.2f} m"
        )

    with c2:
        st.metric(
            "Flight Time",
            f"{t_flight:.2f} s"
        )

    with c3:
        st.metric(
            "Range",
            f"{(velocity**2*np.sin(2*angle_rad))/gravity:.2f} m"
        )

    st.info(
        "Change the angle and velocity to observe how the trajectory changes."
    )
