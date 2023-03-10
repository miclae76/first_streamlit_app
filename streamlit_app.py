import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Mica\'s new Healthy diner')
streamlit.header('Breakfast Favorites')

streamlit.text('π₯£ Omega 3 & Blueberry Oatmeal')
streamlit.text('π₯ Kale, Spinach & Rocket Smoothie')
streamlit.text('πHard-Boiled Free-Range Egg')
streamlit.text('π₯ Avocado Toast')

streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# create picklist
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_date(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice: 
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_date(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
        streamlit.error()

#import snowflake.connector

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:  
         my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
         return my_cur.fetchall()
    
#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
#allow the user to add a fruit in the lits

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('" + add_my_fruit + "')")
        return "Thanks for adding "+ new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'): 
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_fucntion = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
        streamlit.text(back_from_function)

