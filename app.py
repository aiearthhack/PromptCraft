import streamlit as st
from st_setup import setup_page, apply_custom_css
setup_page()

from metrics_page import show_metrics_page
from streamlit_option_menu import option_menu
from performance_page import show_performance_page
from promptground_page import show_promptground_page


apply_custom_css()

def navigation_bar():
    with st.sidebar:
    # with st.container():
        selected = option_menu(
            menu_title="PromptCraft",
            options=["Performance Board", "Metrics", "Promptground"],
            icons=['house', "graph-up-arrow", 'gear'],
            menu_icon="cast",
            # orientation="horizontal",
            default_index=0,
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
        show_promptground_page()
    else:
        show_performance_page()

def main():
    navigation_bar()

if __name__ == "__main__":
    main()