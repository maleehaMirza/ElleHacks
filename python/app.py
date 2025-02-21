import json
import streamlit as st
import openai
from openai import OpenAI


# Function to load custom CSS

st.set_page_config(layout="wide")


def load_css(file_path="style.css"):
    with open(file_path, "r") as css_file:
        css_content = css_file.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# Load external CSS
load_css()

# Title for the app


# Sidebar for navigation
st.sidebar.title("Navigation")
tabs = st.sidebar.radio(
    "Go to", ("Home", "AI Chatbot 🤖", "Cyber Quiz 📝", "Cyber Facts 🤔"))

# Home Page - Hello World
if tabs == "Home":
    # Section layout with inner wrapper for each section
    st.markdown('<div id="section1" class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    logo_path = "logo.png"  # Ensure this file is in the same directory as your script

    # Use columns to align the image and text
    col1, col2 = st.columns([3.2, 1])  # Adjust the ratio as needed

    with col1:
        st.markdown('<span class="heading">CyberQueen</span>',
                    unsafe_allow_html=True)

    with col2:
        # Adjust width as needed
        st.image(logo_path, width=500)

    st.write('<span class="big-text">Empower yourself with CyberQueen — your ultimate hub for mastering cybersecurity in a fun and interactive way. </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">Chat, learn, and test your skills to stay safe in the digital world 👩‍💻! </span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="section2" class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="heading2 ai-heading">AI Chatbot 🤖</span>',
             unsafe_allow_html=True)
    st.write('<span class="small-text">Meet your personal AI chatbot, here to make cybersecurity fun and easy! With a mix of girlie charm and tech-savvy smarts, it breaks down online safety concepts using relatable analogies and pop culture references.</span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="small-text">From protecting your passwords like precious accessories to understanding phishing scams, this chatbot empowers you to navigate the digital world with confidence and style.</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="section3" class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="heading2 quiz-heading">Cyber Quiz 📝</span>',
             unsafe_allow_html=True)
    st.write('<span class="small-text"> Ready to test your cybersecurity smarts in a totally new way? Our CyberQuiz is not the typical quiz. We use computer vision to let you answer quiz questions with your hands, so your hands are the key to unlocking the right answers!</span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="small-text">It is an interactive fun way to learn and engage with cybersecurity concepts—all while keeping things hands-on (literally!). Let your hands guide you through the quiz and level up your digital defense skills! </span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div id="section4" class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="heading2 fact-heading">Cyber Facts 🤔</span>',
             unsafe_allow_html=True)
    st.write('<span class="small-text">Ever wonder what happens behind the scenes of the internet? With Cyber Facts, you get a fresh, random nugget of cybersecurity knowledge every time!</span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="big-text">  </span>', unsafe_allow_html=True)
    st.write('<span class="small-text">From mind-boggling hacks to quirky security tips, these facts will keep you sharp, informed, and maybe even a little amazed at the wild world of cybersecurity. Get ready to learn something new and fun—because the digital world is full of surprises! </span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AI Chatbot Page
elif tabs == "AI Chatbot 🤖":
    st.write('<span class="heading2 ai-heading">AI Chatbot 🤖</span>',
             unsafe_allow_html=True)
    st.write('<span class="smaller-text">Struggling with a tough cybersecurity concept? Ask our AI, and it’ll break it down in the simplest, girliest way possible!</span>', unsafe_allow_html=True)
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        instruction = (
            "You are a confident, tech-savvy cybersecurity expert with a stylish, girlie twist. "
            "You explain cybersecurity topics in a fun, approachable, and easy-to-understand way, "
            "using relatable analogies and trendy references to make learning engaging. "
            "Use beauty, fashion, and pop culture analogies to break down cybersecurity concepts—"
            "like treating passwords as designer handbags (keep them exclusive!), or explaining phishing scams like fake luxury dupes. "
            "Your goal is to empower young women to protect themselves online with confidence, "
            "while keeping the conversation light, friendly, and full of girl-power energy!"
        )

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": ""},
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

# Quiz Page
elif tabs == "Cyber Quiz 📝":
    exec(open("quiz.py").read())

elif tabs == "Cyber Facts 🤔":
    exec(open("fact.py").read())
