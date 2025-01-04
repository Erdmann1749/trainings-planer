import streamlit as st
import json
from pathlib import Path

# Set up page config
st.set_page_config(page_title="Sign In", layout="centered")

# File to store user data
USER_DATA_FILE = Path("user_data.json")

# Load user data
def load_user_data():
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

# Page Title
st.title("Sign In")

# Sign-In Form
email = st.text_input("Email")
password = st.text_input("Password", type="password")
sign_in_button = st.button("Sign In")

if sign_in_button:
    user_data = load_user_data()
    if email in user_data and user_data[email]["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["email"] = email
        st.success("Sign-in successful!")
        st.experimental_rerun()
    elif email not in user_data:
        st.warning("Email not recognized. Please sign up.")
    else:
        st.error("Incorrect password.")

# Redirect to main app if logged in
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.experimental_set_query_params(page="Home")

# Sign-Up Option
st.markdown("---")
st.write("Not registered yet?")
if st.button("Sign Up"):
    st.experimental_set_query_params(page="SignUp")
