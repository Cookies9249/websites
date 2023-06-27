# pip install streamlit-authenticator
# pip install streamlit pandas openpyxl plotly-express

import streamlit as st
import pandas as pd
import plotly_express as px

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# --- USER AUTH ---

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pp", "rm"]
passwords = ["abc", "123"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# create authenticator
auth = stauth.Authenticate(names, usernames, hashed_passwords, cookie_name="sales_dashedboard", key="abcdef", cookie_expiry_days=30)

# create form
name, auth_status, username = auth.login("Log In", "main")

if auth_status == False:
    st.error("Invalid Username or Password")
if auth_status == None:
    st.warning("Please Enter Username and Password")

# if login successful, run app
if auth_status == True:
    # --- GET DATA ---
    @st.cache_data
    def get_data_from_excel():

        df = pd.read_excel(
            io='supermarkt_sales.xlsx',
            engine='openpyxl',
            sheet_name='Sales',
            skiprows=3,
            usecols='B:R',
            nrows=1000,
        )

        # hour column
        df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
        return df
    df = get_data_from_excel()

    # --- SIDEBAR ---
    # user interaction (auth)
    st.sidebar.title(f"Welcome {name}!")

    st.sidebar.header("Please Filter Here:")

    city = st.sidebar.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique(),
    )

    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique(),
    )

    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique(),
    )

    st.sidebar.markdown("###")
    auth.logout("Log Out", "sidebar")

    df_selection = df.query("City == @city & Customer_type == @customer_type & Gender == @gender")

    # --- MAINPAGE ---
    st.title(":bar_chart: Sales Dashboard")
    st.markdown("##")

    # top KPIs
    total_sales = int(df_selection["Total"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

    left_column, middle_column, right_column = st.columns((2,3,3))

    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"USD $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sale Per Transaction:")
        st.subheader(f"USD $ {average_sale_by_transaction}")

    st.markdown("---")

    # -- BAR CHART 1 ---
    sales_by_product = (
        df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product,
        x="Total",
        y=sales_by_product.index,
        orientation="h",
        title="<b>Sales By Product Line<b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # -- BAR CHART 2 ---
    sales_by_hour = (
        df_selection.groupby(by=["hour"])[["Total"]].sum()
    )
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        title="<b>Sales By Hour<b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    fig_hourly_sales.update_layout(
        xaxis=(dict(tickmode="linear")),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
    )

    # display charts
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
    right_column.plotly_chart(fig_product_sales, use_container_width=True)

    # --- CUSTOM STYLE ---
    hide_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """ 
    st.markdown(hide_style, unsafe_allow_html=True)

    st.dataframe(df_selection)