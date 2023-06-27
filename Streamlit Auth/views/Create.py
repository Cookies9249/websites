import streamlit as st

def load_view():
    st.title("Travel Planner")

    # Input fields
    destination = st.text_input("Enter your destination:")
    start_date = st.date_input("Start date:")
    end_date = st.date_input("End date:")

    # Action button
    st.write("###")
    st.markdown(f'''
    <a target="_self" href="/?nav=trip">
        <button class="css-1anllk4 e1ewe7hr10">
            Plan my trip!
        </button>
    </a>
    ''', unsafe_allow_html=True)

    with open("data/details.csv", "w") as file:
        file.write(f"{destination},{start_date},{end_date}")