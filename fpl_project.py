import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly_express as px
import matplotlib.pyplot as plt
import seaborn as sns
import time

#page_bg_img = '''
#<style>
#body {
#background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDMJo6h2zgISKQTzhlyAGjkIi8C4VJery5Yg&usqp=CAU");
#background-size: cover;
#}
#</style>
#'''

#st.markdown(page_bg_img, unsafe_allow_html=True)

@st.cache
def get_FPL_data():
    df = pd.read_csv("combined_GW28.csv")
    return df.set_index('FirstName')

st.title('FPL Predicting WebApp')

st.markdown('Choose the teams and positions for which you want to scout players for FPL and click Apply')

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
        df=df[df['Play Probability'] > 0]

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

    fig = px.line(df1, x ='Player',y='Predicted Points')
    st.plotly_chart(fig)

btn = st.sidebar.button("Apply")
if btn:
    run_data()
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
    st.header('Dreamteam in Progress')
    #data = dict(
    #    character=["Dreamteam", "Harry Kane", "Salah", "Mane", "Saka", "Mount", "DeBruyne", "Alexander-Arnold", "Cancelo", "Chillwell", "Dias", "Ederson"],
    #    parent=["", "Forwards", "Forwards", "Forwards", "Midfielder", "Midfielder", "Midfielder", "Defender", "Defender","Defender","Defender","Goalkeeper" ],
    #    value=[10, 14, 12, 10, 2, 6, 6, 4, 4,6,7,8])

    #figs =px.sunburst(
    #    data,
    #    names='character',
    #    parents='parent',
    #    values='value',
    #)
    #st.plotly_chart(figs)

#expander = st.beta_expander("FAQ")
#expander.write("To be Filled in Due Time")

#left_column, right_column = st.beta_columns(2)
#pressed = left_column.button('Created By')
#if pressed:
#    right_column.write("Darshil Prajapati & Praneeth Ramesh")
