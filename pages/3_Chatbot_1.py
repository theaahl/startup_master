import json
from openai import OpenAI
import streamlit as st
#from streamlit_option_menu import option_menu
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from streamlit_extras.switch_page_button import switch_page
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

task = "In this user test, your task is to act as an early-stage tech startup that is in the process of developing an MVP for your business. Ask the chatbots about something you wonder about regarding MVP development. Test out **both** Chatbot 1 and Chatbot 2, then answer the questionnaire. Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot."
session_storage_name = "chatbot1_messages"

cu.init_chatbot(client, task, session_storage_name, "Chatbot-1")

