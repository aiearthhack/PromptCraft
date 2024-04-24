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