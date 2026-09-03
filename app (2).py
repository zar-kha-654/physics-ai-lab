
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from groq import Groq

st.set_page_config(
    page_title="Physics AI Lab",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Physics AI Lab")
st.write(
    "An interactive physics laboratory where you can experiment "
    "with physical concepts and ask AI to explain what you observe."
)

st.sidebar.header("Choose an Experiment")

experiment_type = st.sidebar.selectbox(
    "Physics Concept",
    [
        "Newton's Second Law",
        "Projectile Motion"
    ]
)

st.divider()

if experiment_type == "Newton's Second Law":

    st.header("⚙️ Newton's Second Law")

    st.write("Explore the relationship between force, mass, and acceleration.")

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
            "Force (N)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0
        )

    with col3:
        friction = st.slider(
            "Friction (N)",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=1.0
        )

    net_force = force - friction
    acceleration = net_force / mass

    st.subheader("Results")

    r1, r2, r3 = st.columns(3)

    r1.metric("Force", f"{force:.1f} N")
    r2.metric("Mass", f"{mass:.1f} kg")
    r3.metric("Acceleration", f"{acceleration:.2f} m/s²")

    st.latex(r"F = ma")
    st.latex(r"a = \frac{F}{m}")

    st.subheader("Interactive Experiment")

    duration = 5
    dt = 0.05

    times = np.arange(0, duration, dt)

    velocity = acceleration * times
    position = 0.5 * acceleration * times**2

    fig, ax = plt.subplots(figsize=(10, 3))

    object_size = 0.3 + mass * 0.025

    ax.set_xlim(
        -1,
        max(10, position[-1] + 2)
    )

    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xlabel("Position (m)")

    object_patch = plt.Rectangle(
        (position[0], -object_size / 2),
        object_size,
        object_size
    )

    ax.add_patch(object_patch)

    progress = st.slider(
        "Run experiment",
        0,
        len(times) - 1,
        0
    )

    object_patch.set_x(position[progress])

    ax.set_title(
        f"Time: {times[progress]:.2f}s | "
        f"Velocity: {velocity[progress]:.2f} m/s"
    )

    st.pyplot(fig)

    st.info(
        f"At this point, the object has traveled "
        f"{position[progress]:.2f} meters."
    )

    st.divider()

    st.subheader("🤖 Ask the AI Physics Tutor")

    question = st.text_input(
        "Ask something about this experiment:"
    )

    if question:

        try:
            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            prompt = f"""
You are an expert physics tutor.

The student is performing an interactive Newton's Second Law experiment.

Current values:
Mass = {mass} kg
Force = {force} N
Friction = {friction} N
Acceleration = {acceleration:.2f} m/s²

Student question:
{question}

Explain the answer clearly for a student.
Connect your explanation to the experiment.
Do not invent results.
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful physics tutor."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(
                "AI Tutor is not connected yet. "
                "The simulation itself is working."
            )


elif experiment_type == "Projectile Motion":

    st.header("🪐 Projectile Motion")

    col1, col2 = st.columns(2)

    with col1:
        velocity = st.slider(
            "Initial velocity (m/s)",
            1.0,
            50.0,
            20.0
        )

    with col2:
        angle = st.slider(
            "Launch angle (degrees)",
            5,
            85,
            45
        )

    gravity = 9.81

    theta = np.radians(angle)

    t = np.linspace(0, 10, 500)

    x = velocity * np.cos(theta) * t
    y = velocity * np.sin(theta) * t - 0.5 * gravity * t**2

    mask = y >= 0

    x = x[mask]
    y = y[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y)

    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Trajectory")
    ax.grid(True)

    st.pyplot(fig)

    st.info(
        "Experiment with the velocity and angle to see how "
        "the projectile trajectory changes."
    )
