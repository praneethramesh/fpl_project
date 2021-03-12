import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly_express as px
import matplotlib.pyplot as plt
import seaborn as sns
import time

@st.cache
def get_FPL_data():
    df = pd.read_csv("/Users/praneethramesh/Downloads/FPL20-GW20.csv")
    df = df.drop('GW21Forecast', 1)
    df = df.drop('GW22Forecast', 1)
    df = df.drop('GW23Forecast', 1)
    df = df.drop('GW24Forecast', 1)
    df = df.drop('GW25Forecast', 1)
    df = df.drop('GW26Forecast', 1)
    df = df.drop('GW27Forecast', 1)
    df = df.drop('GW28Forecast', 1)
    df = df.drop('GW29Forecast', 1)
    df = df.drop('GW30Forecast', 1)
    df = df.drop('GW31Forecast', 1)
    df = df.drop('GW32Forecast', 1)
    df = df.drop('GW33Forecast', 1)
    df = df.drop('GW34Forecast', 1)
    df = df.drop('GW35Forecast', 1)
    df = df.drop('GW36Forecast', 1)
    df = df.drop('GW37Forecast', 1)
    df = df.drop('GW38Forecast', 1)
    return df.set_index('FirstName')

st.title('FPL Statistics WebApp')

st.markdown('Choose the teams and positions for which you want to scout players for FPL')

df=get_FPL_data()



st.sidebar.subheader('Filters')
#Sidebar Options
params={
'Team' : st.sidebar.multiselect('Team',df['Team'].unique()),
'PositionsList' : st.sidebar.selectbox('PositionsList',('FWD','MID','DEF','GLK')),
'Cost' : st.sidebar.slider('Max Cost',3800000,max(df['Cost'])+500000,step=10000),
'All' :st.sidebar.checkbox('All Teams')
}


def map_df(df):
    if params['All']==1:
        df=df[df['PositionsList']==params['PositionsList']]
        df=df[df['Cost']<=params['Cost']]
        df.reset_index()
        return df
    else:
        df=df[df['Team'].isin(params['Team'])]
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


if st.sidebar.button('Intercorelation Heatmap'):
    st.header('Intercorelation Matrix Heatmap')
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask = mask, vmax=1, square=True)
    
    st.pyplot(f)

#expander = st.beta_expander("FAQ")
#expander.write("To be Filled in Due Time")

#left_column, right_column = st.beta_columns(2)
#pressed = left_column.button('Created By')
#if pressed:
#    right_column.write("Darshil Prajapati & Praneeth Ramesh")
