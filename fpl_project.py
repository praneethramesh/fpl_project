import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import time

@st.cache
def get_FPL_data():
    df = pd.read_csv("/FPL20-GW20.csv")
    return df.set_index("Team")

st.title('FPL Statistics WebApp')
df = get_FPL_data()
team = st.multiselect(
    "Choose teams", list(df.index), ["ARS", "LIV"]
)
if not team:
    st.error("Please select at least one team.")
else:
    data = df.loc[team]
    st.write("### FPL Database", data.sort_index())

    data = data.T.reset_index()

expander = st.beta_expander("FAQ")
expander.write("To be Filled in Due Time")

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Created By')
if pressed:
    right_column.write("Darshil Prajapati & Praneeth Ramesh")



        
