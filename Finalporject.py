"""
Class: CS230--Section 2 
Name: Aaron Sousa
Description: Below is a Website on all college football stadium data. It covers information on stadium sizes, years built, and many our facts about each stadium.
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px

#Opening the data into from an excel format
excel_file = "stadiums-geocoded.xlsx"
sheet_name = "in"
df = pd.read_excel(excel_file,
                       sheet_name=sheet_name,
                       usecols='A:K',
                       header=3)

#functions
def filter_by_conference_age(df):

    #Streamlit selection
    conference = df["Conference"].unique().tolist()
    ages = df["Built"].unique().tolist()
    age_selection = st.slider("Built:", min_value=min(ages),
                                        max_value=max(ages),
                                        value=(min(ages), max(ages)))

    conference_selection = st.multiselect('Conference:', conference, default=conference)

    #filter data frame based on selection (shows how many results there are)
    mask = (df['Built'].between(*age_selection)) & (df["Conference"].isin(conference_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'Available results: {number_of_result}')

    #Group Dataframe after selection
    df_grouped = df[mask].groupby(by=["Conference"]).count()[['Built']]
    df_grouped = df_grouped.rename(columns={"Built": "Amount of Stadiums"})
    df_grouped = df_grouped.reset_index()

    return df_grouped

#function to create new data frame for largest stadiums
def largest_capacity_stadiums(df, n=5):
    top_n = df.sort_values(by='Capacity', ascending=False).head(n)

    # Extract the stadium names and capacities
    names = top_n['Stadium'].tolist()
    capacities = top_n['Capacity'].tolist()
    largest_stadiums = pd.DataFrame({'Stadium': names, 'Capacity': capacities})

    # Create a new DataFrame with the names and capacities and return it
    return largest_stadiums

#function for smallest stadiums
def smallest_capacity_stadiums(df, n=5):
    bottom_n = df.sort_values(by='Capacity', ascending=True).head(n)

    # Extract the stadium names and capacities
    names = bottom_n['Stadium'].tolist()
    capacities = bottom_n['Capacity'].tolist()
    smallest_stadiums = pd.DataFrame({'Stadium': names, 'Capacity': capacities})

    # Create a new DataFrame with the names and capacities and return it
    return smallest_stadiums

#function to insert lottieurls into my webpage
def loadlottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


#Moving animations
lottie_stadium = loadlottieurl("https://assets5.lottiefiles.com/private_files/lf30_muej992g.json")
lottie_football= loadlottieurl("https://assets9.lottiefiles.com/packages/lf20_n918Sz.json")


#Page configuration
st.set_page_config(page_title="Stadiums Accross the US!", page_icon=":tada:", layout = "wide")
st.markdown("<h1 style='text-align: center; color: White; font-size: 70px;'>Stadiums Accross the US!</h1>", unsafe_allow_html=True)
st.write(
         """\n\nIn this webpage we are going to analyze all the college football stadiums in the United States in different ways:
            \n\t- We will be able to look at the stadiums on a map
            \n\t- We will look at a chart of the 10 biggest stadiums
            \n\t- We will look at a chart of the 10 smallest stadiums
            \n\t- And there will be a scatter plot of the the stadiums by size to get a better understanding of the data"""

         )


#Header Section
with st.container():
    st.subheader("Welcome to the hub of all College Football Stadiums in the US! :wave:")
    st.write("If you want to learn more about other stadiums around the world [click here >](https://olympics.com/en/news/largest-stadium-world-venue-capacity-spectator-seats)")

#Map Section
with st.container():
    st.write("---")
    st.markdown(
        "<h1 style='text-align: center; color: White;'>Below is an Interactive Map of All the College Football Stadiums in The United States!</h1>",
        unsafe_allow_html=True)
    #map
    fig = px.scatter_mapbox(df,
                            lon=df['Longitude'],
                            lat=df['Latitude'],
                            zoom= 3,
                            color=df["Stadium"],
                            size=df['Capacity'],
                            width=1800,
                            height=900,
                            title="Stadium Scatter map"
                        )
    fig.update_layout(mapbox_style= "open-street-map")
    st.plotly_chart(fig)

#Filter bar chart for how many stadiums are in each conference, also filter by year made
with st.container():
     st.write("---")
     left_column, right_column = st.columns(2)
     with left_column:
         st.header("In the left Column is a Bar Chart that Shows how many stadiums are in each conference of College football. It can be filtered by Conference and Year Built.")
         st.write("##")

        #Call on function to creat filters and filter data
         df_grouped = filter_by_conference_age(df)

         #Plot bar chart
         bar_chart = px.bar(df_grouped,
                            x="Conference",
                            y="Amount of Stadiums",
                            text="Amount of Stadiums",
                            width= 500,
                            template='plotly_white')
         st.plotly_chart(bar_chart)

     with right_column:
         st.header("In the right Column is two Seperate Graphs, the top 10 Biggest and Smallest Stadiums with their Capacity's")
         st.write("##")

        #function to filter for top 10 largest stadiums
         top_stadiums = largest_capacity_stadiums(df, n=10)

         fig_2 = px.bar(top_stadiums,
                      x='Stadium',
                      y='Capacity',
                      orientation='v',
                      labels={'Capacity': 'Capacity (seats)', 'Stadium': 'Stadium Name'},
                      title=f'Top {top_stadiums.shape[0]} Largest Stadiums')

         st.plotly_chart(fig_2)

         smallest_stadiums = smallest_capacity_stadiums(df, n=10)

         fig_3 = px.bar(smallest_stadiums,
                      x='Stadium',
                      y='Capacity',
                      orientation='v',
                      labels={'Capacity': 'Capacity (seats)', 'Stadium': 'Stadium Name'},
                      title=f'The {smallest_stadiums.shape[0]} Smallest Stadiums')

         st.plotly_chart(fig_3)

with st.container():
    st.write("---")
    st.markdown("<h1 style='text-align: center; color: White;'>Below is a scatter plot of all the Stadiums by Year Built and Capacity.</h1>", unsafe_allow_html=True)
    # Plot bar scatter chart
    scatter = px.scatter(df, x="Built", y="Capacity", title="Scatter Plot of All Stadium Capacities",
                         color=df["Stadium"], height=1000, width=1700)
    st.plotly_chart(scatter)

#Data Frame Section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st_lottie(lottie_stadium, height=700,width=700, key="stadium")
    with right_column:
        st_lottie(lottie_football,height=700,width=700, key="football")


with st.container():
        st.write("---")
        st.header("If you want to look at all the unfiltered data, below is a DataFrame with all the information")
        st.write("##")
        # Data Frame
        st.dataframe(df)

#Get in touch with me section
with st.container():
    st.write("---")
    st.header("Get in touch with me if you have Any questions or want a stadium added!")
    st.write("##")

    #Contact form that acutally works
    contact_form = """
    <form action="https://formsubmit.co/asousa@falcon.bentley.edu" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your Email"required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()





