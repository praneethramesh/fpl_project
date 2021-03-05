import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly_express as px
import time

@st.cache
def get_FPL_data():
    df = pd.read_csv("FPL20-GW20.csv")
    return df.set_index('FirstName')

st.title('FPL Statistics WebApp')

st.markdown('Choose the teams and positions for which you want to scout players for FPL')

df=get_FPL_data()

st.sidebar.subheader('Filters')
#Sidebar Options
params={
'Team' : st.sidebar.multiselect('Team',df['Team'].unique()),
'PositionsList' : st.sidebar.selectbox('PositionsList',('FWD','MID','DEF','GLK')),
'Cost' : st.sidebar.slider('Max Cost',3800000,max(df['Cost'])+500000,step=10000)
}


def map_df(df):
    if params['Team'] != "":
        df=df[df['Team'].isin(params['Team'])]
    else:
        st.write('Dam Dam Dam')
    df=df[df['PositionsList']==params['PositionsList']]
    df=df[df['Cost']<=params['Cost']]
    df.reset_index()
    return df

def run_data():
    df1=map_df(df)
    df1
    fig = px.scatter(df1, x ='Cost',y='AveragePoints',color='Surname')
    st.plotly_chart(fig)



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
