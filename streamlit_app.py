import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Mom's New Healthy Dinner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avogado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
#new section to show fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
# import requests
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   #  normalize the response
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
# input user fruit choice
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
   else:
      back_from_function=get_fruityvice_data(fruit_choice)
      # put the results on table
      streamlit.dataframe(back_from_function)   
except URLError as e:
   streamlit.error()  
streamlit.write('The user entered ', fruit_choice)






streamlit.header("View Our Fruit List- Add Your Favorites!")
# snowflake related function to get fruit list
def get_fruit_load_list():
   with my_cnx.cursor() as  my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()
   
### add button to load the fruit
if streamlit.button("Get Fruit Load List"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_row = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_row)

# Allow the end user to add a fruit to the list
def insert_raw_snowflake(new_fruit):
   with my_cnx.cursor() as  my_cur:
      my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
      my_cur.close()
      return "Thank you for adding a new fruit "+ new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a Fruit to The List"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_raw_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_function)
# streamlit.write('The user entered ', add_my_fruit)

# streamlit.write('Thank you for adding', add_my_fruit)
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")

