import streamlit as st

st.title("Simple Streamlit App")

user_input = st.text_input("Enter something:")

if st.button("Submit"):

    result = f"You entered: {user_input}"

    # Display the result
    st.write(result)

# This is a placeholder for additional elements you might add later
st.write("More features coming soon!")
