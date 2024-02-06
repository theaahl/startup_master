import json
from openai import OpenAI
import streamlit as st
#from streamlit_option_menu import option_menu
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import uuid
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from streamlit_extras.switch_page_button import switch_page
import time
import app_components as components 

st.set_page_config(layout = "wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
# cookie_manager.get_all()

def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()


####### SIDEBAR #######
components.sidebar_nav(False)

### HEADER ###
components.sticky_header("Task Information", "Chatbot 1", "Chatbot 2")

with st.expander("View Task *(PS: Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.)*"):
    st.write("In this user test, your task is to act as an early-stage tech startup that is in the process of developing an MVP for your business. Ask the chatbots about something you wonder about regarding MVP development. Test out **both** Chatbot 1 and Chatbot 2, then answer the questionnaire. Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.")

time.sleep(1)

# #st.subheader("All Cookies:")
# cookies = cookie_manager.get_all()
# #st.write(cookies)
# print(cookies)

# # @st.cache_resource
# # def get_manager():
# #     return stx.CookieManager()

# cookie_manager = get_manager()
# # Generate a random UUID (UUID4)
# if 'user_id' not in st.session_state:
#     if len(cookie_manager.get(cookie="userid")) == 0:
#         print("her")
#         st.session_state['user_id'] = str(uuid.uuid4())
#         #cookie = st.text_input("Cookie", key="1")
#         cookie_manager.set("userid", st.session_state.user_id)
    
#     else:
#         st.session_state['user_id'] = cookie_manager.get(cookie="userid")
#     #cookie2 = st.text_input("Cookie", key="0")
#     # print("kjeksoppskrift:")
#     # all_cookies = cookie_manager.get_all()
#     # print("starter klokke")
#     # time.sleep(2)
#     # print("klokke ferdig")

#     # print(all_cookies)
#     # print(cookie_manager.get(cookie="userid"))
#     # print(st.session_state.user_id)
#user_id = uuid.uuid4()
# st.session_state['user_id'] = cookie_manager.get(cookie="userid")
# print(cookie_manager.get(cookie="userid"))
# print(st.session_state.user_id)



print("chatbot 1 cookie", cookie_manager.get(cookie="userid"))

def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    items = db.cycle_1 # return all result from the 'test_chats' collection
    items.insert_one(mydict)

def get_chatlog():
    log = {}
    message_id_count = 0
    for msg in st.session_state.chatbot1_messages:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog):
    userchat = {"Task-1":{"id": cookie_manager.get(cookie="userid"), "time": datetime.now(), "Chatbot-1": chatlog}}
    return userchat

def update_chat_db():
    db = client.usertests 
    chatlog = get_chatlog()
    
    print(len(list(db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}))))

    if len(list(db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_1.update_one({"Task-1.id": cookie_manager.get(cookie="userid")}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Chatbot-1": chatlog}})
    else:
        write_data(get_userchat(chatlog))
        print("lagret ny chatobjekt")

if "chatbot1_messages" not in st.session_state:
    db = client.usertests 
    chatlog = []


    if len(list(db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        chatlog = db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-1")

    if len(chatlog) > 0:
        chatlog = db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-1")
        msg_count = 0
        st.session_state["chatbot1_messages"] = []
        for msg in chatlog[0]:
            st.session_state.chatbot1_messages.append({"role": chatlog[0][str(msg_count)]['role'], "content": chatlog[0][str(msg_count)]['content']})
            print(msg)
            msg_count += 1

    else:
        st.session_state["chatbot1_messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        
for msg in st.session_state.chatbot1_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.secrets.api.key: #openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    APIclient = OpenAI(api_key=st.secrets.api.key)
    st.session_state.chatbot1_messages.append({"role": "user", "content": prompt})

    st.chat_message("user").write(prompt)
    response = APIclient.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.chatbot1_messages)
    msg = response.choices[0].message.content
    st.session_state.chatbot1_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    print("kjeks her:", cookie_manager.get(cookie="userid"))

    update_chat_db()

