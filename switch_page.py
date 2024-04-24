import streamlit as st
from metrics_page import show_metrics_page
from streamlit_option_menu import option_menu


def navigation_bar():
    with st.sidebar:
    # with st.container():
        selected = option_menu(
            menu_title="PromptCraft",
            options=["Performance Board", "Metrics", "Promptground"],
            icons=['house', "graph-up-arrow", 'gear'],
            menu_icon="cast",
            # orientation="horizontal",
            styles={
                "nav-link": {
                    "text-align": "left",
                    "--hover-color": "#eee",
                }
            }
        )
    if selected == "Metrics":
        show_metrics_page()
    elif selected == "Promptground":
        show_promptground()
    else:
        show_performance_page()