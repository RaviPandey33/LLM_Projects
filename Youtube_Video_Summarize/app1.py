from openai import OpenAI
import streamlit as st

# Replace 'your-api-key' with your actual OpenAI API key
client = OpenAI(api_key="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")

st.title("Chat with GPT-4")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Text input for user prompt
with st.form(key='chat_form', clear_on_submit=True):
    prompt = st.text_input("Enter your question:", key='input')
    submit_button = st.form_submit_button(label='Ask')

# Display chat history
for message in st.session_state.messages:
    role = "User" if message["role"] == "user" else "ChatGPT"
    st.markdown(f"**{role}:** {message['content']}")

# Handle form submission
if submit_button and prompt:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send the prompt to ChatGPT and get the response
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state.messages
    )

    # Store ChatGPT response
    answer = response.choices[0].message.content.strip()
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display ChatGPT response
    st.markdown(f"**ChatGPT:** {answer}")

# JavaScript to handle Enter key press in text area
st.markdown(
    """
    <script>
    const textArea = document.querySelector('textarea');
    textArea.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            document.querySelector('button').click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)
