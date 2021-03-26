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
    df = pd.read_csv("combined_GW30.csv")
    return df

st.title('FPL Predictions WebApp')

st.markdown('GW 30 Predictions')

st.markdown('Choose the teams and positions for which you want to scout players for FPL and click Apply')

st.markdown('We have formulated a top 10 list for Strikers, Midfielders and Defenders and a top 5 list for Goalkeepers by default')

df=get_FPL_data()

st.sidebar.subheader('Filters')

#Sidebar Options
params={
'Team' : st.sidebar.multiselect('Team',df['Team'].unique()),
'Positions' : st.sidebar.selectbox('Positions',('FWD','MID','DEF','GK')),
'Cost' : st.sidebar.slider('Max Cost',3.0,max(df['Price'])+1,step=1.0),
'All' :st.sidebar.checkbox('All Teams'),
'Remove' :st.sidebar.checkbox('Disregard players unlikely to play')
}

def map_df(df):
    df=df[df['Predicted Points'] > 0.1]
    if params['Remove']==1:
        df=df[df['Play Probability'] > 0.5]

    if params['All']==1:
        df=df[df['Position']==params['Positions']]
        df=df[df['Price']<=params['Cost']]
        df.reset_index()
    else:
        df=df[df['Team'].isin(params['Team'])]
        df=df[df['Position']==params['Positions']]
        df=df[df['Price']<=params['Cost']]
        df.reset_index()
    return df

def run_data():
    df1=map_df(df)
    df1
    st.write(df1.iloc[0]['Player'],', has the highest predicted score for GW30')
    df1=df1.head(10)
    fig = px.line(df1, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

def top10fwd(df):
    df=df[df['Predicted Points'] > 0.1]
    df=df[df['Play Probability'] > 0.5]
    df=df[df['Position']=='FWD']
    
    df2=df.head(10)
    df2

    st.write(df2.iloc[0]['Player'],', has the highest predicted score for GW30')
    fig = px.line(df2, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

def top10mid(df):
    df=df[df['Predicted Points'] > 0.1]
    df=df[df['Play Probability'] > 0.5]
    df=df[df['Position']=='MID']
    
    df3=df.head(10)
    df3

    st.write(df3.iloc[0]['Player'],', has the highest predicted score for GW30')
    fig = px.line(df3, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

def top10def(df):
    df=df[df['Predicted Points'] > 0.1]
    df=df[df['Play Probability'] > 0.5]
    df=df[df['Position']=='DEF']
    
    df4=df.head(10)
    df4
    
    st.write(df4.iloc[0]['Player'],', has the highest predicted score for GW30')
    fig = px.line(df4, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

def top5gk(df):
    df=df[df['Predicted Points'] > 0.1]
    df=df[df['Play Probability'] > 0.5]
    df=df[df['Position']=='GK']
    
    df5=df.head(5)
    df5

    st.write(df5.iloc[0]['Player'],', has the highest predicted score for GW30')
    fig = px.line(df5, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

def dreamTeam():
    df6 = pd.read_csv("dreamteam_GW30.csv")
    
    return df6

btn = st.sidebar.button("Apply")
btn_reset = st.sidebar.button("Reset Screen")

if st.button('Top 10 Strikers'):
    top10fwd(df)

if st.button('Top 10 Midfielders'):
    top10mid(df)

if st.button('Top 10 Defenders'):
    top10def(df)

if st.button('Top 5 Goal Keepers'):
    top5gk(df)

if btn:
    run_data()
else:
    pass

if btn_reset:
    get_FPL_data()
else:
    pass

if st.sidebar.button('Intercorelation Heatmap'):
    st.header('Intercorelation Matrix Heatmap')
    st.markdown('Each square shows the correlation between the variables on each axis. Values closer to zero means there is no linear trend between the two variables. Value closer to 1 means they are more positively correlated; that is as one increases so does the other and stronger the relationship between the two. The diagonals are correlating each variable to itself. For the rest the darker the color the higher the correlation between the two variables.')
    df = pd.read_csv("FPL20-GW20.csv")
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
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask = mask, vmax=1, square=True)
    
    st.pyplot(f)

if st.sidebar.button('DreamTeam Composition Prediction'):
    st.title("Predicted Dreamteam Composition for GW30")
    df6=dreamTeam()
    df6

    fig = px.line(df6, x ='Predicted Points',y='FirstName')
    st.plotly_chart(fig)

expander = st.beta_expander("Method behind the Madness:")
expander.write("We have used the FPL data from 2017-2019 to train our model. We have used XG Boost to predict the FPL points for all the players in GW30 of 20/21 Season")
expander.write("'The Ball is round, the game lasts 90 minutes, and everything else is just Theory' - Josef Sepp Herberger ")
expander.write("An experiment by Darshil Prajapati & Praneeth Ramesh")

#left_column, right_column = st.beta_columns(2)
#pressed = left_column.button('Created By')
#if pressed:
#    right_column.write("Darshil Prajapati & Praneeth Ramesh")
