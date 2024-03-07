import streamlit as st
import pandas as pd
import numpy  as np
import plotly.express as px

import json
import requests
from streamlit_lottie import st_lottie


st.markdown('<h1 style="text-align: center; color: #D8DACC; font-size: 40px; font-weight: bold;">Sales Analysis</h1>', unsafe_allow_html=True)



def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

animation = load_lottieurl('https://lottie.host/96ab8a4c-8d9a-4067-a71f-42cd66946106/yqNMxJCNx2.json')
st_lottie(animation,speed = .6,quality = 'high',width = 700,height = 500)

df= pd.read_csv("amazon_data.csv")
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = pd.to_datetime(df['order_date']).dt.month
df['order_month_name'] = pd.to_datetime(df['order_date']).dt.month_name()
df['order_day'] = pd.to_datetime(df['order_date']).dt.day
df['order_year'] = pd.to_datetime(df['order_date']).dt.year
df['order_day_name'] = pd.to_datetime(df['order_date']).dt.day_name()
df['holiday'] = df['order_day_name'].apply(lambda x: 1 if x in ['Sunday', 'Saturday'] else 0)
df['year_quarter'] = pd.to_datetime(df['order_date']).dt.quarter
df.drop(columns=['year','month'],axis=1, inplace=True)
df['age_category'] = pd.cut(df['age'], bins=[df['age'].min(), 20, 30, 40, 50, 60, 70, df['age'].max()], labels=['18-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-75'])
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df['holiday'] = df['holiday'].apply(lambda x: 'Yes' if x == 1 else 'No')
df['status'] = df['status'].apply(lambda x: 'canceled' if x in['canceled', 'refund', 'closed', 'order_refunded'] else 'complete')
df_complete = df[df['status']=='complete']
df_canceled = df[df['status']=='canceled']
df['holiday'] = df['order_day_name'].apply(lambda x: 1 if x in ['Sunday', 'Saturday'] else 0)
df['holiday'] = df['holiday'].apply(lambda x: 'Holiday' if x == 1 else 'Workday')

# -----------------------------------------------------------
st.divider()

selected = st.selectbox('Select Date Type to filter by :',['order_month_name','order_day_name','year_quarter','order_year','order_day'])

df_selected = df[selected].value_counts().reset_index()

fig1 = px.pie(df_selected
    ,values=selected,names='index',template='simple_white',color_discrete_sequence=px.colors.sequential.RdBu
    ,title=f'The number of orders in each {selected}',hole=0.3)
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(showlegend=False)
fig1.update_traces(marker_line_color='black', marker_line_width=1)
st.plotly_chart(fig1)

largest = df_selected.nlargest(1,selected)['index'][0]

st.write(f'* The Most Popular {selected} For Orders Is {largest}')

# -----------------------------------------------------------
st.divider()

selected = st.selectbox('Select Column To Filter By :',['county', 'city', 'state', 'region'])
time = st.radio('Select Time Range :',('All',2020,2021),horizontal=True)
if time == 'All':
    fig= px.bar(df[selected].value_counts().reset_index().nlargest(10,selected),y='index',x=selected,template='simple_white',color_discrete_sequence=px.colors.sequential.RdBu
            ,text_auto = True,color = 'index',title=f'Top 10 {selected} In Total Count Of Orders',labels={'index':selected,selected:'Count'})
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig)
    st.subheader(f'- The Most Popular {selected} In Count Of Orders Is '+df[selected].value_counts().reset_index().nlargest(1,selected)['index'][0]+' All Time .')
else:
    fig= px.bar(df[df['order_year'] == time][selected].value_counts().reset_index().nlargest(10,selected),y='index',x=selected,template='simple_white',color_discrete_sequence=px.colors.sequential.RdBu
            ,text_auto = True,color = 'index',title=f'Top 10 {selected} In Total Count Of Orders In {time}',labels={'index':selected,selected:'Count'})
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig)
    st.subheader(f'- The Most Popular {selected} In Count Of Orders Is '+df[df['order_year'] == time][selected].value_counts().reset_index().nlargest(1,selected)['index'][0]+f' In {time} .')

# -----------------------------------------------------------
st.divider()

column1,column2 = st.columns(2)

cat = column1.selectbox('Select Category To Filter By :',df['category'].unique())
time_type = column2.selectbox('Select Time Range :',['order_month',  'order_day',  'year_quarter','order_year'])
year = column1.radio('Select Year :',['All',2020,2021],horizontal=True)

if year == 'All':
    fig=px.line(df[df['category'] == cat].groupby(time_type)['total'].mean().reset_index()
            ,x=time_type,y='total'
            ,template='simple_white',color_discrete_sequence=px.colors.sequential.RdBu
            ,title='The Mean Total For '+ cat +' Orders In Each '+time_type,markers=True)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    column1.plotly_chart(fig)

else:
    fig=px.line(df[(df['category'] == cat) & (df['order_year'] == year)].groupby(time_type)['total'].mean().reset_index()
            ,x=time_type,y='total'
            ,template='simple_white',color_discrete_sequence=px.colors.sequential.RdBu
            ,title='The Mean Total For '+ cat +' Orders In Each '+time_type+f' In {year}',markers=True)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    column1.plotly_chart(fig)
