import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from openai import OpenAI


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Physics AI Lab",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Physics AI Lab")
st.caption(
    "Ask a physics question. Understand the concept. "
    "Run the experiment. Test yourself."
)


# =========================================================
# OPENAI
# =========================================================

def ask_gpt(question):

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    prompt = f"""
You are Physics AI Lab, an interactive physics tutor.

The student asked:

{question}

Identify the main physics concept.

Return EXACTLY in this structure:

TOPIC:
(one of: pendulum, projectile, free_fall, newton, waves)

SHORT_CONCEPT:
Give a simple explanation in 2-4 sentences.

IMPORTANT_CONCEPTS:
Give 4-5 important concepts as a comma-separated list.

EXPERIMENT:
Explain in one sentence what the student will observe.

MCQ:
Write one conceptual multiple-choice question.

A:
option

B:
option

C:
option

D:
option

ANSWER:
A/B/C/D

EXPLANATION:
Explain why the answer is correct in 1-2 sentences.

Keep it beginner-friendly.
Do not use unnecessary mathematics.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


# =========================================================
# PARSE GPT RESPONSE
# =========================================================

def parse_response(text):

    sections = {}

    current = None

    for line in text.splitlines():

        line = line.strip()

        if line.endswith(":"):

            current = line[:-1].upper()
            sections[current] = ""

        elif current:

            sections[current] += line + "\n"

    return sections


# =========================================================
# PENDULUM
# =========================================================

def pendulum_experiment(length, gravity, damping):

    theta0 = np.radians(25)

    t = np.linspace(0, 10, 400)

    omega = np.sqrt(gravity / length)

    theta = (
        theta0
        * np.exp(-damping * t)
        * np.cos(omega * t)
    )

    x = length * np.sin(theta)
    y = -length * np.cos(theta)

    return t, x, y, theta


# =========================================================
# PROJECTILE
# =========================================================

def projectile_experiment(velocity, angle, gravity):

    angle = np.radians(angle)

    vx = velocity * np.cos(angle)
    vy = velocity * np.sin(angle)

    flight_time = 2 * vy / gravity

    t = np.linspace(
        0,
        max(flight_time, 0.01),
        200
    )

    x = vx * t
    y = vy * t - 0.5 * gravity * t**2

    y = np.maximum(y, 0)

    return x, y


# =========================================================
# FREE FALL
# =========================================================

def free_fall_experiment(height, gravity):

    t_max = np.sqrt(2 * height / gravity)

    t = np.linspace(0, t_max, 200)

    y = height - 0.5 * gravity * t**2

    return t, y


# =========================================================
# NEWTON
# =========================================================

def newton_experiment(mass, force, friction):

    net_force = force - friction

    acceleration = net_force / mass

    return net_force, acceleration


# =========================================================
# WAVES
# =========================================================

def wave_experiment(amplitude, frequency):

    x = np.linspace(0, 10, 500)

    wave = amplitude * np.sin(
        2 * np.pi * frequency * x
    )

    return x, wave


# =========================================================
# ASK PHYSICS
# =========================================================

st.header("🔬 Ask Physics AI")

question = st.text_input(
    "What do you want to understand?",
    placeholder="Example: Why does a pendulum slow down?"
)

if st.button("🚀 Explore Physics"):

    if question.strip():

        with st.spinner("Physics AI is thinking..."):

            answer = ask_gpt(question)

        st.session_state["answer"] = answer

    else:

        st.warning("Ask a physics question first.")


# =========================================================
# SHOW AI RESPONSE
# =========================================================

if "answer" in st.session_state:

    sections = parse_response(
        st.session_state["answer"]
    )

    topic = sections.get(
        "TOPIC",
        "pendulum"
    ).strip().lower()

    st.divider()

    st.header("💡 Short Concept")

    st.write(
        sections.get(
            "SHORT_CONCEPT",
            ""
        )
    )

    st.header("📌 Important Concepts")

    concepts = sections.get(
        "IMPORTANT_CONCEPTS",
        ""
    )

    for concept in concepts.split(","):

        if concept.strip():

            st.markdown(
                f"- **{concept.strip()}**"
            )

    st.header("🔬 Interactive Experiment")

    st.write(
        sections.get(
            "EXPERIMENT",
            ""
        )
    )


    # =====================================================
    # PENDULUM
    # =====================================================

    if "pendulum" in topic:

        st.subheader("🕰️ Pendulum Lab")

        col1, col2, col3 = st.columns(3)

        with col1:

            length = st.slider(
                "Length (m)",
                0.5,
                5.0,
                2.0,
                0.1
            )

        with col2:

            gravity = st.slider(
                "Gravity (m/s²)",
                1.0,
                20.0,
                9.81,
                0.1
            )

        with col3:

            damping = st.slider(
                "Air resistance / damping",
                0.0,
                0.5,
                0.05,
                0.01
            )

        t, x, y, theta = pendulum_experiment(
            length,
            gravity,
            damping
        )

        frame = st.slider(
            "▶ Run Pendulum",
            0,
            len(t) - 1,
            0
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.set_xlim(
            -length - 0.5,
            length + 0.5
        )

        ax.set_ylim(
            -length - 0.5,
            0.5
        )

        ax.plot(
            [0, x[frame]],
            [0, y[frame]]
        )

        ax.scatter(
            [x[frame]],
            [y[frame]],
            s=400
        )

        ax.scatter(
            [0],
            [0],
            s=100
        )

        ax.set_aspect("equal")

        ax.set_title(
            "Interactive Pendulum"
        )

        ax.axis("off")

        st.pyplot(fig)

        period = 2 * np.pi * np.sqrt(
            length / gravity
        )

        st.metric(
            "Approximate Period",
            f"{period:.2f} seconds"
        )


    # =====================================================
    # PROJECTILE
    # =====================================================

    elif "projectile" in topic:

        st.subheader("🏹 Projectile Lab")

        velocity = st.slider(
            "Initial velocity (m/s)",
            5.0,
            50.0,
            20.0
        )

        angle = st.slider(
            "Launch angle",
            0.0,
            90.0,
            45.0
        )

        gravity = st.slider(
            "Gravity",
            1.0,
            20.0,
            9.81
        )

        x, y = projectile_experiment(
            velocity,
            angle,
            gravity
        )

        fig, ax = plt.subplots(
            figsize=(8, 4)
        )

        ax.plot(x, y)

        ax.scatter(
            [x[-1]],
            [y[-1]],
            s=150
        )

        ax.set_xlabel(
            "Horizontal distance (m)"
        )

        ax.set_ylabel(
            "Height (m)"
        )

        ax.set_title(
            "Projectile Motion"
        )

        ax.grid(True)

        st.pyplot(fig)


    # =====================================================
    # FREE FALL
    # =====================================================

    elif "free_fall" in topic:

        st.subheader("🍎 Free Fall Lab")

        height = st.slider(
            "Initial height (m)",
            1.0,
            100.0,
            20.0
        )

        gravity = st.slider(
            "Gravity",
            1.0,
            20.0,
            9.81
        )

        t, y = free_fall_experiment(
            height,
            gravity
        )

        time = st.slider(
            "Time",
            0.0,
            float(t[-1]),
            0.0
        )

        current_height = (
            height
            - 0.5 * gravity * time**2
        )

        current_height = max(
            current_height,
            0
        )

        fig, ax = plt.subplots(
            figsize=(5, 6)
        )

        ax.scatter(
            [0],
            [current_height],
            s=400
        )

        ax.set_xlim(-1, 1)

        ax.set_ylim(
            0,
            height + 5
        )

        ax.set_ylabel(
            "Height (m)"
        )

        ax.set_title(
            "Free Fall"
        )

        st.pyplot(fig)


    # =====================================================
    # NEWTON
    # =====================================================

    elif "newton" in topic:

        st.subheader("🚗 Newton's Second Law Lab")

        mass = st.slider(
            "Mass (kg)",
            1.0,
            20.0,
            5.0
        )

        force = st.slider(
            "Force (N)",
            0.0,
            100.0,
            20.0
        )

        friction = st.slider(
            "Friction (N)",
            0.0,
            50.0,
            0.0
        )

        net_force, acceleration = (
            newton_experiment(
                mass,
                force,
                friction
            )
        )

        st.metric(
            "Acceleration",
            f"{acceleration:.2f} m/s²"
        )

        time = st.slider(
            "Experiment time",
            0.0,
            5.0,
            0.0
        )

        position = (
            0.5
            * acceleration
            * time**2
        )

        fig, ax = plt.subplots(
            figsize=(8, 3)
        )

        ax.scatter(
            [position],
            [0],
            s=mass * 200
        )

        ax.set_xlim(
            0,
            max(10, position + 2)
        )

        ax.set_ylim(
            -1,
            1
        )

        ax.set_yticks([])

        ax.set_title(
            "Newton's Second Law"
        )

        st.pyplot(fig)


    # =====================================================
    # WAVES
    # =====================================================

    elif "waves" in topic:

        st.subheader("🌊 Wave Lab")

        amplitude = st.slider(
            "Amplitude",
            0.1,
            5.0,
            1.0
        )

        frequency = st.slider(
            "Frequency",
            0.1,
            5.0,
            1.0
        )

        x, wave = wave_experiment(
            amplitude,
            frequency
        )

        fig, ax = plt.subplots(
            figsize=(9, 4)
        )

        ax.plot(x, wave)

        ax.axhline(0)

        ax.set_xlabel("Position")

        ax.set_ylabel("Amplitude")

        ax.set_title(
            "Interactive Wave"
        )

        ax.grid(True)

        st.pyplot(fig)


    # =====================================================
    # MCQ
    # =====================================================

    st.divider()

    st.header("🧠 Test Your Understanding")

    st.write(
        sections.get(
            "MCQ",
            "Answer the question below."
        )
    )

    options = {
        "A": sections.get("A", ""),
        "B": sections.get("B", ""),
        "C": sections.get("C", ""),
        "D": sections.get("D", "")
    }

    selected = st.radio(
        "Choose your answer:",
        [
            f"A. {options['A']}",
            f"B. {options['B']}",
            f"C. {options['C']}",
            f"D. {options['D']}"
        ]
    )

    if st.button("✅ Check Answer"):

        selected_letter = selected[0]

        correct = sections.get(
            "ANSWER",
            ""
        ).strip().upper()

        if selected_letter == correct:

            st.success(
                "🎉 Correct! Great understanding."
            )

        else:

            st.error(
                f"Not quite. The correct answer is {correct}."
            )

        st.info(
            sections.get(
                "EXPLANATION",
                ""
            )
        )
