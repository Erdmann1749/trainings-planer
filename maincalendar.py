import streamlit as st
import json
from datetime import datetime, time
from pathlib import Path
from streamlit_calendar import calendar

# Load and save data
def load_data():
    file_path = Path("plan.json")
    if file_path.exists():
        with open("plan.json", "r") as f:
            data = json.load(f)
    else:
        data = {"events": []}
    return data

def save_data(data):
    with open("plan.json", "w") as f:
        json.dump(data, f)

# Load events
if "all_events" not in st.session_state:
    st.session_state["all_events"] = load_data().get("events", [])

all_events = st.session_state["all_events"]

# Define coaches and colors
coaches = [
    "Felix Ott",
    "Pino Ott",
    "Ronny Kemmerich",
    "Alex Grozdanovic",
    "Paul Sämann",
]
coach_colors = {
    "Felix Ott": "#C1D6FF",
    "Pino Ott": "#FFD1B2",
    "Ronny Kemmerich": "#B2FFD1",
    "Alex Grozdanovic": "#FFB2D6",
    "Paul Sämann": "#D1B2FF",
}

# Define students and groups
students = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
groups = {
    "1. Herren": ["Max", "Tom", "Leon"],
    "2. Herren": ["Chris", "Luke", "Phil"],
    "Herren 30": ["Jan", "Oliver", "Kevin"],
    "Herren 40": ["Matthias", "Stefan", "Uwe"],
    "1. Damen": ["Sophie", "Marie", "Nina"],
}

# Add colors and ensure proper text visibility for events
for event in all_events:
    event["backgroundColor"] = coach_colors.get(event["resourceId"], "#D3D3D3")
    event["textColor"] = "#000000"  # Set text color to black for readability

# Calendar options
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "timeGridDay,timeGridWeek,dayGridMonth",
    },
    "initialView": "timeGridWeek",
    "height": "auto",
}

# Set Streamlit layout to wide mode
st.set_page_config(layout="wide", page_title="Training Scheduler")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu_options = ["Calendar", "Profile", "Contacts"]
selected_page = st.sidebar.radio("Go to", menu_options)

# Sign Out Button at the bottom
if st.sidebar.button("Sign Out"):
    st.session_state["logged_in"] = False
    st.experimental_rerun()

# Page Content Based on Sidebar Selection
if selected_page == "Calendar":
    st.title("🎾 Training Scheduler")

    # Add Event Section
    st.subheader("Create a New Event")
    coach = st.selectbox("Coach", coaches)

    # Student or Group Selection
    option = st.radio("Select Mode", ["Individual Students", "Groups"])
    if option == "Individual Students":
        selected_students = st.multiselect("Select Student(s)", students, default=[])
    elif option == "Groups":
        selected_group = st.selectbox("Select a Group", list(groups.keys()))
        selected_students = groups[selected_group]

    # Training Details
    training_types = [
        "🎾 Forehand Practice",
        "🎾 Backhand Practice",
        "🎯 Serving Drills",
        "🏃‍♂️ Footwork Training",
        "🌟 Match Strategy",
        "🏅 Match Training",
        "🔄 Overall",
    ]
    training_type = st.selectbox("Type of Training", training_types)
    event_start_date = st.date_input("Start Date")
    event_start_time = st.time_input("Start Time", time(8, 0))
    event_end_time = st.time_input("End Time", time(10, 0))

    # Add Event Button
    if st.button("Add Event"):
        if coach and selected_students and training_type and event_start_date and event_start_time and event_end_time:
            # Combine date and time for start and end
            start = datetime.combine(event_start_date, event_start_time).isoformat()
            end = datetime.combine(event_start_date, event_end_time).isoformat()

            # Create events for each selected student
            for student in selected_students:
                new_event = {
                    "title": f"{training_type} - {coach} Coaching {student}",
                    "start": start,
                    "end": end,
                    "resourceId": coach,
                    "backgroundColor": coach_colors.get(coach, "#D3D3D3"),
                    "textColor": "#000000",
                }
                st.session_state["all_events"].append(new_event)

            # Save updated events
            save_data({"events": st.session_state["all_events"]})
            st.success(f"Event for {', '.join(selected_students)} added successfully!")

    # View Coach Dropdown
    st.subheader("View Coach")
    view_options = ["All"] + coaches
    selected_view = st.selectbox("View", view_options)

    # Filter events based on the selected view
    if selected_view == "All":
        filtered_events = st.session_state["all_events"]
    else:
        filtered_events = [
            event for event in st.session_state["all_events"] if event["resourceId"] == selected_view
        ]

    # Calendar Section
    st.subheader("Calendar")
    st.markdown('<div class="streamlit-calendar-container">', unsafe_allow_html=True)
    calendar(events=filtered_events, options=calendar_options)
    st.markdown('</div>', unsafe_allow_html=True)

    # Delete Event Section
    st.subheader("Delete an Event")
    if st.session_state["all_events"]:
        # Dropdown to select an event to delete
        event_titles = [event["title"] for event in st.session_state["all_events"]]
        selected_event = st.selectbox("Select an Event to Delete", event_titles)

        if st.button("Delete Event"):
            # Find and remove the selected event
            st.session_state["all_events"] = [
                event for event in st.session_state["all_events"] if event["title"] != selected_event
            ]

            # Save updated events
            save_data({"events": st.session_state["all_events"]})
            st.success(f"Event '{selected_event}' deleted successfully!")
    else:
        st.info("No events available to delete.")

elif selected_page == "Profile":
    st.title("👤 Profile Page")
    st.write("Welcome to your profile!")
    st.write("Manage your personal information here.")

elif selected_page == "Contacts":
    st.title("📇 Contacts Page")
    st.write("Manage your contacts here!")
    st.write("You can add, view, and edit your contact list.")
