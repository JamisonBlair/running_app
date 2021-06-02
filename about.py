import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def page():
    st.write("""
    Welcome! This is a route recommendation app for runners, created by Jamison Barsotti.
    Using public data from Runkeeper, runners in San Francisco, Oakland, San Jose,
    and Chico, California, can find nearby routes that fit their athletic level.

    Users can
    input their location, desired distance (in miles), and hill preference, and the app will generate
    five nearby routes fitting those qualifications, ranked by proximity to the user.
    Try it out by selecting the 'Recommender' option on the sidebar.
    ___
    ## About the data
    The data used was gathered from public routes available on Runkeeper. Below,
    you can check out the mileage distribution of the gathered routes that are less
    than or equal to 30 miles in distance.
    """)
    city = st.selectbox('City', ['All','Chico','Oakland',\
                                 'San Francisco', 'San Jose'])
    
    
    df = pd.read_csv("DATA")
    if city != 'All':
        df = df[df['city'] == city.lower()]
    
    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=False)
    sns.histplot(df['miles'][df['miles']<=30], bins=60)
    plt.xlabel("Distance in miles")
    plt.ylabel("Route count")
    st.pyplot(fig)

    st.write("""
    As one might expect, each of these distributions are skewed right.
    We can even find evidence that the typical runner likes
    routes that are either races, or at the very least, common race distances.
    We can see that by noting the median route distance
    for each distribution is around 3.1 miles, or a 5k. There are also noticeable
    bumps in the distributions arond 6.2 miles (10k), 13.1 miles (half marathon), and,
    with the exception of Chico, 26.1 miles (marathon). Note that Chico is a much smaller
    city without a well-known marathon.
    """)

