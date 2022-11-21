import pandas as pd
import requests
from urllib.error import URLError

import streamlit
import snowflake.connector

def get_fruityvice_data(this_fruit_choice):
  streamlit.write('The user entered ', fruit_choice)
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute('select * from pc_rivery_db.public.fruit_load_list')
    return my_cur.fetchall()
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values({fruit_choice})")
    return f"Thanks for adding {new_fruit}"
  
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?')
try:
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.header("The fruit load list contains:")
  streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the List'):            
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_choice)
  my_cnx.close()
  streamlit.text(back_from_function)
