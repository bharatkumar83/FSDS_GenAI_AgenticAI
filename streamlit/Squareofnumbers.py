import streamlit as st

st.title("My first Streamlit app created by Bharat")

st.write("Welcome to my first Streamlit app!")

st.header("Select a Number")
number = st.slider("Choose a number", 0, 100, 50)

st.subheader("Result")
squared_number = number * number
st.write(f"The square of {number} is {squared_number}.")