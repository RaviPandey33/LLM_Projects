# import openai
from openai import OpenAI 
import streamlit as st

# Replace 'your-api-key' with your actual OpenAI API key
client = OpenAI(api_key="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")

st.title("Chat with GPT-4")

# Text input for user prompt
# prompt = st.text_input("Enter your question:")

prompt = st.text_area("Enter your question (press Enter to submit):", height=50)


# Button to submit the prompt
if st.button("Ask") or (prompt and st.session_state.get("submit", False)):
    if prompt:
        st.session_state["submit"] = False  # Reset the submit state
        # Send the prompt to ChatGPT and get the response
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Print the response from ChatGPT
        answer = response.choices[0].message.content.strip()
        # st.text_area("ChatGPT's response:", value=answer, height=200)
        
        # st.markdown(f"**ChatGPT's response:**\n\n{answer}")
        
        st.markdown(f"""
        **ChatGPT's response:**
        <div id="response-text">{answer}</div>
        <button onclick="copyToClipboard()">Copy</button>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("response-text").innerText;
            navigator.clipboard.writeText(copyText).then(function() {{
                alert("Copied to clipboard");
            }}, function(err) {{
                console.error("Could not copy text: ", err);
            }});
        }}
        </script>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a question to ask.")


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
