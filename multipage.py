import streamlit as st

class MultiPage:




    def __init__(self):
        self.pages = []

    def add_page(self, title, func):

        self.pages.append({
            'title': title,
            'function': func
            })

    def run(self):

        app = st.sidebar.selectbox('Navigation',
                           self.pages,
                           format_func=lambda app: app['title'])

        app['function']()
