import streamlit 

streamlit.title('Snowflake streamlit application')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd 
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list goes here. Customer can choose the fruit they want to include 
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display table on page 
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response 

import requests
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
streamlit.text(fruityvice_response)

#display fruityvice api response 
streamlit.header('Fruityvice Fruit Advice!')
streamlit.text(fruityvice_response.json()) #writes data to screen

#take the json version of the of the response and normalize 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

#table out put
streamlit.dataframe(fruityvice_normalized)


