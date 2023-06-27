# Imports
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page

import yaml
from yaml.loader import SafeLoader

from views import Create, Map, Home, Trip
from Navigation import initialize_bar

# Configurations
st.set_page_config(page_title="ItineraryAI", page_icon=":book:", layout="wide")

# Run Code
initialize_bar()

# Navigation Bar Code
def navigation():
    # Get Current Route
    try:
        route = st.experimental_get_query_params()['nav'][0]
    except:
        route = None
    
    # Redirect to Page
    if route == None:
        Home.load_view()
    elif route == "map":
        Map.load_view()
    elif route == "create":
        Create.load_view()
    elif route == "trip":
        Trip.load_view()
navigation()

# Change Style
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """ 
st.markdown(hide_style, unsafe_allow_html=True)

