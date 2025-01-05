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
]

EXAMPLE_STUDENTS = {
    "Alice Smith": "alice@example.com",
    "Bob Johnson": "bob@example.com",
}

EXAMPLE_GROUPS = {
    "1. Herren": ["Alice Smith", "Bob Johnson"],
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
data = load_data(DATA_FILE, {"students": EXAMPLE_STUDENTS, "groups": EXAMPLE_GROUPS, "coaches": {}})
students = data.get("students", {})
groups = data.get("groups", {})
coaches = data.get("coaches", {})

if "all_events" not in st.session_state:
    st.session_state["all_events"] = all_events
if "students" not in st.session_state:
    st.session_state["students"] = students
if "groups" not in st.session_state:
    st.session_state["groups"] = groups
if "coaches" not in st.session_state:
    st.session_state["coaches"] = coaches

# Define coaches and colors
all_coaches = [
    "Felix Ott",
    "Pino Ott",
    "Ronny Kemmerich",
]
coach_colors = {
    "Felix Ott": "#C1D6FF",
    "Pino Ott": "#FFD1B2",
    "Ronny Kemmerich": "#B2FFD1",
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

def navigate(page):
    st.session_state["selected_page"] = page

st.sidebar.title("Navigation")
st.sidebar.button("Calendar", on_click=navigate, args=("Calendar",))
st.sidebar.button("Profile", on_click=navigate, args=("Profile",))
st.sidebar.button("Contacts", on_click=navigate, args=("Contacts",))
st.sidebar.button("Groups", on_click=navigate, args=("Groups",))

# Page Content
if st.session_state["selected_page"] == "Calendar":
    st.title("🎾 Training Scheduler")
    st.subheader("Create a New Event")
    coach = st.selectbox("Coach", all_coaches)

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

    training_types = ["🎾 Forehand Practice", "🎾 Backhand Practice", "🏃‍♂️ Footwork Training"]
    training_type = st.selectbox("Type of Training", training_types)
    event_start_date = st.date_input("Start Date")
    event_start_time = st.time_input("Start Time", time(8, 0))
    event_end_time = st.time_input("End Time", time(10, 0))

    # Event Type
    event_type = st.radio("Event Type", ["Single Event", "Recurring Event"])
    recurrence_days = []
    if event_type == "Recurring Event":
        recurrence_days = st.multiselect("Select Days for Recurrence", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    if st.button("Add Event"):
        start = datetime.combine(event_start_date, event_start_time).isoformat()
        end = datetime.combine(event_start_date, event_end_time).isoformat()
        if group_event:
            # Add recurring events for groups
            if event_type == "Recurring Event":
                for day in recurrence_days:
                    recurring_date = event_start_date + timedelta(days=(list(calendar.day_name).index(day) - event_start_date.weekday()) % 7)
                    recurring_start = datetime.combine(recurring_date, event_start_time).isoformat()
                    recurring_end = datetime.combine(recurring_date, event_end_time).isoformat()
                    new_event = {
                        "title": f"{training_type} - {coach} Coaching {selected_group}",
                        "start": recurring_start,
                        "end": recurring_end,
                        "resourceId": coach,
                        "backgroundColor": coach_colors.get(coach, "#D3D3D3"),
                        "textColor": "#000000",
                    }
                    st.session_state["all_events"].append(new_event)
        else:
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

        save_data(EVENTS_FILE, {"events": st.session_state["all_events"]})
        st.success(f"Event for {', '.join(selected_students)} added successfully!")

    # Calendar Section
    st.subheader("Calendar")
    calendar(events=st.session_state["all_events"], options=calendar_options)

    # Delete Event Section
    st.subheader("Delete an Event")
    if st.session_state["all_events"]:
        event_titles = [event["title"] for event in st.session_state["all_events"]]
        selected_event = st.selectbox("Select an Event to Delete", event_titles)
        if st.button("Delete Event"):
            st.session_state["all_events"] = [event for event in st.session_state["all_events"] if event["title"] != selected_event]
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
    st.subheader("Add a New Contact")
    with st.form("add_contact_form", clear_on_submit=True):
        contact_type = st.radio("Contact Type", ["Student", "Coach"])
        name = st.text_input("First Name")
        surname = st.text_input("Last Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Contact")
        if submitted:
            full_name = f"{name} {surname}"
            contact_list = st.session_state["students"] if contact_type == "Student" else st.session_state["coaches"]
            if full_name in contact_list:
                st.warning(f"{contact_type} '{full_name}' already exists.")
            else:
                contact_list[full_name] = email
                if contact_type == "Student":
                    st.session_state["students"] = contact_list
                else:
                    st.session_state["coaches"] = contact_list
                save_data(DATA_FILE, {"students": st.session_state["students"], "groups": st.session_state["groups"], "coaches": st.session_state["coaches"]})
                st.success(f"{contact_type} '{full_name}' added successfully!")

    st.subheader("Student Contacts")
    for student, email in st.session_state["students"].items():
        st.write(f"**{student}**: {email}")

    st.subheader("Coach Contacts")
    for coach, email in st.session_state["coaches"].items():
        st.write(f"**{coach}**: {email}")

elif st.session_state["selected_page"] == "Groups":
    st.title("👥 Group Management")
    st.subheader("Create a New Group")
    group_name = st.text_input("Enter Group Name")
    group_members = st.multiselect("Choose Students", list(students.keys()))
    if st.button("Create Group"):
        if group_name in groups:
            st.warning("Group already exists.")
        else:
            groups[group_name] = group_members
            st.session_state["groups"] = groups
            save_data(DATA_FILE, {"students": students, "groups": groups, "coaches": coaches})
            st.success(f"Group '{group_name}' created!")

    st.subheader("Existing Groups")
    for group, members in groups.items():
        st.write(f"**{group}**: {', '.join(members)}")
