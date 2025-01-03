import streamlit as st
import json
from pathlib import Path


def store_input(data, coach, day, hour, clients):
    if coach in data:
        if day in data[coach]:
            data[coach][day][str(hour)] = clients.split(",")
        else:
            data[coach][day] = {str(hour): clients.split(",")}
    else:
        data[coach] = {day: {str(hour): clients.split(",")}}
    with open("plan.json", "w") as f:
        json.dump(data, f)

def load_data():
    # if filename not exists
    file_path = Path("plan.json")
    if file_path.exists():
        with open("plan.json", "r") as f:
            data = json.load(f)
    else:
        data = {}
    return data

# App title
st.title("Coaching Session Input Form")

# Input form
with st.form("coaching_form"):
    # Input fields
    coach_name = st.text_input("Trainer Name")
    day_in_week = st.selectbox("Day in Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    client_names = st.text_area("Client Names (separated by commas)")
    hour_in_day = st.time_input("Hour in Day")

    # Submit button
    data = load_data()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Session submitted successfully!")
        store_input(data, coach_name, day_in_week, hour_in_day, client_names)

    # Display the input values
    data = load_data()
    for coach, days in data.items():
        for day, details in days.items():
            st.write(f"### {coach} - {day}")
            for hour_in_day, client_names in details.items():
                st.write(f"- Hour: {hour_in_day} - Clients: {', '.join(client_names)}")
