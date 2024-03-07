import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import app_components as components 
import chatbot_utils as cu

st.set_page_config(layout="wide", page_title="StartupGPT") 


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
components.sticky_header("Chatbot 1", "Chatbot 2", "Chatbot 3")

session_storage_name = "chatbot2_messages"
# gpt_model = "gpt-4"
# system_description = ""
gpt_model = "gpt-3.5-turbo"
system_description = "Act as an educational and invested startup mentor. Your role is to assist early-stage software startups in Norway with idea validation. Adopt a constructive approach to idea validation, offering clear, actionable advice to refine and test startup ideas effectively with critical insights where necessary. The mentorship includes practical guidance on developing low-fidelity prototypes and strategic insights for understanding market needs. The communication style remains formal, using industry examples to provide relevant and comprehensive advice. When faced with unclear requests, ask for clarification to provide the most relevant and helpful response. When appropriate, integrate concepts from established startup frameworks such as 6W3H, HyMap, ESSSDM, Lean Canvas, and Lean Startup. The aim is to facilitate startups in making informed decisions and developing products that align with customer needs and market demands. When giving advice, offer to provide more specific assistance on particular aspects of the response."


cu.init_chatbot(client, session_storage_name,  "Chatbot-2", gpt_model, system_description)

