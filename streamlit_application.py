import streamlit as st, pandas as pd
import requests as r
import snowflake.connector

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
#fruityvice_response = r.get("https://fruityvice.com/api/fruit/"+ "kiwi")
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = r.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
st.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
st.text("The fruit load list contains:")
st.text(my_data_row)
