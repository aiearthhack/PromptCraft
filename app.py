import pandas as pd
import streamlit as st
import json
import ast
from st_setup import setup_page
from switch_page import navigation_bar

setup_page()
navigation_bar()

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


# Define a function to get emoji based on pass/fail status
def get_emoji(status):
    return "✅" if (status == "pass") or (status == True) else "❌"

def display_decision(samples, selected_solution):
    """
    Fetches and displays decision information for the selected solution.

    Args:
    samples (DataFrame): DataFrame containing additional information for each solution.
    selected_solution (int): Identifier of the selected solution.
    """
    advance = samples.loc[samples['Solution ID'] == selected_solution, 'Advance'].iloc[0]
    judge_decision = f"Judge Decision: {get_emoji(advance)}"
    if advance:
        st.write(judge_decision)
    else:
        fail_reason = samples.loc[samples['Solution ID'] == selected_solution, 'FailReason_1'].iloc[0]
        st.write(f"{judge_decision}")
        st.write(f"Fail Reason: {fail_reason}")

def render_solution_buttons(samples, solutions):
    """
    Renders a button for each solution. When clicked, it triggers display_decision and
    potentially display_model_data.

    Args:
    samples (DataFrame): DataFrame containing additional information for each solution.
    solutions (list): List of solutions with their id.
    models (dict): Dictionary of model keys with their display names as values.
    """
    st.subheader("Select a Solution:")

    max_columns = 7
    num_rows = (len(solutions) + max_columns - 1) // max_columns

    selected_solution = st.session_state.get('selected_solution')

    for i in range(num_rows):
        row_solutions = solutions[i * max_columns: (i + 1) * max_columns]
        cols = st.columns(len(row_solutions))

        for col, solution in zip(cols, row_solutions):
            with col:
                if st.button(f"Solution {solution}", key=f"solution_{solution}"):
                    st.session_state['selected_solution'] = solution
                    display_decision(samples, solution)
                    print(f"Selected solution: {solution}")

    # # Display decision after looping through all solution buttons
    # if selected_solution is not None:
    #     st.write("")  # Add some space
    #     st.write("")  # Add some space
    #     st.write("")  # Add some space
    #     with st.expander("Decision", expanded=True):
    #         display_decision(samples, selected_solution)
            

# Function to render checkboxes for models under the selected solution
def render_model_checkboxes(models):
    """
    Renders checkboxes for each model in the selected solution.
    Args:
    models (dict): Dictionary of model keys with their display names as values.
    Returns:
    list: List of selected model keys.
    """
    selected_models = []
    st.subheader("Select Models:")
    # Always use three columns for the checkboxes
    cols = st.columns(3)
    # Track the current column index
    col_index = 0

    for model_key, display_name in models.items():
        # Use the current column for this checkbox
        with cols[col_index]:
            if st.checkbox(display_name, key=f"checkbox_{model_key}"):
                selected_models.append(model_key)

        # Move to the next column, and reset to 0 if it exceeds 2 (since there are three columns)
        col_index = (col_index + 1) % 3
    print(f"Selected models: {selected_models}")
    return selected_models

# Function to display model data in columns with collapsible cards
def display_model_data(samples, models, selected_solution, selected_models):
    """
    Displays the selected models' data in columns with collapsible cards.
    Args:
    selected_solution (dict): Dictionary containing models and their criteria from the selected solution.
    selected_models (list): List of keys of selected models.
    """

    criteria = {
    "criterion_1":"Is the solution application complete, appropriate, and intelligible?",
    "criterion_2":"Is the solution at least in Prototype stage?",
    "criterion_3":"Does the solution address the Challenge question?",
    "criterion_4":"Is the solution powered by technology?",
    "criterion_5":"Is the quality of the solution is good enough that an external reviewer should take the time to read and score it?"
    }
    
    if selected_models:
        cols = st.columns(len(selected_models))
        for i, model_key in enumerate(selected_models):
            with cols[i]:
                ad = f"{remove_last_part(model_key)}_advance"
                model_ad = samples.loc[samples['Solution ID']==selected_solution, ad].iloc[0]
                st.markdown(f"###### {models.get(model_key)} {get_emoji(model_ad)}", unsafe_allow_html=True)
                model_data = ast.literal_eval(samples.loc[samples['Solution ID']==selected_solution, model_key].iloc[0])
                for crit, details in model_data.items():
                    with st.expander(f"{get_emoji(details['result'])} **Criterion {crit.split('_')[1]} - {[crit]}**", expanded=True):
                        st.write(f"**Reason:** {details['reason']}", unsafe_allow_html=True)

def apply_custom_css():
    """ Apply custom CSS to reduce padding and margins for maximum screen utilization. """
    custom_css = """
        <style>
            /* General padding and margin adjustments for the app */
            .css-18e3th9 {  /* This is the main content area class as of the latest versions of Streamlit */
                padding: 0rem; /* Eliminate padding around the main content area */
            }
            .stButton {
                display: inline-block;
                width: 20%; /* Adjust width depending on number of checkboxes */
                padding-right: 10px; /* Spacing between checkboxes */
            }
            .activeButton {
                background-color: #007bff; /* Change background color for active state */
                color: #fff; /* Change text color for active state */
                border: 1px solid #007bff; /* Change border color for active state */
                border-radius: 5px;
            }
            .streamlit-expanderHeader {  /* Reduce padding inside expander headers */
                padding: 0.25rem 1rem; /* Smaller padding for a tighter look */
                font-size: 1.25rem;     /* Increase font size in expander headers and bold the title */
            }
            .streamlit-expanderContent {  /* Reduce margin inside expander content */
                margin: 0; /* Remove margin to maximize content space */
            }
            /* Adjust layout for columns to reduce space between them */
            .block-container > .row > .col { 
                padding: 2px; /* Reduce padding between columns */
            }
            /* Adjust overall container size to be more edge-to-edge */
            .main .block-container { 
                max-width: 95%; /* Optionally increase to 100% to use the full width */
            }
                        /* Set the basic font size to 16px */
            html, body, .stApp {
                font-size: 16px;
            }
            /* Make model checkboxes display in a row */
            .stCheckbox {
                display: inline-block;
                width: 20%; /* Adjust width depending on number of checkboxes */
                padding-right: 10px; /* Spacing between checkboxes */
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def remove_last_part(s):
    last_index = s.rfind('_')
    return s[:last_index] if last_index != -1 else s


def show_performance_page():

    st.title("Performance Board")
    apply_custom_css() 



    samples = load_data('static/sample.csv')
    solutions = samples['Solution ID'].to_list()
    # print(f"Solutions: {solutions}")

    models = {
            "gpt_full_result": "Model GPT4 + Full Content + one-shot",
            "gpt_selected_result": "Model GPT4 + Selected Content + one-shot",
            "gpt_summary_result": "Model GPT4 + Summary + one-shot",
            "claude_selected_result":"Model Claude + Selected Content + one-shot",
            "claude_criteria_result":"Model Claude + Selected Content + criterion per shot",
        }
    # print(models.keys())

    if 'selected_solution' not in st.session_state:
        st.session_state['selected_solution'] = None
    render_solution_buttons(samples, solutions)
    if st.session_state['selected_solution'] is not None:
        selected_models = render_model_checkboxes(models)
        display_model_data(samples, models, st.session_state['selected_solution'], selected_models)

if __name__ == "__main__":
    show_performance_page()