import openai  # Correct import for OpenAI
import streamlit as st
from openai import OpenAI  # Import OpenAI in the same way as in app.py

# Set your OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for model and fact storage
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"  # Default model

if "cyber_fact" not in st.session_state:
    st.session_state["cyber_fact"] = ""  # Stores generated fact

# Function to generate a cybersecurity fact, action, and strengthening advice


def generate_fact_with_combat():
    prompt = """
    Give me a random cybersecurity fact. For that fact, tell me the following:
    1. What action should be taken to combat this cybersecurity issue?
    2. How can a person strengthen their security to prevent this issue from happening?

    Format the output as follows:
    - Fact: [fact]
    - Action to Combat: [action]
    - How to Strengthen: [strengthening advice]
    """

    # Call OpenAI API
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )

    # Extract response content
    fact_text = response.choices[0].message.content.strip()

    # Store the new fact in session state
    st.session_state["cyber_fact"] = fact_text


# Streamlit UI
st.write('<span class="heading2 fact-heading">Cyber Facts 🤔</span>',
         unsafe_allow_html=True)
st.write('<span class="smaller-text">Unlock a new fun and random cybersecurity fact every time you click the button below!</span>', unsafe_allow_html=True)

# Generate new fact when button is pressed
if st.button("Generate Random Cybersecurity Fact"):
    generate_fact_with_combat()  # Update session state with new fact

# Display the fact only if it exists
if st.session_state["cyber_fact"]:
    fact_lines = st.session_state["cyber_fact"].split("\n")

    # Extracting sections correctly
    fact = next((line.replace("- Fact: ", "").strip()
                for line in fact_lines if line.startswith("- Fact:")), "No fact available.")
    action = next((line.replace("- Action to Combat: ", "").strip()
                  for line in fact_lines if line.startswith("- Action to Combat:")), "No action available.")
    strengthening = next((line.replace("- How to Strengthen: ", "").strip()
                         for line in fact_lines if line.startswith("- How to Strengthen:")), "No strengthening advice available.")

    # Display the fact properly
    st.subheader("Fact:")
    st.write(fact)

    st.subheader("Action to Combat:")
    st.write(action)

    st.subheader("How to Strengthen Security:")
    st.write(strengthening)
