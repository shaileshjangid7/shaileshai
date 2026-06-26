import streamlit as st
from google import genai
from google.genai import types

# 1. Page Title UI
st.markdown(
    """
    <h1 style='text-align: center;'> Python AI Assistant</h1>
    <p style='text-align: center; font-size:18px;'>
        Ask any Python programming question.
    </p>
    """,
    unsafe_allow_html=True,
)

# 2. Secure Initialization Block (Saves Client & Chat Rules in Memory)
if "robo" not in st.session_state:
    # Set up client with the stable v1 fix using your Streamlit Secrets key
    st.session_state.robo = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options=types.HttpOptions(api_version="v1")
    )
    
    # Configure your expert rules
    config = types.GenerateContentConfig(
        system_instruction="You are an expert Python developer. "
                           "Answer only questions related to Python programming. "
                           "For any non-Python question, reply exactly: "
                           "Please ask a Python-related question. "
                           "Do not answer questions outside the Python domain."
    )
    
    # Create the persistent chat session
    st.session_state.mychat = st.session_state.robo.chats.create(
        model="gemini-2.5-flash", 
        config=config
    )

# 3. Create a clean Response Box
response_placeholder = st.empty()

# 4. User Input Field
question = st.text_input("", placeholder="Enter your Python question here...")

# Centered Send Button
col1, col2, col3 = st.columns([4, 1, 4])
with col2:
    send = st.button("Send")

# 5. Process the Request safely on Click
if send and question:
    with st.spinner("Analyzing code..."):
        # The session state handles the system rules automatically behind the scenes
        response = st.session_state.mychat.send_message(question)
        response_placeholder.write(response.text)
