import streamlit as st
import json
from datetime import datetime, timedelta, time
from pathlib import Path
from streamlit_calendar import calendar

# Set page configuration for a wide layout
st.set_page_config(page_title="Tennis Scheduler", layout="wide")

# Example data
EXAMPLE_EVENTS = [
    {
        "title": "🎾 Coaching Alice",
        "start": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "end": (datetime.now() + timedelta(days=1, hours=3)).isoformat(),
        "resourceId": "Court 1",
        "backgroundColor": "#C1D6FF",
        "textColor": "#000000",
    },
]

EXAMPLE_CONTACTS = {
    "Alice Smith": "alice@example.com",
    "Bob Johnson": "bob@example.com",
}

EXAMPLE_GROUPS = {
    "Male": ["Bob Johnson", "John Doe"],
    "Female": ["Alice Smith", "Jane Doe"],
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


def sign_in(user_name, password):
    # Create a placeholder
    message_placeholder = st.empty()
    user_data = load_data(USER_DATA_FILE, {})
    if user_name in user_data and user_data[user_name] == password:
        st.session_state["selected_page"] = "Calendar"
        message_placeholder.success("Sign-in successful!")
    elif user_name not in user_data:
        message_placeholder.warning("Username not recognized.")
    else:
        message_placeholder.error("Incorrect password.")

USER_DATA_FILE = Path("user_data.json")
user_data = load_data(USER_DATA_FILE, {})
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Login"

if st.session_state["selected_page"] == "Login":
    # login page if not logged in
    user_name = st.text_input("User Name", key="user_name")
    password = st.text_input("Password", type="password")
    sign_in_button = st.button("Sign In")
    if sign_in_button:
        sign_in(user_name, password)

# Initialize data files
EVENTS_FILE = "plan.json"
DATA_FILE = "data.json"

all_events = load_data(EVENTS_FILE, {"events": EXAMPLE_EVENTS})["events"]
data = load_data(DATA_FILE, {"contacts": EXAMPLE_CONTACTS, "groups": EXAMPLE_GROUPS})
contacts = data.get("contacts", {})
groups = data.get("groups", {})

if "all_events" not in st.session_state:
    st.session_state["all_events"] = all_events
if "contacts" not in st.session_state:
    st.session_state["contacts"] = contacts
if "groups" not in st.session_state:
    st.session_state["groups"] = groups

# Define courts as resources
courts = [
             {"id": f"Court {i}", "title": f"Court {i}"} for i in range(1, 7)
         ] + [{"id": f"Court {i}", "title": f"Court {i} (Indoor)"} for i in range(7, 9)]

# Calendar options
calendar_options = {
    "editable": True,
    "selectable": True,
    "allDaySlot": False,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek",
    },
    "initialView": "resourceTimelineWeek",
    "height": "auto",
    "resources": courts,
    "resourceAreaWidth": "150px",
    "resourceLabelText": "Courts",
    "views": {
        "resourceTimelineDay": {
            "type": "resourceTimeline",
            "duration": {"days": 1},
            "slotMinTime": "07:00:00",
            "slotMaxTime": "24:00:00",
        },
        "resourceTimelineWeek": {
            "type": "resourceTimeline",
            "duration": {"days": 7},
            "slotMinTime": "07:00:00",
            "slotMaxTime": "24:00:00",
        },
    },
}


# Navigation
def navigate(page):
    st.session_state["selected_page"] = page

