import streamlit as st
import pandas as pd
from dataClean import format_proposal
from SproutsPrompts import get_prompt, get_prompt_list
from solution_columns import get_solution_col, challenge_2023, challenge_2024
import os
from dotenv import load_dotenv


def show_promptground_page():
    # Page title
    st.title("Promptground")

    load_dotenv()
    url = os.environ.get('csv_2023')

    samples = pd.read_csv(url)
    solutions = samples['Solution ID'].tolist()

    st.session_state['samples'] = samples
    st.session_state['prompt_list'] = get_prompt_list()

    # Initialize session state keys if not already present
    if 'assistant_option' not in st.session_state:
        st.session_state['assistant_option'] = "AI Sprouts"
    for i in range(5):
        if f'criterion_{i+1}' not in st.session_state:
            st.session_state[f'criterion_{i+1}'] = False
    if 'solution_id' not in st.session_state:
        st.session_state['solution_id'] = solutions[0]
    if 'solution_type' not in st.session_state:
        st.session_state['solution_type'] = 'Selected Content (16 columns)'
    if 'combined_content' not in st.session_state:
        st.session_state['combined_content'] = ""
    if 'selected_columns_content_per_criterion' not in st.session_state:
        st.session_state['selected_columns_content_per_criterion'] = ""


    st.session_state['full_columns_content'] = get_solution_col(challenge_2023,range(40))
    st.session_state['selected_columns_content'] = get_solution_col(challenge_2023, [1, 3, 4, 5, 6, 7, 8, 11, 12, 13, 20, 21, 25, 26, 28, 29])

    # Create two columns with a 1:2 ratio
    col_left, col_right = st.columns([1, 2])

    # Left Column for Inputs
    with col_left:
        st.subheader("Assistant Instruction")
        assistant_option = st.radio("Choose an Assistant", 
                                    ["AI Sprouts", "Charles/Justin"], 
                                    key='assistant_option',
                                    on_change=render_content)

        st.subheader("Criteria")
        # Using Streamlit's columns function inside the left column to arrange checkboxes in a row
        criteria_cols = st.columns(5)
        criterion_option = []
        for i, col in enumerate(criteria_cols):
            with col:
                # Use a unique key for each checkbox and a callback to update content
                criterion_option.append(st.checkbox(f"{i + 1}", key=f'criterion_{i+1}', on_change=render_content))

        st.subheader("Solution Proposal")
        selected_solution_id = st.selectbox("Select a Solution ID", 
                                            options=solutions,
                                            index=0,
                                            key='solution_id',
                                            format_func=lambda id: f"Solution {id}",
                                            on_change=render_content)
           
        solution_option = st.radio("Select a Solution Content Type", 
                                   ["Full Content (40 columns)", "Selected Content (16 columns)", "GPT4 Summary"],
                                    key='solution_type',
                                    on_change=render_content)
                                   
    # Right Column for Combined Text Output and Copy Button
    with col_right:
        tab1, tab2, tab3, tab4 = st.tabs(["Prompt", 
                                          "Full Content (40 columns)", 
                                          "Selected Content (16 columns)",
                                          "Selected Content per Criterion"])

        with tab1:
            col1, col2 = st.columns([0.8, 0.2])
        # with col1:
        #     st.subheader("Prompt")

        # with col2:
        #     if st.button("Clear All", key="clear_all"):
        #         st.session_state['combined_content'] = ''
        
        # A large text area for combined user input, criteria input, and solution output
        combined_content = st.text_area("Combined instruction, criteria, and solution content into a prompt", 
                                        height=600, 
                                        help="Edit content here", 
                                        value=st.session_state['combined_content'])

        # Copy Button
        if st.button("Copy"):
            # Copy to clipboard and display it
            st.write("Content copied to clipboard:", combined_content)
            st.experimental_set_query_params(text=combined_content)

        with tab2:
            full_content = st.text_area("Full Content (40 columns)",
                                        height=600,
                                        value=st.session_state['full_columns_content'])
            
        with tab3:
            selected_content = st.text_area("Selected Content (16 columns)",
                                            height=600,
                                            value=st.session_state['selected_columns_content'])
        with tab4:
            criterion_content = st.text_area("Selected Content per Criterion",
                                            height=600,
                                            value=st.session_state['selected_columns_content_per_criterion'])

    if st.session_state[f'criterion_{1}']:
        st.session_state['selected_columns_content_per_criterion'] = get_solution_col(challenge_2023, [0, 3, 4, 5, 6, 7, 8, 41])
    elif st.session_state[f'criterion_{2}']:
        st.session_state['selected_columns_content_per_criterion'] = get_solution_col(challenge_2023, [0, 7, 11, 12, 13, 29, 41])
    elif st.session_state[f'criterion_{3}']:
        st.session_state['selected_columns_content_per_criterion'] = get_solution_col(challenge_2023, [0, 4, 5, 6, 7, 41])
    elif st.session_state[f'criterion_{4}']:
        st.session_state['selected_columns_content_per_criterion'] = get_solution_col(challenge_2023, [0, 5, 20, 25, 26, 28, 41])
    elif st.session_state[f'criterion_{5}']:
        st.session_state['selected_columns_content_per_criterion'] = get_solution_col(challenge_2023, [0, 3, 4, 5, 6, 21, 41])

def print_st():
    print(f"assistant_option: {st.session_state['assistant_option']}")
    for i in range(5):
        print(f"criterion_{i+1}: {st.session_state[f'criterion_{i+1}']}")
    print(f"solution_id: {st.session_state['solution_id']}")
    print(f"solution_type: {st.session_state['solution_type']}")
    print(f"combined_content: {st.session_state['combined_content']}")

def render_content():
    """Render the content based on user choices."""
    print_st()

    prompt_list = st.session_state['prompt_list']
    samples = st.session_state['samples']
    content=""
    if st.session_state['assistant_option'] == "AI Sprouts":
        content += get_prompt(prompt_list[0])
        
    elif st.session_state['assistant_option'] == "Charles/Justin":
        content += ""

    for i in range(5):
        if st.session_state[f'criterion_{i+1}']:
            content += "\n\n" + get_prompt(prompt_list[i+1])
    
    if (st.session_state['solution_id'] is not None) & (st.session_state['solution_type'] is not None):
        id = st.session_state['solution_id']
        print(id)
        solution = samples[samples['Solution ID'] == id].iloc[0]
        # print(solution)
        # print()
        if st.session_state['solution_type'] == "Full Content (40 columns)":
            content += "\n\n" + format_proposal(solution, col_selected=False)
            # print(content)
        elif st.session_state['solution_type'] == "Selected Content (16 columns)":
            content += "\n\n" + format_proposal(solution, col_selected=True)
            # print(content)

        elif st.session_state['solution_type'] == "GPT4 Summary":
            content += "\n\n" + samples[samples['Solution ID'] == id]['summary'].iloc[0]
    
    st.session_state['combined_content'] = content


# Display the page
show_promptground_page()
