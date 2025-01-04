import streamlit as st
import json
from datetime import datetime, timedelta, time
from pathlib import Path
from streamlit_calendar import calendar

# Example data
EXAMPLE_EVENTS = [
    {
        "title": "🎾 Forehand Practice - Felix Coaching Alice",
        "start": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "end": (datetime.now() + timedelta(days=1, hours=3)).isoformat(),
        "resourceId": "Felix Ott",
        "backgroundColor": "#C1D6FF",
        "textColor": "#000000",
    },
    {
        "title": "🎾 Backhand Practice - Pino Coaching Bob",
        "start": (datetime.now() + timedelta(days=2, hours=1)).isoformat(),
        "end": (datetime.now() + timedelta(days=2, hours=2)).isoformat(),
        "resourceId": "Pino Ott",
        "backgroundColor": "#FFD1B2",
        "textColor": "#000000",
    },
]

EXAMPLE_STUDENTS = {
    "Alice Smith": "alice@example.com",
    "Bob Johnson": "bob@example.com",
    "Charlie Brown": "charlie@example.com",
    "Diana Prince": "diana@example.com",
    "Eve White": "eve@example.com",
}

EXAMPLE_GROUPS = {
    "1. Herren": ["Alice Smith", "Bob Johnson"],
    "2. Herren": ["Charlie Brown", "Diana Prince"],
    "Herren 30": ["Eve White"],
}

EXAMPLE_PROFILE = {
    "Name": "Tennis Coach",
    "Email": "coach@example.com",
    "Phone": "+49 123 456 789",
    "Address": "123 Tennis Court Lane, Berlin, Germany",
}

# Load and save data
def load_data(file_name, default_data):
    file_path = Path(file_name)
    if file_path.exists():
        with open(file_name, "r") as f:
            data = json.load(f)
    else:
        data = default_data
    return data

def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f)

# Initialize data files
EVENTS_FILE = "plan.json"
DATA_FILE = "data.json"

# Load or set default data
all_events = load_data(EVENTS_FILE, {"events": EXAMPLE_EVENTS})["events"]
data = load_data(DATA_FILE, {"students": EXAMPLE_STUDENTS, "groups": EXAMPLE_GROUPS})
students = data.get("students", {})
groups = data.get("groups", {})

if "all_events" not in st.session_state:
    st.session_state["all_events"] = all_events
if "students" not in st.session_state:
    st.session_state["students"] = students
if "groups" not in st.session_state:
    st.session_state["groups"] = groups

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

# Add colors to events
for event in st.session_state["all_events"]:
    event["backgroundColor"] = coach_colors.get(event["resourceId"], "#D3D3D3")
    event["textColor"] = "#000000"  # Ensure text visibility

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
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Calendar"

# Define navigation function
def navigate(page):
    st.session_state["selected_page"] = page

st.sidebar.title("Navigation")
st.sidebar.button("Calendar", on_click=navigate, args=("Calendar",))
st.sidebar.button("Profile", on_click=navigate, args=("Profile",))
st.sidebar.button("Contacts", on_click=navigate, args=("Contacts",))
st.sidebar.button("Groups", on_click=navigate, args=("Groups",))

# Sign Out Button at the bottom
st.sidebar.markdown("---")
if st.sidebar.button("Sign Out"):
    st.session_state["logged_in"] = False
    st.experimental_rerun()

# Page Content Based on Selected Page
if st.session_state["selected_page"] == "Calendar":
    st.title("🎾 Training Scheduler")

    # Add Event Section
    st.subheader("Create a New Event")
    coach = st.selectbox("Coach", coaches)

    # Student or Group Selection
    option = st.radio("Select Mode", ["Individual Students", "Groups"])
    if option == "Individual Students":
        selected_students = st.multiselect("Select Student(s)", list(students.keys()), default=[])
        group_event = False
    elif option == "Groups":
        selected_group = st.selectbox("Select a Group", list(groups.keys()))
        if selected_group != "Choose an Option":
            selected_students = groups[selected_group]
            group_event = True
        else:
            selected_students = []
            group_event = False

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

            if group_event:
                # Create one event for the entire group
                new_event = {
                    "title": f"{training_type} - {coach} Coaching {selected_group}",
                    "start": start,
                    "end": end,
                    "resourceId": coach,
                    "backgroundColor": coach_colors.get(coach, "#D3D3D3"),
                    "textColor": "#000000",
                }
                st.session_state["all_events"].append(new_event)
                st.success(f"Event for group '{selected_group}' added successfully!")
            else:
                # Create individual events for each student
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
                st.success(f"Event for {', '.join(selected_students)} added successfully!")

            # Save updated events
            save_data(EVENTS_FILE, {"events": st.session_state["all_events"]})

    # Calendar Section
    st.subheader("Calendar")
    calendar(events=st.session_state["all_events"], options=calendar_options)

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
            save_data(EVENTS_FILE, {"events": st.session_state["all_events"]})
            st.success(f"Event '{selected_event}' deleted successfully!")
    else:
        st.info("No events available to delete.")