if st.session_state["selected_page"] != "Login":
    st.sidebar.title("Navigation")

    # Group for the main navigation buttons
    with st.sidebar:
        # Inject custom CSS for flexbox layout
        st.markdown(
            """
            <style>
            /* Sidebar container layout using flexbox */
            [data-testid="stSidebar"] > div:first-child {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
    

            /* Wrapper for navigation buttons */
            .navigation-buttons {
                flex-grow: 100; /* Occupy all available space to push the logout button down */
            }
    
            /* Logout button pinned to the bottom */
            .logout-button {
                margin-top: 150%; /* Automatically pushes the button to the bottom */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Navigation buttons
        st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
        st.button("Calendar", on_click=navigate, args=("Calendar",))
        st.button("Profile", on_click=navigate, args=("Profile",))
        st.button("Contacts", on_click=navigate, args=("Contacts",))
        st.button("Groups", on_click=navigate, args=("Groups",))
        st.markdown('</div>', unsafe_allow_html=True)

        # Logout button pinned to the bottom
        st.markdown('<div class="logout-button">', unsafe_allow_html=True)
        if st.button("Logout", on_click=navigate, args=("Login",)):
            st.write("You have logged out!")
        st.markdown('</div>', unsafe_allow_html=True)


# Pages
if st.session_state["selected_page"] == "Calendar":
    st.title("🎾 Training Scheduler")

    st.subheader("Create a New Event")
    coach = st.selectbox("Coach", ["Felix Ott", "Pino Ott", "Ronny Kemmerich"])

    st.write("### Select Groups")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Male**")
        male_groups = {g: st.checkbox(g) for g in groups.get("Male", [])}
    with col2:
        st.write("**Female**")
        female_groups = {g: st.checkbox(g) for g in groups.get("Female", [])}

    selected_groups = [group for group, selected in {**male_groups, **female_groups}.items() if selected]

    event_start_date = st.date_input("Start Date")
    event_start_time = st.time_input("Start Time", time(8, 0))
    event_end_time = st.time_input("End Time", time(10, 0))

    # Event Type Selection on the Same Line
    col1, col2 = st.columns([1, 2])  # Adjust column width if needed
    with col1:
        event_type = st.radio("Event Type", ["Recurring Event", "Single Event"])
    with col2:
        if event_type == "Recurring Event":
            recurrence_days = st.multiselect("Select Recurrence Days",
                                             ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                                              "Sunday"])
        else:
            recurrence_days = []

    if st.button("Add Event"):
        # Validation to ensure at least one group is selected
        if not selected_groups:
            st.error("You must select at least one group before creating an event.")
        else:
            # Proceed to create the event if a group is selected
            start = datetime.combine(event_start_date, event_start_time).isoformat()
            end = datetime.combine(event_start_date, event_end_time).isoformat()
            for group in selected_groups:
                if event_type == "Single Event":
                    new_event = {
                        "title": group,  # Only show the group or person's name
                        "start": start,
                        "end": end,
                        "resourceId": "Court 1",
                    }
                    st.session_state["all_events"].append(new_event)
                else:
                    for _ in recurrence_days:  # Recurrence days are selected but not part of the title
                        new_event = {
                            "title": group,  # Only show the group or person's name
                            "start": start,
                            "end": end,
                            "resourceId": "Court 1",
                        }
                        st.session_state["all_events"].append(new_event)

            # Save updated events and display success message
            save_data(EVENTS_FILE, {"events": st.session_state["all_events"]})
            st.success(f"Event(s) for {', '.join(selected_groups)} added successfully!")

    st.subheader("Calendar")
    calendar(events=st.session_state["all_events"], options=calendar_options)

    st.subheader("Delete Event")
    if st.session_state["all_events"]:
        event_titles = [event["title"] for event in st.session_state["all_events"]]
        selected_event = st.selectbox("Select Event to Delete", event_titles)
        if st.button("Delete Event"):
            st.session_state["all_events"] = [event for event in st.session_state["all_events"] if
                                              event["title"] != selected_event]
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
    st.write("### Add a New Contact")
    new_name = st.text_input("Name")
    new_email = st.text_input("Email")
    if st.button("Add Contact"):
        if new_name and new_email:
            st.session_state["contacts"][new_name] = new_email
            save_data(DATA_FILE, {"contacts": st.session_state["contacts"], "groups": st.session_state["groups"]})
            st.success(f"Contact {new_name} added successfully!")
        else:
            st.error("Please provide both name and email.")

    st.write("### Delete a Contact")
    if st.session_state["contacts"]:
        contact_to_delete = st.selectbox("Select a Contact", list(st.session_state["contacts"].keys()))
        if st.button("Delete Contact"):
            del st.session_state["contacts"][contact_to_delete]
            save_data(DATA_FILE, {"contacts": st.session_state["contacts"], "groups": st.session_state["groups"]})
            st.success(f"Contact {contact_to_delete} deleted successfully!")
    else:
        st.info("No contacts available.")

elif st.session_state["selected_page"] == "Groups":
    st.title("👥 Groups Page")
    st.write("### Add a New Group")
    new_group_name = st.text_input("Group Name")
    new_group_gender = st.radio("Gender", ["Male", "Female"])
    if st.button("Add Group"):
        if new_group_name:
            st.session_state["groups"].setdefault(new_group_gender, []).append(new_group_name)
            save_data(DATA_FILE, {"contacts": st.session_state["contacts"], "groups": st.session_state["groups"]})
            st.success(f"Group {new_group_name} added to {new_group_gender} groups successfully!")
        else:
            st.error("Please provide a group name.")

    st.write("### Delete a Group")
    gender = st.radio("Select Gender", ["Male", "Female"], key="delete_group_gender")
    if st.session_state["groups"].get(gender):
        group_to_delete = st.selectbox("Select a Group", st.session_state["groups"][gender], key="delete_group")
        if st.button("Delete Group"):
            st.session_state["groups"][gender].remove(group_to_delete)
            save_data(DATA_FILE, {"contacts": st.session_state["contacts"], "groups": st.session_state["groups"]})
            st.success(f"Group {group_to_delete} deleted successfully!")
    else:
        st.info(f"No {gender} groups available.")
