import datetime
import uuid
import streamlit as st
from st_pages import add_indentation, hide_pages, show_pages_from_config
from streamlit_extras.switch_page_button import switch_page
import extra_streamlit_components as stx
import time
import app_components as components 

st.set_page_config(layout = "wide", page_title="StartupGPT")
# show_pages_from_config()
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("./styles.css")
    
####### SIDEBAR #######
components.sidebar_nav(False)
### HEADER ###
components.sticky_header("None", "Task Information", "Chatbot 1")
if('user_id' not in st.session_state):
    st.write("You need to consent in the \"Home\" page to get access")
    switch_page("Chatbot")
else:
    st.subheader("Task")
    st.write("In this user test, your task is to act as an early-stage tech startup that is in the process of developing an MVP for your business. Ask the chatbots about something you wonder about regarding MVP development. Test out **both** Chatbot 1 and Chatbot 2, then answer the questionnaire. Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.")

    st.subheader("Context")
    st.write("Early-stage startups face many challenges, leading to the majority of them failing to create a viable product. One of the main reasons for this is the failure to understand the product-market fit, i.e. if the product is something customers are willing to buy.")

    st.write("Creating an MVP is an important step on the way to understanding customers, and obtaining feedback from stakeholders in early stages. Low- and high-fidelity prototypes can for instance contribute to testing hypotheses about customer needs, and facilitate fundraising and early user engagement. In the early stages, low-fidelity prototypes will help the startup explore their idea and understand if the problem is worth solving. Later on, high-fidelity prototypes can help secure investors and early adopters. This exposure can help drive the startup for further growth and establish a solid market presence.")

    st.write("Thank you! Your participation in this survey is a valuable contribution to our master thesis") #*insert søt emoji eller noe*