elif st.session_state["selected_page"] == "Profile":
    st.title("👤 Profile Page")
    st.write(f"**Name:** {EXAMPLE_PROFILE['Name']}")
    st.write(f"**Email:** {EXAMPLE_PROFILE['Email']}")
    st.write(f"**Phone:** {EXAMPLE_PROFILE['Phone']}")
    st.write(f"**Address:** {EXAMPLE_PROFILE['Address']}")

elif st.session_state["selected_page"] == "Contacts":
    st.title("📇 Contacts Page")

    # Section: Add New Student
    st.subheader("Add a New Student")
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("First Name")
        surname = st.text_input("Last Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if name and surname and email:
                full_name = f"{name} {surname}"
                if full_name in st.session_state["students"]:
                    st.warning(f"Student '{full_name}' already exists.")
                else:
                    st.session_state["students"][full_name] = email
                    save_data(DATA_FILE, {"students": st.session_state["students"], "groups": st.session_state["groups"]})
                    st.success(f"Student '{full_name}' added successfully!")
            else:
                st.error("Please fill in all fields.")

    # Section: Display Student Contacts
    st.subheader("Student Contacts")
    for student, email in st.session_state["students"].items():
        st.markdown(
            f"""
            <div style="background-color: #d3d3d3; padding: 15px; border-radius: 10px; border: 1px solid #a9a9a9; margin-bottom: 10px; font-size: 16px; color: black;">
                <strong>{student}</strong>: {email}
            </div>
            """,
            unsafe_allow_html=True,
        )

elif st.session_state["selected_page"] == "Groups":
    st.title("👥 Group Management")

    # Section: Create a New Group
    st.subheader("Create a New Group")
    group_name = st.text_input("Enter Group Name")
    if group_name:
        if group_name in groups:
            st.warning("This group name already exists. Choose a different name.")
        else:
            # Allow selecting students after entering a valid group name
            st.markdown("### Select Students for the Group")
            group_members = st.multiselect("Choose Students", list(students.keys()))
            if st.button("Create Group"):
                if group_members:
                    groups[group_name] = group_members
                    st.session_state["groups"] = groups
                    save_data(DATA_FILE, {"students": st.session_state["students"], "groups": st.session_state["groups"]})
                    st.success(f"Group '{group_name}' created successfully with members: {', '.join(group_members)}!")
                else:
                    st.error("Please select at least one student to create a group.")
    else:
        st.info("Enter a group name to start creating a group.")

    # Section: Existing Groups
    st.subheader("Existing Groups")
    if groups:
        for group_name, members in groups.items():
            st.markdown(
                f"""
                <div style="background-color: #d3d3d3; padding: 15px; border-radius: 10px; border: 1px solid #a9a9a9; margin-bottom: 10px; font-size: 16px; color: black;">
                    <strong>{group_name}</strong>: {', '.join(members)}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No groups available.")

    # Section: Delete a Group
    st.subheader("Delete a Group")
    if groups:
        group_to_delete = st.selectbox("Select a Group to Delete", ["Choose an Option"] + list(groups.keys()))
        if group_to_delete != "Choose an Option":
            if st.button("Delete Group"):
                del groups[group_to_delete]
                st.session_state["groups"] = groups
                save_data(DATA_FILE, {"students": students, "groups": groups})
                st.success(f"Group '{group_to_delete}' deleted successfully!")
    else:
        st.info("No groups available to delete.")
