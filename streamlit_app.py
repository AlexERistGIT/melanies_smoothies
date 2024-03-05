# Import python packages
import streamlit as st
import pandas as pd
# GILT NICHT FÜR Streamlit Ausserhalb Snowflake: (SnIS): from snowflake.snowpark.context import get_active_session
# "Focus" on Column
from snowflake.snowpark.functions import col
import requests


########################################################################################
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom Smoothie!
    \n**(https://docs.streamlit.io).
    \n*** https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
    """
)



########################################################################################Name Box
title= st.text_input(label="Movie title", 
                         value="Life of Brien", 
                         max_chars=100, 
                         key=None, 
                         type="default", 
                         help=None, 
                         autocomplete=None, 
                         on_change=None, 
                         args=None, 
                         kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
st.write("The current movie title is: ",title)


########################################################################################Name Box2
name_on_order= st.text_input(label="Name on smoothie:")
st.write("The name of your smoothie will be: ",name_on_order)

########################################################################################
# Dataframe im App "auflisten", Eine Spalte selektieren: index ist automatisch da :) die Schlange ! ;)  
# NCIHT FÜR STREAMLET SnIS: session = get_active_session()
## nur für Streamlit Ausserhalb Snowflake: (SnIS)
cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#Im Streamapp darstellen ? Das hier einckommentieren: 
# DEBUG st.dataframe(data=my_dataframe, use_container_width=True)
# DEBUG st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function 
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


# Spalte jetzt nutzen: "max_selection=5" begrenzt maximale Anzahl auf 5... cheers :) 
ingredients_list=st.multiselect('Choose up to 5 ingredients:',
                                my_dataframe,
                                max_selections=5)

# Our ingredients variable is an object or data type called a LIST
#  Wenn Liste nicht leer ist then do everything below this line that is indented.
ingredients_string = '' # variable für text
if ingredients_list:  
    # st.write('You selection is:', incredients_list)
    # oder 
    # st.text(f'Your selection is:' + f'{incredients_list}') 
    # or for each_fruit in ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        ############################Ingrediente darstellen
        # Ohne Filter: alles: fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        st.subheader(fruit_chosen+' Nutrition Information')
        ### response Filtern
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        # st.text(fruityvice_response.json()) # json response zurückgeben als Text
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True) # json response als dataframe zurückgeben
    # st.write('You selection is:', ingredients_string)

    # liste in die Tabelle schreiben
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #DEBUG:  st.write(my_insert_stmt);     st.stop();
    
    # Submit Button einbauen 
    time_to_insert = st.button('Submit Order') 
    
    # Wenn ingredients_string nicht leer ist: SQL ausführen, "Goody" posten ;)
    # Alte Variante: "if ingredients_string:": bei jedem neuen Fruit wurde neue Zeile erzeugt. Jetzt wird nur nach Submit passieren: 
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(body='Your Smoothie is ordered "'+ name_on_order + '"!', icon="✅")
        





######################################################################################## Trash
#L1 gelöscht: option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana', 'Strawberries', 'Peaches'))
#
#st.write('You favorite fruit is:', option)

# Dataframe im App "auflisten" 
#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)

# Aus Streamlit Dokumentation 
# To initialize an empty selectbox, use None as the index value:
# braucht man nicht noch einmal import streamlit as st
# funktioniert nicht mit leerem Auswahl: "placeholder"-Option wird nicht unterstützt? Fehlermeldung. 
#option2 = st.selectbox(   "How would you like to be contacted?",
#   ("Email", "Home phone", "Mobile phone"),
#   index=None, 
#   placeholder="Select contact method...",
#)
#
#st.write('You selected:', option2)
