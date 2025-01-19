import streamlit as st
import json
from datetime import datetime, timedelta, time
from pathlib import Path
from streamlit_calendar import calendar

# Set global layout to wide
st.set_page_config(page_title="Tennis Scheduler", layout="wide")

# Example data
EXAMPLE_EVENTS = [
    {
        "title": "🎾 Coaching Felix Ott",
        "start": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "end": (datetime.now() + timedelta(days=1, hours=3)).isoformat(),
        "resourceId": "Court 1",
    },
]

EXAMPLE_CONTACTS = {
    "students": {},
    "trainers": {},
    "groups": {}
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
all_events = load_data(EVENTS_FILE, {"events": EXAMPLE_EVENTS})["events"]
data = load_data(DATA_FILE, {"contacts": EXAMPLE_CONTACTS})
contacts = data.get("contacts", EXAMPLE_CONTACTS)

# Ensure keys exist
if "students" not in contacts:
    contacts["students"] = {}
if "trainers" not in contacts:
    contacts["trainers"] = {}
if "groups" not in contacts:
    contacts["groups"] = {}

# Initialize session states
if "all_events" not in st.session_state:
    st.session_state["all_events"] = all_events
if "contacts" not in st.session_state:
    st.session_state["contacts"] = contacts
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Trainingskalender"
if "show_schueler_form" not in st.session_state:
    st.session_state["show_schueler_form"] = False
if "show_trainer_form" not in st.session_state:
    st.session_state["show_trainer_form"] = False
if "show_group_form" not in st.session_state:
    st.session_state["show_group_form"] = False

# Define courts as resources
courts = [
    {"id": f"Court {i}", "title": f"Court {i}"} for i in range(1, 7)
] + [{"id": f"Court {i}", "title": f"Court {i} (Indoor)"} for i in range(7, 9)]

# Updated calendar options with day and week views available in the toolbar
calendar_options = {
    "editable": True,
    "selectable": True,
    "allDaySlot": False,
    "headerToolbar": {
        "left": "prev,next today",  # Navigation buttons
        "center": "title",  # Calendar title
        "right": "resourceTimelineDay,resourceTimelineWeek",  # Buttons for day and week views
    },
    "initialView": "resourceTimelineDay",  # Default to day view
    "height": "auto",  # Automatically adjust height
    "resources": courts,  # Courts displayed as resources in the left column
    "resourceAreaWidth": "200px",  # Adjust width of the resource column
    "resourceLabelText": "Plätze",  # Label for the resource column
    "slotMinTime": "07:00:00",  # Start time for the timeline
    "slotMaxTime": "24:00:00",  # End time for the timeline
    "scrollTime": "08:00:00",  # Start the scroll at 8 AM
}


# Add custom CSS for column borders
def add_column_borders():
    st.markdown(
        """
        <style>
        .column {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
            background-color: #f9f9f9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar Navigation
if st.sidebar.button("Trainingskalender"):
    st.session_state["selected_page"] = "Trainingskalender"
if st.sidebar.button("Mein Profil"):
    st.session_state["selected_page"] = "Mein Profil"
if st.sidebar.button("Kontakte"):
    st.session_state["selected_page"] = "Kontakte"

# Pages
if st.session_state["selected_page"] == "Trainingskalender":
    st.title("Trainingskalender")

    # Create three columns for information above the calendar
    col1, col2, col3 = st.columns(3)

    # Column 1: Trainer Selection
    with col1:
        st.subheader("Neues Training erstellen")
        coach = st.selectbox("Trainer", ["Felix Ott"])

    # Column 2: Court and Group Selection
    with col2:
        st.subheader("Platz und Gruppe auswählen")
        selected_court = st.selectbox("Platz auswählen", [court["title"] for court in courts])
        group = st.selectbox("Gruppe auswählen", ["Keine Gruppe"] + list(st.session_state["contacts"]["groups"].keys()))

    # Column 3: Date and Time Selection
    with col3:
        st.subheader("Datum und Zeit")
        event_start_date = st.date_input("Startdatum")
        event_start_time = st.time_input("Startzeit", time(8, 0))
        event_end_time = st.time_input("Endzeit", time(10, 0))

    # Button to add a new event
    if st.button("Training hinzufügen"):
        start = datetime.combine(event_start_date, event_start_time).isoformat()
        end = datetime.combine(event_start_date, event_end_time).isoformat()

        new_event = {
            "title": f"Training mit Trainer {coach}" + (f" ({group})" if group != "Keine Gruppe" else ""),
            "start": start,
            "end": end,
            "resourceId": selected_court,
        }
        st.session_state["all_events"].append(new_event)
        save_data(EVENTS_FILE, {"events": st.session_state["all_events"]})
        st.success(f"Training mit Trainer {coach} erfolgreich hinzugefügt!")

    # Calendar Section
    st.subheader("Trainingsansicht")
    try:
        calendar(events=st.session_state["all_events"], options=calendar_options)
    except Exception as e:
        st.error(f"Fehler beim Laden des Kalenders: {e}")


elif st.session_state["selected_page"] == "Mein Profil":
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 600px;
            margin: auto;
            padding-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Mein Profil")

    # Display profile information
    st.markdown("### Profilinformationen")
    st.write(f"**Name:** {EXAMPLE_PROFILE['Name']}")
    st.write(f"**E-Mail:** {EXAMPLE_PROFILE['Email']}")
    st.write(f"**Telefon:** {EXAMPLE_PROFILE['Phone']}")
    st.write(f"**Adresse:** {EXAMPLE_PROFILE['Address']}")

elif st.session_state["selected_page"] == "Kontakte":
    st.title("Kontakte")
    add_column_borders()

    col1, col2, col3 = st.columns(3)

    # Schüler/in Column
    with col1:
        st.markdown('<div class="column"><h4>Schüler/in</h4>', unsafe_allow_html=True)
        if st.button("➕ Schüler/in", key="add_schueler"):
            st.session_state["show_schueler_form"] = not st.session_state["show_schueler_form"]
        
        if st.session_state["show_schueler_form"]:
            with st.form("add_schueler_form", clear_on_submit=True):
                name = st.text_input("Full Name", key="schueler_name")
                email = st.text_input("Email", key="schueler_email")
                gender = st.selectbox("Geschlecht", ["m", "w", "d"], key="schueler_gender")
                submitted = st.form_submit_button("Add Schüler/in")
                if submitted:
                    st.session_state["contacts"]["students"][name] = {"email": email, "gender": gender}
                    st.session_state["show_schueler_form"] = False
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})
        
        # Display students
        for student, details in list(st.session_state["contacts"]["students"].items()):
            col_student, col_delete = st.columns([4, 1])
            with col_student:
                st.write(f"{student} ({details['email']}, {details['gender']})")
            with col_delete:
                if st.button("❌", key=f"delete_student_{student}"):
                    del st.session_state["contacts"]["students"][student]
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})

    # Trainer Column
    with col2:
        st.markdown('<div class="column"><h4>Trainer</h4>', unsafe_allow_html=True)
        if st.button("➕ Trainer", key="add_trainer"):
            st.session_state["show_trainer_form"] = not st.session_state["show_trainer_form"]

        if st.session_state["show_trainer_form"]:
            with st.form("add_trainer_form", clear_on_submit=True):
                name = st.text_input("Full Name", key="trainer_name")
                email = st.text_input("Email", key="trainer_email")
                gender = st.selectbox("Geschlecht", ["m", "w", "d"], key="trainer_gender")
                submitted = st.form_submit_button("Add Trainer")
                if submitted:
                    st.session_state["contacts"]["trainers"][name] = {"email": email, "gender": gender}
                    st.session_state["show_trainer_form"] = False
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})

        # Display trainers
        for trainer, details in list(st.session_state["contacts"]["trainers"].items()):
            col_trainer, col_delete = st.columns([4, 1])
            with col_trainer:
                st.write(f"{trainer} ({details['email']}, {details['gender']})")
            with col_delete:
                if st.button("❌", key=f"delete_trainer_{trainer}"):
                    del st.session_state["contacts"]["trainers"][trainer]
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})                

    # Gruppen Column (All actions in column 3)
    with col3:
        st.markdown('<div class="column"><h4>Gruppen</h4>', unsafe_allow_html=True)
        
        # Add Group Button and Form
        if st.button("➕ Gruppen", key="add_group"):
            st.session_state["show_group_form"] = not st.session_state["show_group_form"]

        if st.session_state["show_group_form"]:
            with st.form("add_group_form", clear_on_submit=True):
                group_name = st.text_input("Group Name", key="group_name")
                group_students = st.multiselect(
                    "Add Students to Group",
                    options=list(st.session_state["contacts"]["students"].keys()),
                    key="group_students",
                )
                submitted = st.form_submit_button("Add Group")
                if submitted:
                    st.session_state["contacts"]["groups"][group_name] = group_students
                    st.session_state["show_group_form"] = False
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})
                    st.success(f"Group '{group_name}' successfully created!")

        # Display groups with Delete and Edit buttons
        for group, members in list(st.session_state["contacts"]["groups"].items()):
            group_row = st.columns([4, 1, 1])  # Adjust widths for alignment
            with group_row[0]:
                st.write(f"**{group}:** {', '.join(members)}")
            with group_row[1]:
                if st.button(f"❌", key=f"delete_group_{group}"):
                    del st.session_state["contacts"]["groups"][group]
                    save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})
            with group_row[2]:
                if st.button(f"✏️", key=f"edit_group_{group}"):
                    st.session_state[f"editing_{group}"] = True

            # Edit form for the group
            if st.session_state.get(f"editing_{group}", False):
                with st.form(f"edit_form_{group}", clear_on_submit=False):
                    new_group_name = st.text_input("Gruppenname bearbeiten", value=group)
                    new_group_members = st.multiselect(
                        "Schüler/innen bearbeiten",
                        options=list(st.session_state["contacts"]["students"].keys()),
                        default=members,
                    )
                    submitted = st.form_submit_button("Speichern")
                    if submitted:
                        # Update group details
                        del st.session_state["contacts"]["groups"][group]  # Remove old group
                        st.session_state["contacts"]["groups"][new_group_name] = new_group_members
                        save_data(DATA_FILE, {"contacts": st.session_state["contacts"]})
                        st.session_state[f"editing_{group}"] = False
                        st.success(f"Gruppe '{group}' erfolgreich bearbeitet!")