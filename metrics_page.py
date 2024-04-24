import streamlit as st
import dataprocess as dp
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

st.set_option('deprecation.showPyplotGlobalUse', False)


def show_metrics_page():
    # Page title
    st.header("Metrics")

    # Apply general styling
    st.markdown("""
    <style>
        /* General padding and margin adjustments for the app */
        .css-18e3th9 {
            padding: 0rem; /* Eliminate padding around the main content area */
        }
    </style>
    """, unsafe_allow_html=True)

    # Text
    st.markdown("### Test models and prompts:")
    st.markdown("- Model GPT4 + Full Content + one-shot")
    st.markdown("- Model GPT4 + Selected Content + one-shot")
    st.markdown("- Model GPT4 + Summary + one-shot")
    st.markdown("- Model Claude + Selected Content + one-shot")
    st.markdown("- Model Claude + Selected Content + criterion per shot")
    st.markdown("\n")
    st.markdown("### Test data:")
    st.markdown("- Pass: 6")
    st.markdown("- Fail: 8")
    st.markdown("- Total: 14")

    # Create instances of DataProcessor and Plotter
    url = os.environ.get('AZURE_URL')
    processor = dp.DataProcessor(url)
    plotter = dp.Plotter(processor)

    # Two graphs
    st.subheader("Model Performance Metrics")
    st.pyplot(plotter.plot_metrics())

    st.subheader("Confusion Matrices")
    st.pyplot(plotter.plot_confusion_matrix())


if __name__ == "__main__":
    show_metrics_page()
