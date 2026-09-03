def ask_gpt(question):

    from groq import Groq

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    prompt = f"""
You are the AI tutor inside Physics AI Lab.

A student asked this physics question:

{question}

Your job is to identify the physics concept and help the student learn it.

Return EXACTLY this structure:

TOPIC:
Choose one:
pendulum
projectile
free_fall
newton
waves

SHORT_CONCEPT:
Explain the concept simply in 2-4 sentences.

IMPORTANT_CONCEPTS:
Give 4-5 important ideas separated by commas.

EXPERIMENT:
Describe what the interactive experiment should demonstrate.

MCQ:
Create ONE conceptual multiple-choice question about this topic.

A:
option A

B:
option B

C:
option C

D:
option D

ANSWER:
A, B, C, or D

EXPLANATION:
Explain why the answer is correct.

Keep everything beginner-friendly.
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
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
