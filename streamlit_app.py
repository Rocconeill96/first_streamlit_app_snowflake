#all libraries 
import streamlit 
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Snowflake streamlit application')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas as pd 
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list goes here. Customer can choose the fruit they want to include 
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display table on page 
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response 
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    fruityvice_response = requests.get('https://fruityvice.com/api/fruit/'+ fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLerror as e:
   streamlit.error()
    
streamlit.header("The fruit load list contains:")
#snowflake functions 
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute('select * from fruit_load_list')
    return my_cur.fetchall()
  
#add button to load fruit 
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return 'Thanks for adding ' + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
   

# #don't run while troubleshooting
streamlit.stop()


#allow end user to add a fruit to the list
streamlit.write('Thanks for adding', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

# import requests
# fruit_added_response = requests.get('https://fruityvice.com/api/fruit/'+ add_my_fruit)
# fruit_added_normalized = pd.json_normalize(fruit_added_response.json())
