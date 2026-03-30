from pawpal_system import Owner, Pet, Task, Scheduler, Priority
import streamlit as st
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Session state memory
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)

if st.button("Add pet"):
    new_pet = Pet(pet_name, species, int(pet_age), owner)
    owner.add_pet(new_pet)
    st.session_state.selected_pet = new_pet
    st.success(f"{pet_name} was added successfully.")

if owner.get_pets():
    st.write("Current pets:")
    pet_table = [
        {"name": pet.name, "species": pet.species, "age": pet.age}
        for pet in owner.get_pets()
    ]
    st.table(pet_table)
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if owner.get_pets():
    pet_options = [pet.name for pet in owner.get_pets()]
    selected_pet_name = st.selectbox("Choose pet", pet_options)

    selected_pet = next(
        (pet for pet in owner.get_pets() if pet.name == selected_pet_name),
        None
    )

    task_title = st.text_input("Task title", value="Morning walk")
    task_category = st.text_input("Task category", value="Walk")
    task_hour = st.number_input("Hour", min_value=0, max_value=23, value=8)
    task_minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority_label = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"], index=2)

    if st.button("Add task"):
        priority_map = {
            "LOW": Priority.LOW,
            "MEDIUM": Priority.MEDIUM,
            "HIGH": Priority.HIGH,
        }

        new_task = Task(
            title=task_title,
            category=task_category,
            due_time=time(int(task_hour), int(task_minute)),
            duration=int(duration),
            priority=priority_map[priority_label],
            pet=selected_pet,
        )

        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added for {selected_pet.name}.")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("Current Tasks")
all_tasks = owner.get_all_tasks()
if all_tasks:
    task_table = [
        {
            "pet": task.pet.name,
            "title": task.title,
            "category": task.category,
            "time": str(task.due_time),
            "duration": task.duration,
            "priority": task.priority.name,
            "completed": task.completed,
        }
        for task in all_tasks
    ]
    st.table(task_table)
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    schedule = scheduler.generate_daily_plan()
    conflicts = scheduler.detect_conflicts()

    st.markdown("### Today's Schedule")
    if schedule:
        for task in schedule:
            st.write(
                f"{task.due_time} | {task.pet.name} | {task.title} ({task.category})"
            )
    else:
        st.info("No tasks to schedule.")

    st.markdown("### Conflicts")
    if conflicts:
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("No conflicts found.")