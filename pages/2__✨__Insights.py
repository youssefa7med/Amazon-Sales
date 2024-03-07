import streamlit as st
import pandas as pd
import numpy  as np
import plotly.express as px

import json
import requests
from streamlit_lottie import st_lottie


st.set_page_config(layout="wide")

st.markdown('<h1 style="text-align: center; color: #D8DACC; font-size: 40px; font-weight: bold;">Insights</h1>', unsafe_allow_html=True)


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
column1,column2,column3 = st.columns([2,4,1])
fig1 = px.bar(df['age_category'].value_counts().reset_index()
        ,x='index',y='age_category',template='presentation',color='age_category'
        ,text_auto=True,color_discrete_sequence=px.colors.sequential.RdBu
        ,title='The number of orders in each age category')
fig1.update_layout(showlegend=False)
fig1.update_traces(marker_line_color='black', marker_line_width=1)
column2.plotly_chart(fig1,use_container_width=True)
column2.write('The Age Categories Range From 18-20 To 70-75 is lower Than The Rest')

# -----------------------------------------------------------


# st.divider()

# fig2 = px.bar(df.groupby('category')['price'].mean().reset_index().sort_values(by = 'price',ascending = False).round(2)
#         , x='price',y = 'category',color = 'category',text_auto = True,template='presentation'
#         ,title = 'The mean price per each category')

# st.plotly_chart(fig2)
# st.write('''* Mobiles & Tablets Have The Highest Mean Total For Orders Because That Already Is The Most Expensive Product .''')
# st.write('''* Books Have The Lowest Mean Total For Orders Because That Is The Least Expensive Product .''')

# -----------------------------------------------------------
st.divider()

col1,col2 = st.columns(2)

fig3 = (px.bar(df[df['order_year'] == 2020].groupby('category')['total'].sum().reset_index().sort_values(by = 'total',ascending = False).round(2)
    , x='total',y = 'category',template='presentation'
    ,color = 'category',text_auto = True
    ,title = f'The sum total per each category in {2020}'))
fig3.update_layout(showlegend=False)
fig3.update_traces(marker_line_color='black', marker_line_width=1)
col1.plotly_chart(fig3,use_container_width=True)

fig4 = (px.bar(df[df['order_year'] == 2021].groupby('category')['total'].sum().reset_index().sort_values(by = 'total',ascending = False).round(2)
    , x='total',y = 'category',template='presentation'
    ,color = 'category',text_auto = True
    ,title = f'The sum total per each category in {2021}'))
fig4.update_layout(showlegend=False)
fig4.update_traces(marker_line_color='black', marker_line_width=1)
col2.plotly_chart(fig4,use_container_width=True)


col1.write('''* Entertainment Have High Sum Of Total For Orders In 2020 Because of High Demand On Entertainment Because Of The Coronavirus Pandemic And The Most People Are In There Home .''')
col2.write("""* Mobiles & Tablets Have The Highest Sum Total For Orders In 2021 Because Of The Most Companies Produce These Products Stopped Publishing New Products Throughout 2020 Because Of The Coronavirus Pandemic And That Made The Demand Lower .""")

col1.subheader('- The Percentage Of Entertainment Orders In 2020 Was '+str(round(df[(df['category'] == 'Entertainment') & (df['order_year'] == 2020)]['total'].sum() / df[df['order_year'] == 2020]['total'].sum()*100,2))+'%')
col2.subheader('- The Percentage Of Entertainment Orders In 2021 Was '+str(round(df[(df['category'] == 'Entertainment') & (df['order_year'] == 2021)]['total'].sum() / df[df['order_year'] == 2021]['total'].sum()*100,2))+'%')

# -------------------------------------------------------
st.divider()

column1,column2,column3 = st.columns([1,4,1])


fig = px.bar(df_complete.groupby('county')['total'].sum().reset_index().sort_values(by = 'total',ascending = False).round(2).nlargest(10,'total')
        ,x='total',y = 'county',text_auto=True,color='county',color_discrete_sequence=px.colors.sequential.RdBu
        ,template='presentation',title='Top 10 Counties In Total Of Orders',labels={'order_id':'Count','county':'County'})

fig.update_layout(showlegend=False)
fig.update_traces(marker_line_color='black', marker_line_width=1)
column2.plotly_chart(fig,use_container_width=True)
column2.write('- The County Of Los Angeles Has The Highest Total Of Orders')
column2.subheader('- Los Angeles Is Considered One Of The Most Expensive Cities In the World And Has The Highest Standard Of Living In The World.')

# -----------------------------------------------------------
st.divider()

column1,column2,column3 = st.columns([1,4,1])

fig = px.bar(df.groupby('county')['order_id'].count().sort_values(ascending=False).reset_index().nlargest(10,'order_id')
        ,x='order_id',y = 'county',text_auto=True,color='county',color_discrete_sequence=px.colors.sequential.RdBu
        ,template='presentation',title='Top 10 Counties In Total Count Of Orders',labels={'order_id':'Count','county':'County'})
fig.update_layout(showlegend=False)
fig.update_traces(marker_line_color='black', marker_line_width=1)
column2.plotly_chart(fig,use_container_width=True)
column2.subheader('- The County Of Jefferson Has The Highest Count Of Orders')

