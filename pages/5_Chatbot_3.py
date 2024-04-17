import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
st.set_page_config(layout="wide", page_title="StartupGPT") 
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
components.sticky_header("Chatbot 2", "Chatbot 3", "Feedback")

session_storage_name = "chatbot3_messages"

gpt_model = "gpt-4"
def generate_system_instructions():
    description_variables = ['role', 'year', 'stage', 'size', 'industry', 'location']
    description_defaults = ['startup member', 'some years', 'startup', 'some', 'undisclosed', 'Norway']
    demographics_dict = {}

    for i in range(len(description_variables)):
        var = 'startup_' + description_variables[i]
        if description_variables[i] in st.session_state:
            demographics_dict[var] = st.session_state[description_variables[i]]

        else:
            demographics_dict[var] = description_defaults[i]

    return demographics_dict

demographics_dict = generate_system_instructions()

system_description = f"Act as an educational and invested startup mentor. Your role is to assist the {demographics_dict['startup_role']}, of a {demographics_dict['startup_year']} old startup in this stage: {demographics_dict['startup_stage']}, in {demographics_dict['startup_location']} with idea validation. The startup operates within the {demographics_dict['startup_industry']} industry and has {demographics_dict['startup_size']} employees."

cu.init_chatbot(client, session_storage_name, "Chatbot-3", gpt_model,system_description, True)

