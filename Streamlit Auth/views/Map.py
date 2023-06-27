import streamlit as st
import pydeck as pdk
from util import csv_to_json
import pandas as pd

def load_view():
    csv_file_path = 'data/plan.csv'
    json_file_path = 'data/plan.json'

    # Obtain a .json file from .csv file
    csv_to_json(csv_file_path, json_file_path)

    # Load the location data from the JSON file
    with open(json_file_path, 'r') as json_file:
        data = pd.read_json(json_file)

    # Custom text layer for dot rendering
    layers = [pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["Long", "Lat"],
        get_radius=50,
        get_fill_color=[255, 0, 0],
        pickable=True,
        auto_highlight=True,
        id="scatterplot-layer",
    ), pdk.Layer(
        "TextLayer",
        data=data,
        get_position=["Long", "Lat"],
        get_text="Name",
        get_color=[0, 0, 0, 200],
        get_size=15,
        get_alignment_baseline="'bottom'",
    )]

    # PyDeck map
    view_state = pdk.ViewState(latitude=43.672161, longitude=-79.322981, zoom=11)
    map_style = "mapbox://styles/mapbox/light-v9"
    map = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style=map_style
    )

    # Render the map using Streamlit
    st.pydeck_chart(map)