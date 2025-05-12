import streamlit as st
import openai
from openai import OpenAI

st.set_page_config(page_title="TACSiS – AI Financial Assistant", layout="wide")
st.title("🧠 TACSiS – AI-Powered Finance Assistant")

# Use modern OpenAI Client (v1.0+)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask TACSiS:", key="user_prompt")

if st.button("Ask"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are TACSiS, a helpful Canadian financial assistant."},
                    *[
                        {"role": "user" if sender == "You" else "assistant", "content": msg}
                        for sender, msg in st.session_state.chat_history
                    ]
                ]
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append(("TACSiS", reply))
        except Exception as e:
            st.session_state.chat_history.append(("TACSiS", f"⚠️ Error: {str(e)}"))

# Show chat
for sender, msg in st.session_state.chat_history[::-1]:
    st.markdown(f"**{sender}:** {msg}")
