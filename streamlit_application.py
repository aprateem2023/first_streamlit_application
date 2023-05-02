import streamlit as st, pandas as pd
import requests as r
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = r.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
        # write your own comment -what does the next line do? 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
    return fruityvice_normalized

def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return 'Thanks for adding '+ add_my_fruit

st.title("My Parents New Healthy Diner")
st.header("Breakfast Favourites")
st.text("🥣 Omega 3 and Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Avocado Toast")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

if len(fruits_selected) != 0 :
    st.dataframe(fruits_to_show)

else :
    st.dataframe(my_fruit_list)
    

st.header("Fruityvice Fruit Advice!")

try :
    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else :
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()

st.header("View Our Fruit List - Add Your Favorites!")
if st.button("Get Fruit List"):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
    my_data_rows = get_fruit_load_list(my_cnx)
    fr_t_s = my_data_rows.loc['jackfruit']
    st.dataframe(fr_t_s)
    my_cnx.close()
    st.dataframe(my_data_rows)
    
st.stop()
add_my_fruit = st.text_input('What fruit would you like to add?')
if not add_my_fruit:
    st.error("Please add a fruit name.")
else :
    if st.button("Add a Fruit to the List"):
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    
        back_from_function = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
        st.text(back_from_function)
    
