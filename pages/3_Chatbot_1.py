import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
st.set_page_config(layout = "wide", page_title="StartupGPT")
import app_components as components 
import chatbot_utils as cu

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

# task = "In this user test, your task is to act as an early-stage tech startup that is in the process of developing an MVP for your business. Ask the chatbots about something you wonder about regarding MVP development. Test out **both** Chatbot 1 and Chatbot 2, then answer the questionnaire. Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot."
session_storage_name = "chatbot1_messages"
# gpt_model = "gpt-3.5-turbo"
# system_description = "Act as an educational and invested startup mentor. Your role is to assist early-stage software startups in Norway with idea validation. Adopt a constructive approach to idea validation, offering clear, actionable advice to refine and test startup ideas effectively with critical insights where necessary. The mentorship includes practical guidance on developing low-fidelity prototypes and strategic insights for understanding market needs. The communication style remains formal, using industry examples to provide relevant and comprehensive advice. When faced with unclear requests, ask for clarification to provide the most relevant and helpful response. When appropriate, integrate concepts from established startup frameworks such as 6W3H, HyMap, ESSSDM, Lean Canvas, and Lean Startup. The aim is to facilitate startups in making informed decisions and developing products that align with customer needs and market demands. When giving advice, offer to provide more specific assistance on particular aspects of the response."

gpt_model = "gpt-4" #"gpt-3.5-turbo"
system_description = ""

startup_role = st.session_state['role']
startup_age = st.session_state['year']
startup_stage = st.session_state['stage']
startup_size = st.session_state['size']
startup_industry = st.session_state['industry']
startup_location = st.session_state['location']

system_description = f"I am a {startup_role}, in a {startup_stage} of {startup_size} employees, withing the     {startup_industry} industry. My startup has been operating for {startup_age} and is located in {startup_location}. Provide answers based on this information"

cu.init_chatbot(client, session_storage_name, "Chatbot-1", gpt_model, system_description, False)