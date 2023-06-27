import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import requests

import pandas as pd

st.set_page_config(page_title="My Website", page_icon=":tada:", layout="wide")

# --- HEADER ---
with st.container():
    # writing text
    st.subheader("Hi, I am Carson :wave:")
    st.title("A High School Student From Canada")
    st.write("""
        This is my first streamlit project. \n
        [Learn More](https://www.google.com) \n
        To change the theme, check https://blog.streamlit.io/introducing-theming/ \n
        """)
    
    # oction menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Projects", "Contact"],
            icons=["house", "book", "envelope"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"  # remove for vertical
        )
    st.title(f"You have selected {selected}")

# --- ASSETS ---
# animation
def load_animation(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_animation = load_animation("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")

# images
img1 = Image.open("images/image1.jpg")
img2 = Image.open("images/image2.jpg")

# CSS 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

# --- WHAT I DO ---
with st.container():
    # add a line
    st.write("---")

    # add columns
    left_column, right_column = st.columns(2)

    with left_column:
        st.header("What I Do")
        st.write("##")
        st.write("""
                This is just a test where I can write:
                 - a lot of information
                 - on seperate lines
                 - in a dotted list
                 - and see whether it shows the seperate
                 - lines on the website.
                 - Thanks for reading!
                 """)
        
    with right_column:
        st_lottie(lottie_animation, height=300, key="coding")
        st.write("This animation was taken from https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
        
# --- PROJECTS ---
with st.container():
    st.write("---")
    st.header("My Projects")
    st.write("##")

    # uneven columns
    image_column, text_column = st.columns((1, 2))

    # images
    with image_column:
        st.image(img1)

    with text_column:
        st.subheader("Integrating Animations Into Your Streamlit App")
        st.write("""
                Learn how to use Lottie files in Streamlit! \n
                For the source of animations, visit https://lottiefiles.com/
                """)
        st.markdown("[Watch this video](https://www.youtube.com/watch?v=VqgUkExPvLY&ab_channel=CodingIsFun)")
    
with st.container():
    image_column, text_column = st.columns((1, 2))

    # images
    with image_column:
        st.image(img2)

    with text_column:
        st.subheader("Integrating Forms Into Streamlit!")
        st.write("""
                Learn how to use Forms in Streamlit! \n
                For the source API, visit https://formsubmit.co/
                """)

# --- CONTACT ---
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # contact form
    contact_form = """
    <form action="https://formsubmit.co/cookieandcroissant@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="Name" placeholder="Your Name" required>
        <input type="email" name="Email" placeholder="Your Email" required>
        <textarea name="Message" placeholder="Your Message" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()