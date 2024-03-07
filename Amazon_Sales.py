import streamlit as st
import pandas as pd
import numpy  as np
import plotly.express as px

import json
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.dataframe_explorer import dataframe_explorer

st.set_page_config(page_title="Amazon Sales",initial_sidebar_state = 'expanded',page_icon = '🛒')

st.markdown('<h1 style="text-align: center; color: #D8DACC; font-size: 40px; font-weight: bold;">Amazon Sales Analysis</h1>', unsafe_allow_html=True)

df= pd.read_csv("amazon_data.csv")

def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

animation = load_lottieurl('https://lottie.host/1aa2e56a-2b49-4a92-b3f1-e584cd31c1fe/0s0gvbrnBS.json')

st_lottie(animation,speed = .95,quality = 'high',width = 700,height = 500)

tab1,tab2 = st.tabs(["Overview","Dataset"])
with tab1:
    st.markdown('''
    <h3 style="text-align: left; font-size: 20px; font-weight: bold;">Analyzing the dataset provided, which contains information on Amazon sales, customer details, and order specifics, offers a comprehensive opportunity to derive valuable insights and make informed decisions. By conducting a thorough dataset analysis, we can uncover trends, patterns, and correlations that can be beneficial for optimizing business strategies, improving customer experiences, and enhancing overall operational efficiency.

    ###### Sales Analysis:
    * Total Sales: Calculating the total sales revenue over different time periods (daily, monthly, yearly) can provide insights into the business's overall performance.
    * Category Analysis: Analyzing sales by category can help identify the most popular product categories and tailor marketing strategies accordingly.
    * Discount Analysis: Understanding the impact of discounts on sales volume and revenue can guide pricing strategies.
    * Payment Method Analysis: Examining payment method preferences can optimize payment processing and identify areas for improvement.
    ###### Customer Analysis:
    * Customer Demographics: Analyzing customer demographics such as age, gender, location can help in targeted marketing efforts.
    Customer Behavior: Studying customer behavior like purchase frequency, average order value can improve customer retention strategies.
    * Customer Segmentation: Segmenting customers based on their buying patterns can personalize marketing campaigns and enhance customer satisfaction.
    ###### Order Analysis:
    * Order Processing Time: Analyzing the time taken to process orders can streamline operations and improve efficiency.
    * Order Status Analysis: Monitoring order statuses can identify bottlenecks in the supply chain and improve customer service.
    * SKU Analysis: Understanding the popularity of different SKUs can optimize inventory management and forecasting.
    ###### Customer Experience:
    * Communication Channels: Analyzing preferred communication channels (email, phone) can enhance customer service interactions.
    * Sign-up Date Analysis: Studying sign-up dates can help understand customer acquisition trends and optimize marketing campaigns.
    * Region Analysis: Understanding customer distribution across regions can guide expansion strategies and localized marketing efforts.

    ''', unsafe_allow_html=True)

with tab2:
    st.markdown(''' ### The dataset contains detailed information about orders and customers, including the following key fields:
    * Order_id: A unique identifier for each order placed.
    * Order_date: The date and time when the order was placed.
    * Status: The current status of the order (e.g., processing, shipped, delivered).
    * Item_id: Unique identifier for each item in the order.
    * Sku: Stock Keeping Unit, a unique code assigned to each distinct product for inventory management.
    * Qty_ordered: The quantity of the specific item ordered.
    * Price: The price per unit of the item.
    * Value: The total value of the item in the order (price * quantity).
    * Discount_amount: The amount of discount applied to the item.
    * Total: The total cost of the item after discount.
    * Category: The category to which the item belongs (e.g., electronics, clothing, groceries).
    * Payment_method: The method used for payment (e.g., credit card, PayPal, cash on delivery).
    * Bi_st: Business Intelligence status, indicating whether the order data has been processed for analytics.
    * Cust_id: Unique identifier for each customer.
    * Year: The year when the order was placed.
    * Month: The month when the order was placed.
    * Ref_num: Reference number associated with the order.
    * Name Prefix: Prefix added before a person's name (e.g., Mr., Mrs., Dr.).
    * First Name: The first name of the customer.
    * Middle Initial: The middle initial of the customer's name.
    * Last Name: The last name of the customer.
    * Gender: The gender of the customer.
    * Age: The age of the customer.
    * Full_name: The full name of the customer (concatenation of first name, middle initial, and last name).
    * E Mail: The email address of the customer.
    * Sign In Date: The date when the customer signed up or created an account.
    * Phone No.: The phone number of the customer.
    * Place Name: The name of the place associated with the customer (e.g., residence city).
    * County: The county where the customer resides.
    * City: The city where the customer resides.
    * State: The state where the customer resides.
    * Zip: The ZIP or postal code of the customer's location.
    * Region: The region where the customer resides.
    * User Name: The username associated with the customer's account.
    * Discount_percent: The percentage of discount applied to the order.

    \n
    #### Data source for this URL: [Kaggle Dataset](https://www.kaggle.com/datasets/earthfromtop/amazon-sales-fy202021/data)
    ''')

    if st.button('Show Sample Data') :
        st.dataframe(df.sample(10),use_container_width=True)

