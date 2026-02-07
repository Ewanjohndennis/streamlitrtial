import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Productivity Dashboard", layout="wide")

DATA_PATH = "data/tasks.csv"

# Create folder & file if not exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=["Tasks", "Category", "Deadline", "Status", "Created"])
    df.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

st.title("Productivity Dashboard")
st.write("All your Tasks in One Place")

# ---------------------------------------------------
# Correct: Use callback to clear inputs
# ---------------------------------------------------
def add_task_callback():
    task = st.session_state.taskinput
    category = st.session_state.categoryinput
    deadline = st.session_state.deadlineinput

    if task.strip() == "":
        return
    
    newtask = pd.DataFrame([{
        "Tasks": task,
        "Category": category,
        "Deadline": str(deadline),
        "Status": "Pending",
        "Created": str(datetime.now().date())
    }])

    updated_df = pd.concat([st.session_state.df_data, newtask], ignore_index=True)
    updated_df.to_csv(DATA_PATH, index=False)
    st.session_state.df_data = updated_df

    # CLEAR FIELDS SAFELY
    st.session_state.taskinput = ""
    st.session_state.categoryinput = "Study"
    st.session_state.deadlineinput = datetime.now().date()

# Store df in session_state
if "df_data" not in st.session_state:
    st.session_state.df_data = df

# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
st.subheader("Add Task")

st.text_input("Task Name", key="taskinput")
st.selectbox("Category", ["Study", "Internship", "Personal", "Other"], key="categoryinput")
st.date_input("Deadline", key="deadlineinput")

st.button("Add Task", on_click=add_task_callback)

# Reload df from session state
df = st.session_state.df_data

# ---------------------------------------------------
# Task List
# ---------------------------------------------------
st.subheader("Your Tasks")

if not df.empty:
    for i in range(len(df)):
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        col1.write(df.loc[i, "Tasks"])
        col2.write(df.loc[i, "Category"])
        col3.write(df.loc[i, "Deadline"])

        if col4.checkbox(f"Done {i}", value=(df.loc[i, "Status"] == "Done")):
            df.loc[i, "Status"] = "Done"
        else:
            df.loc[i, "Status"] = "Pending"

    df.to_csv(DATA_PATH, index=False)
else:
    st.info("No Tasks Added")

# ---------------------------------------------------
# Dashboard Section
# ---------------------------------------------------
st.subheader("Dashboard")

if not df.empty:
    total = len(df)
    completed = len(df[df["Status"] == "Done"])
    pending = total - completed

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tasks", total)
    c2.metric("Completed Tasks", completed)
    c3.metric("Pending Tasks", pending)

    chart_df = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed, pending]
    })

    st.bar_chart(chart_df, x="Status", y="Count")
else:
    st.warning("No Tasks Added")
