import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import time

@st.cache
def get_FPL_data():
    df = pd.read_csv("/Users/praneethramesh/Downloads/FPL20-GW20.csv")
    return df.set_index('Surname')

st.title('FPL Statistics WebApp')

df=get_FPL_data()

st.sidebar.subheader('Filters')
#Sidebar Options
params={
'Team' : st.sidebar.selectbox('Team',df['Team'].unique()),
'PositionsList' : st.sidebar.selectbox('PositionsList',('FWD','MID','DEF','GLK')),
'Cost' : st.sidebar.slider('Max Cost',3800000,max(df['Cost']),step=10000)
}


def map_df(df):
    df=df[df['Team']==params['Team']]
    df=df[df['PositionsList']==params['PositionsList']]
    df=df[df['Cost']<params['Cost']]
    df.reset_index()
    return df

def run_data():
    df1=map_df(df)
    df1

btn = st.sidebar.button("Apply")
if btn:
    run_data()
else:
    pass


#expander = st.beta_expander("FAQ")
#expander.write("To be Filled in Due Time")

#left_column, right_column = st.beta_columns(2)
#pressed = left_column.button('Created By')
#if pressed:
#    right_column.write("Darshil Prajapati & Praneeth Ramesh")



        
