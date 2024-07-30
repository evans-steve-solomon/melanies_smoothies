#Import python packages
import streamlit as st
#import pandas as pd
#import snowflake.connector
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx =st.connection("Snowflake")
session =cnx.session()

'''conn = snowflake.connector.connect(
    user = 'evanssteve16',
    password = 'Learn@1308',
    account = 'ZMHFBCH.ABB08608',
    warehouse = 'COMPUTE_WH',
    database = 'SMOOTHIES',
    schema = 'PUBLIC'
)

cur = conn.cursor()

cur.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
rows = cur.fetchall()
'''

# Convert the results to a Pandas DataFrame
fruit_options_df = pd.DataFrame(rows, columns=['FRUIT_NAME'])

# Convert the 'FRUIT_NAME' column to a list
fruit_options = fruit_options_df['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',fruit_options,max_selections=5)
if ingredients_list:

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)values ('""" + ingredients_string + """','"""+ name_on_order+"""')"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!,'+name_on_order,icon="✅")

# Close the cursor and connection
cur.close()
conn.close()
