import streamlit as st
from streamlit.components.v1 import html

def initialize_bar():
    TITLE = "ItineraryAI"
    VIEWS = {"Home":"#",
            "Create":"create",
            "Trip":"trip",
            "Map":"map"}

    # Navigation Bar HTML
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    nav_items = ''
    for item, path in VIEWS.items():
        nav_items += (f'<li class="nav-item active"><a class="nav-link navitem disabled" href="/?nav={path}">{item}</a></li>')

    st.markdown(f"""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #0083B8;">
        <div class="navbar-brand">{TITLE}</div>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                {nav_items}
            </ul>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    # Change JS
    # so using navigation bar doesn't load new page on new tab
    js = '''
    <script>
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }
    </script>
    '''
    html(js)