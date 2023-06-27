### NOT IN USE ###

import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

def load_view():
    # Text
    st.markdown("# Mapping Demo")
    st.sidebar.header("Mapping Demo")
    st.write(
        """This demo shows how to use
    [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
    to display geospatial data."""
    )

    # Set the location coordinates
    location_lat = 37.7749
    location_lon = -122.4194

    # Create the PyDeck map layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"position": [location_lon, location_lat]}],
        get_position="position",
        get_radius="100 * (1 / pow(2, zoom))",
        pickable=True,
    )

    # Initialize the PyDeck map view and style
    view_state = pdk.ViewState(latitude=location_lat, longitude=location_lon, zoom=11)
    map_style = "mapbox://styles/mapbox/light-v9"

    # Create the PyDeck map
    map = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=map_style)

    # Render the map using Streamlit
    st.pydeck_chart(map)