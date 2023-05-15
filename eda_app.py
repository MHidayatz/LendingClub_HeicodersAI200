# Core Packages
import streamlit as st

# Load EDA packages
import pandas as pd

def run_eda_app():
    st.subheader("From Exploratory Data Analysis")
    df = pd.read_csv("data/lc_trainingset.csv")
    st.dataframe(df)
