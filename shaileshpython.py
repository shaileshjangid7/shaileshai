import streamlit as st
from google import genai
from google.genai import types
config = types.GenerateContentConfig(
    system_instruction = """.You are an expert Python developer.
 Answer only questions related to Python programming.
 For any non-Python question, reply exactly:
 Please ask a Python-related question.
 Do not answer questions outside the Python domain."""
  )
st.markdown(
  """
  <h1 style='text-align: center;'> Python AI Assistant</h1>
  <p style='text-align: center; font-size:18px;'>
    Ask any Python programming question.
  </p>
  """,
  unsafe_allow_html=True,
)
robo = genai.Client( api_key=st.secrets["GOOGLE_API_KEY"])
mychat = robo.chats.create(model="gemini-flash-lite-latest")

Placeholder for the response
response_placeholder = st.empty()

question = st.text_input("", placeholder="Enter your Python question here...")

col1, col2, col3 = st.columns([4, 1, 4])

with col2:
  send =st.button("Send")

if send:
  question = question + config.system_instruction
  response = mychat.send_message(question)
  response_placeholder.write(response.text)
