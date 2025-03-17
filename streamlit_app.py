import streamlit as st 
from typing import List
from uuid import uuid4
import json
# Initialize questions list in session state
if "Questions" not in st.session_state: 
    st.session_state.Questions = []

# Track selected question
if "SelectedQuestion" not in st.session_state: 
    st.session_state.SelectedQuestion = -1

# Function to add a new question
def add_questions():
    st.session_state.Questions.append({
        "question": "",
        "sample_answer": "",
        "relevant_theory": "",
        "schema": []  # Initialize schema here
    })
    st.session_state.SelectedQuestion = len(st.session_state.Questions) - 1  # Auto-select new question

# Function to add a marking scheme (schema) entry
def add_schema():
    selected_index = st.session_state.SelectedQuestion
    if selected_index != -1:
        st.session_state.Questions[selected_index]['schema'].append({"scheme": "", "score": 0.0})

# Function to delete a schema entry
def delete_schema(index):
    selected_index = st.session_state.SelectedQuestion
    if selected_index != -1 and 0 <= index < len(st.session_state.Questions[selected_index]['schema']):
        del st.session_state.Questions[selected_index]['schema'][index]

# Function to delete a question
def delete_question(index):
    if 0 <= index < len(st.session_state.Questions):
        del st.session_state.Questions[index]
        
    if st.session_state.Questions:
        st.session_state.SelectedQuestion = max(0, index - 1)  # Select previous question
    else:
        st.session_state.SelectedQuestion = -1  # No questions left

# Function to select a question
def select_question(i):
    st.session_state.SelectedQuestion = i

def save_json(file_name:str):
    with open(f"./{file_name}.json",'w') as fptr:
        json.dump(st.session_state.Questions,fp = fptr)

# Sidebar UI
with st.sidebar: 
    sub_name = st.text_input(label="Subject Name")
    st.header("QUESTIONS")
    st.button(label="ADD QUESTION ➕", type="primary", on_click=add_questions)

    # Display each question with side-by-side "Select" and "Delete" buttons
    for i in range(len(st.session_state.Questions)):
        col1, col2 = st.columns([3, 2])
        with col1:
            if st.button(f"📄 QUESTION {i+1}", key=f"select_{i}"):
                select_question(i)  # Select question
        with col2:
            st.button("❌", key=f"del_{i}", on_click=lambda i=i: delete_question(i))  # Delete button
    
    st.download_button(label="DOWNLOAD JSON 📄",file_name="questions.json",data = json.dumps(st.session_state.Questions))


# **Main Content: Show Only Selected Question**
if st.session_state.SelectedQuestion != -1:
    index = st.session_state.SelectedQuestion
    q = st.session_state.Questions[index]

    st.header(f"SETUP: QUESTION {index+1}") 

    q["question"] = st.text_area("Enter Question", value=q["question"], key=f"QUESTION-{index}")
    q["sample_answer"] = st.text_area("Sample Answer", value=q["sample_answer"], key=f"SAMPLE-ANSWER-{index}")
    q["relevant_theory"] = st.text_area("Relevant Theory", value=q["relevant_theory"], key=f"RELEVANT-THEORY-{index}")

    # Add Schema Button
    st.button(label="ADD SCHEMA ➕", type="primary", on_click=add_schema)

    # Display Schema Entries
    for i, schema in enumerate(q["schema"]):
        col1, col2, col3 = st.columns([5, 1, 2])
        with col1:
            schema["scheme"] = st.text_area("Schema", value=schema["scheme"], key=f"SCHEME-{index}-{i}")
        with col2:
            schema["score"] = st.number_input("Score", min_value=0.0, value=schema["score"], step=0.01, format="%0.2f", key=f"SCORE-{index}-{i}")
        with col3:
            st.button(label="DELETE ❌", key=f"SCHEMA-DEL-{index}-{i}", on_click=lambda i=i: delete_schema(i))
