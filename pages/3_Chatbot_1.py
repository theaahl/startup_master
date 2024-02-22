import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import app_components as components 
import chatbot_utils as cu

st.set_page_config(layout = "wide", page_title="StartupGPT")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

@st.cache_resource(experimental_allow_widgets=True)
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()


####### SIDEBAR #######
components.sidebar_nav(False)

### HEADER ###
components.sticky_header("Task Information", "Chatbot 1", "Chatbot 2")

session_storage_name = "chatbot1_messages"
gpt_model = "gpt-3.5-turbo"

cu.init_chatbot(client, session_storage_name, "Chatbot-1", gpt_model)

