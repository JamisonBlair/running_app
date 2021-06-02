import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from multipage import MultiPage
import about

import folium

@st.cache
def get_route_points(url):
        return get_lats_longs('https://'+url)

def model():
        least = int(st.selectbox('At least (miles)', list(range(0,10))))
        most = st.selectbox('At most (miles)', list(range(0,10))+['Any'])
        if most == 'Any':
                most = np.inf
        most = float(most)
        hills = st.selectbox('Hills?', ['','Little to none', 'Moderate', 'Intense', 'No preference'])
        loop = st.selectbox('Round trip?', ['','Yes','No', 'Either'])
        city = st.selectbox('Choose a city', ['','Chico', 'Oakland', \
                                                 'San Francisco', 'San Jose'])
        address = st.text_input('Address', '')

        routes = pd.read_csv('DATA', index_col=False)
        routes = routes[routes['city']== city.lower()]

        if address != '' and hills !='' and loop != '' and city != '':
                address = address + ', ' + city
                
                try:
                        loc = convert_address(address)
                        recs = route_finder(loc, hills, loop, least, most, routes)
                except:
                        st.write("Unable to find a route near that location. Please try another one.")
                        st.stop()
                if type(recs) is str:
                        st.write(recs)
                else:
                        choices, urls = route_display(recs, routes)
                        selection = st.selectbox('Choose a recommendation:', ['']+choices)
                        if selection!='':
                                a = int(selection[0])-1
                                url = urls[a]
                                m = folium.Map(location=eval(recs[a][1]),tiles='OpenStreetMap',zoom_start=13)
                                folium.Marker(location=eval(recs[a][1]), popup='Start').add_to(m)
                                folium.Marker(location=loc,popup='You', icon=folium.Icon()).add_to(m)
                                route = get_route_points(url)
                                folium.PolyLine(route,
                                        color='red',
                                        weight=2,
                                        opacity=1).add_to(m)
                                m

def main():
        app = MultiPage()
        st.markdown('''
        # Running Route Recommendation App
        ''')
        app.add_page('About', about.page)
        app.add_page('Recommender', model)

        app.run()


if __name__ == '__main__':
        main()
