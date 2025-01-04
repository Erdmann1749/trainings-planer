import streamlit as st
import json
from pathlib import Path

# Set up page config
st.set_page_config(page_title="Sign Up", layout="centered")

# File to store user data
USER_DATA_FILE = Path("user_data.json")

# Mock data for cities and tennis clubs
CITIES_AND_CLUBS = {
    "Berlin": ["Berlin Tennis Club", "Capital Aces", "Spree Swingers"],
    "Munich": ["Munich Masters", "Bavarian Smashers", "Isar Spinners"],
    "Hamburg": ["Hamburg Rackets", "Alster Aces", "North Swingers"],
    "Cologne": ["Cologne Champs", "Rhein Smashers", "Westphalian Warriors"],
    "Frankfurt": ["Frankfurt Flyers", "Main Smashers", "Skyline Swingers"],
}

cities = list(CITIES_AND_CLUBS.keys())
cities.append("Other")  # Add "Other" option for custom cities

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
st.title("Sign Up")

# Sign-Up Form
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
repeat_password = st.text_input("Repeat Password", type="password")
country = st.selectbox("Country", ["USA", "Germany", "France", "UK", "Other"])

# City Selection
city = st.selectbox("City", cities, index=0)
if city == "Other":
    custom_city = st.text_input("Enter your City (Suggestions will appear below)")
    if custom_city:
        suggestions = [c for c in CITIES_AND_CLUBS.keys() if custom_city.lower() in c.lower()]
        if suggestions:
            st.write("Suggestions:")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
else:
    custom_city = None

# Tennis club dropdown (dynamic based on city input)
selected_club = None
if custom_city:
    selected_club = st.text_input("Enter Tennis Club")
elif city != "Other":
    selected_club = st.selectbox(
        "Select Tennis Club", CITIES_AND_CLUBS.get(city, ["No clubs available"])
    )

# Sign-Up Button
if st.button("Sign Up"):
    city_to_save = custom_city if custom_city else city
    if (
        first_name
        and last_name
        and email
        and password
        and repeat_password
        and country
        and city_to_save
        and selected_club
    ):
        if password != repeat_password:
            st.error("Passwords do not match.")
        else:
            user_data = load_user_data()
            if email in user_data:
                st.warning("This email is already registered. Please sign in.")
            else:
                # Save user data
                user_data[email] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password,
                    "country": country,
                    "city": city_to_save,
                    "tennis_club": selected_club,
                }
                save_user_data(user_data)
                st.success("Sign-up successful! You can now sign in.")
                if st.button("Go to Sign In"):
                    st.experimental_set_query_params(page="SignIn")
    else:
        st.error("All fields are required.")
