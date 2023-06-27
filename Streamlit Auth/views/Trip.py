import streamlit as st
import pandas as pd
import csv
from datetime import datetime, timedelta

def load_view():
    # ----- GENERATE PLAN -----
    # Read trip details
    with open('data/details.csv') as file:
        data = list(csv.reader(file, delimiter=","))
    
    # If no plan has been made yet
    if data == []:
        st.error("Please Create a Trip First")
        return
    
    # Initialize Variables
    destination = data[0][0]
    start_date = datetime.date(datetime.strptime(data[0][1], '%Y-%m-%d'))
    end_date = datetime.date(datetime.strptime(data[0][2], '%Y-%m-%d'))

    # Replace with ChatGPT API
    reponse = """Datetime,Name,Address,Cost,Rating,Lat,Long
2023-06-23 08:00,Breakfast at Maha's,226 Greenwood Ave,15.00,4.5,43.672161,-79.322981
2023-06-23 10:00,Royal Ontario Museum,100 Queen's Park,25.00,4.7,43.667713,-79.394777
2023-06-23 13:00,Lunch at Pai Northern Thai Kitchen,18 Duncan St,20.00,4.6,43.647785,-79.388791
2023-06-23 15:00,CN Tower,290 Bremner Blvd,35.00,4.7,43.642566,-79.387057
2023-06-23 18:00,Dinner at Richmond Station,1 Richmond St W,45.00,4.5,43.651994,-79.379910
2023-06-24 08:00,Breakfast at Lady Marmalade,898 Queen St E,20.00,4.6,43.659606,-79.348270
2023-06-24 10:00,Ripley's Aquarium of Canada,288 Bremner Blvd,35.00,4.5,43.642403,-79.386614
2023-06-24 13:00,Lunch at Banjara Indian Cuisine,796 Bloor St W,15.00,4.4,43.662896,-79.420421
2023-06-24 15:00,Art Gallery of Ontario,317 Dundas St W,30.00,4.7,43.653607,-79.392385
2023-06-24 18:00,Dinner at Canoe Restaurant,66 Wellington St W,60.00,4.6,43.647049,-79.381826
2023-06-25 08:00,Breakfast at Saving Grace,907 Dundas St W,15.00,4.6,43.651542,-79.413922
2023-06-25 10:00,Toronto Islands,9 Queens Quay W,14.00,4.8,43.632025,-79.376055
2023-06-25 13:00,Lunch at Kinka Izakaya Original,398 Church St,25.00,4.6,43.661747,-79.378120
2023-06-25 15:00,St. Lawrence Market,93 Front St E,0,4.7,43.648662,-79.371116
2023-06-25 18:00,Dinner at The Chase,10 Temperance St,55.00,4.5,43.649563,-79.378672
"""

    # Write conversation into csv file
    with open("data/plan.csv", "w") as file:
        file.write(reponse)

    # Convert csv file to pandas df
    data = pd.read_csv('data/plan.csv')
    df = pd.DataFrame(data)

    # ----- TRIP DETAILS -----

    # Display the trip plan
    st.title("Your Trip Plan")
    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader("Destination:")
        st.subheader(destination)
    with middle_column:
        st.subheader("Start date:")
        st.subheader(start_date.strftime('%B %d, %Y'))
    with right_column:
        st.subheader("End date:\n")
        st.subheader(end_date.strftime('%B %d, %Y'))

    # ----- STATS -----

    # Create Columns
    st.title("Your Trip Stats")
    left_column, middle_column, right_column = st.columns(3)

    # Total Days
    with left_column:
        st.subheader("Total Time:")

        time = (end_date - start_date + timedelta(days=1)).days
        days_rating = ":earth_americas:" * time
        st.subheader(f"{time} Days {days_rating}")

    # Total Cost
    with middle_column:
        st.subheader("Total Cost:")

        cost = int(df["Cost"].sum())
        cost_rating = ":dollar:" * int(round(cost/100, 0))
        st.subheader(f"USD $ {cost} {cost_rating}")
    
    # Average Rating
    with right_column:
        st.subheader("Average Rating:")

        star = round(df["Rating"].mean(), 1)
        star_rating = ":star:" * int(round(star, 0))
        st.subheader(f"{star} {star_rating}")

    # ----- SCHEDULE -----

    # Index through df
    st.title("Schedule")
    rows = df.shape[0]
    index_date = start_date - timedelta(days=1)

    df_new = pd.DataFrame()

    for r in range(rows):
        # Compare index_date with date of event
        dt = datetime.strptime(df["Datetime"][r], '%Y-%m-%d %H:%M')

        # If new day, print day
        if not datetime.date(dt) == index_date:
            index_date += timedelta(days=1)
            st.subheader(index_date.strftime('%B %d, %Y'))
        
        # print activity name
        st.write(df["Name"][r])
    
    # Use Dataframe to print
    st.dataframe(df)