import streamlit as st
import pandas as pd
from dataClean import format_proposal
from SproutsPrompts import get_prompt, get_prompt_list
import os
from dotenv import load_dotenv


def show_promptground_page():
    # Page title
    st.title("Promptground")

    load_dotenv()
    url = os.environ.get('AZURE_URL')

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


    st.session_state['full_columns_content'] = """
    0. Solution ID
    1. Challenge Name
    2. Solution Status
    3. Provide a one-line summary of your solution.
    4. What specific problem are you solving?
    5. What is your solution?
    6. Who does your solution serve, and in what ways will the solution impact their lives?
    7. How are you and your team well-positioned to deliver this solution?
    8. Which dimension of the Challenge does your solution most closely address?
    9. In what city, town, or region is your solution team headquartered?
    10. In what country is your solution team headquartered?
    11. What is your solution's stage of development?
    12. Please share details about what makes your solution a Prototype rather than a Concept.
    13. How many people does your solution currently serve?
    14. Why are you applying to Solve?
    15. In which of the following areas do you most need partners or support?
    16. Is your solution an active or past participant in another entrepreneurship network?
    17. Please share the names of the other entrepreneurship networks.
    18. How did you first hear about Solve?
    19. Tell us more about how you found out about Solveâ€™s 2023 Global Challenges.
    20. What makes your solution innovative?
    21. What are your impact goals for the next year and the next five years, and how will you achieve them?
    22. Which of the UN Sustainable Development Goals does your solution address?
    23. How are you measuring your progress toward your impact goals?
    24. What is your theory of change?
    25. Describe the core technology that powers your solution.
    26. Which of the following categories best describes your solution?
    27. How do you know that this technology works?
    28. Please select the technologies currently used in your solution:
    29. In which countries do you currently operate?
    30. In which countries will you be operating within the next year?
    31. What type of organization is your solution team?
    32. If you selected Other, please explain here.
    33. How many people work on your solution team?
    34. How long have you been working on your solution?
    35. What is your approach to incorporating diversity, equity, and inclusivity into your work?
    36. What is your business model?
    37. Do you primarily provide products or services directly to individuals, to other organizations, or to the government?
    38. What is your plan for becoming financially sustainable?
    39. Share some examples of how your plan to achieve financial sustainability has been successful so far.
    """

    st.session_state['selected_columns_content'] = """
    0. Solution ID
    1. Challenge Name
    3. Provide a one-line summary of your solution.

    4. What specific problem are you solving?
    5. What is your solution?
    6. Who does your solution serve, and in what ways will the solution impact their lives?
    7. How are you and your team well-positioned to deliver this solution?
    8. Which dimension of the Challenge does your solution most closely address?

    11. What is your solution's stage of development?
    12. Please share details about what makes your solution a Prototype rather than a Concept.
    13. How many people does your solution currently serve?

    20. What makes your solution innovative?
    21. What are your impact goals for the next year and the next five years, and how will you achieve them?

    25. Describe the core technology that powers your solution.
    26. Which of the following categories best describes your solution?

    28. Please select the technologies currently used in your solution:
    29. In which countries do you currently operate?
    """

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
        tab1, tab2, tab3 = st.tabs(["Prompt", "Full Content (40 columns)", "Selected Content (16 columns)"])

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
