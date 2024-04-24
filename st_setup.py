import streamlit as st
import streamlit.components.v1 as components

def setup_page():
    st.set_page_config(
        page_title="PromptCraft | Model and Prompt Evaluation Toolkit",
        page_icon=":rocket:",
        layout="wide",
        initial_sidebar_state='auto',
    )
    components.html(
        """
        <script>
        window.parent.document.querySelector('header').style.display = 'none';
        </script>
        """,
        width=0,
        height=0,
        scrolling=False,
    )
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