col1,col2 = st.columns(2)

fig = px.bar(df_complete.groupby('county')['order_id'].count().sort_values(ascending=False).reset_index().nlargest(10,'order_id')
        ,x='order_id',y = 'county',text_auto=True,color='county',color_discrete_sequence=px.colors.sequential.RdBu
        ,template='presentation',title='Top 10 Counties In Completed Orders',labels={'order_id':'Count','county':'County'})
fig.update_layout(showlegend=False)
fig.update_traces(marker_line_color='black', marker_line_width=1)
col1.plotly_chart(fig,use_container_width=True)
col1.subheader('- DaKalb '+str(round(df[(df['county'] == 'DeKalb') & (df['status'] == 'complete')]['order_id'].count() / df[df['county'] == 'DeKalb']['order_id'].count()*100,2))+'%'+' Completed Orders')
col1.subheader('- Los Angeles '+str(round(df[(df['county'] == 'Los Angeles') & (df['status'] == 'complete')]['order_id'].count() / df[df['county'] == 'Los Angeles']['order_id'].count()*100,2))+'%'+' Completed Orders')
col1.subheader('- Jefferson '+str(round(df[(df['county'] == 'Jefferson') & (df['status'] == 'complete')]['order_id'].count() / df[df['county'] == 'Jefferson']['order_id'].count()*100,2))+'%'+' Completed Orders')


fig = px.bar(df_canceled.groupby('county')['order_id'].count().sort_values(ascending=False).reset_index().nlargest(10,'order_id')
        ,x='order_id',y = 'county',text_auto=True,color='county',color_discrete_sequence=px.colors.sequential.RdBu
        ,template='presentation',title='Top 10 Counties In Canceled Orders',labels={'order_id':'Count','county':'County'})
fig.update_layout(showlegend=False)
fig.update_traces(marker_line_color='black', marker_line_width=1)
col2.plotly_chart(fig,use_container_width=True)
col2.subheader('- Jefferson '+str(round(df[(df['county'] == 'Jefferson') & (df['status'] == 'canceled')]['order_id'].count() / df[df['county'] == 'Jefferson']['order_id'].count()*100,2))+'%'+' Canceled Orders')
col2.subheader('- Los Angeles '+str(round(df[(df['county'] == 'Los Angeles') & (df['status'] == 'canceled')]['order_id'].count() / df[df['county'] == 'Los Angeles']['order_id'].count()*100,2))+'%'+' Canceled Orders')
col2.subheader('- DeKalb '+str(round(df[(df['county'] == 'DeKalb') & (df['status'] == 'canceled')]['order_id'].count() / df[df['county'] == 'DeKalb']['order_id'].count()*100,2))+'%'+' Canceled Orders')

# -----------------------------------------------------------
st.divider()
col,column_use,col = st.columns([1,2,1])
column_use.header('- Solution To Reduce Cancellations -')


col1,col2 = st.columns(2)
fig= px.sunburst(df.groupby(['gender','status'])['order_id'].count().reset_index()
        ,path=['gender','status'],values='order_id',template='simple_white'
        ,color_discrete_sequence=px.colors.sequential.RdBu,title='The Number Of Orders Per Each Gender & Status').update_traces(textinfo='label+percent parent')
fig.update_layout(showlegend=False)
col1.plotly_chart(fig,use_container_width=True)

fig = px.sunburst(df[df['discount_percent']>0].groupby(['gender','status'])['order_id'].count().reset_index()
        ,path=['gender','status'],values='order_id',template='simple_white'
        ,color_discrete_sequence=px.colors.sequential.RdBu,title='The Number Of Orders Per Each Gender & Status With Discount').update_traces(textinfo='label+percent parent')
fig.update_layout(showlegend=False)
col2.plotly_chart(fig,use_container_width=True)

col,column_use,col = st.columns([1,2,1])
column_use.header('Make More Discounts In Holidays')
# -----------------------------------------------------------
st.divider()

column1,column2,column3 = st.columns([1,4,1])

fig = px.pie(df.groupby('holiday')['total'].mean().round(2).reset_index()
        ,values='total',names='holiday',template='presentation'
        ,title='The mean total per holiday').update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)
fig.update_traces(marker_line_color='black', marker_line_width=1)
column2.plotly_chart(fig,use_container_width=True)
st.subheader('- 50.2% Of Total Mean Orders Are On Holidays Although The Holidays Are Two Days Only .')
st.subheader('- That Means You Can Make More Profit In Holidays Because You Can Sell More Than The Rest Of The Week .')

# -----------------------------------------------------------
# st.divider()

# column1,column2,column3 = st.columns([1,4,1])

# fig=px.bar(df.groupby(['payment_method','gender'])['total'].mean().reset_index().round(2)
#         ,x='payment_method',y='total',color='gender',barmode='group'
#         ,text_auto=True,template='presentation',title='The mean total per each payment method & gender')

# column2.plotly_chart(fig)
# st.subheader('- All Payment Methods Have The Similar Mean But Finance Settlement Method has The Highest Mean Total For Females Because The Registration Steps Are More Complex And Men Get Bored .')

# -----------------------------------------------------------
st.divider()






