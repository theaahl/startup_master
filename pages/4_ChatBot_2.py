import streamlit as st
from openai import OpenAI
#from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from st_pages import add_indentation,hide_pages, show_pages_from_config

st.set_page_config(layout="wide") 
# show_pages_from_config()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("/Users/theaahlgren/Documents/Masteroppgave/StartupGPT_prototype/startup_master/styles.css")

# Custom CSS for back and forth buttons to fit content
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)


### Custom CSS for the sticky header
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: white;
        z-index: 999;
    }
</style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)


####### SIDEBAR ######
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])
#show_pages_from_config()

with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        task_info = f"""
         <a href="Task_Information" target = "_self">
         <button class="not_clicked">
            Task information
        </button></a>
            """
        st.markdown(task_info, unsafe_allow_html=True)

        c1 = f"""
        <a href="Chatbot_1" target = "_self">
        <button class="not_clicked">
            Chatbot 1
        </button></a>
            """
        st.markdown(c1, unsafe_allow_html=True)

        c2 = f"""
        <a href="Chatbot_2" target = "_self">
        <button class="clicked">
            Chatbot 2
        </button></a>
            """
        st.markdown(c2, unsafe_allow_html=True)

        feedback = f"""
        <a href="Feedback" target = "_self">
        <button class="not_clicked">
            Feedback
        </button></a>
            """
        st.markdown(feedback, unsafe_allow_html=True)

#### HEADER ####
header = st.container()
header.warning('Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information')
header.header("Chatbot 2")
col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: Chatbot 1", type="secondary"):
        switch_page("chatbot 1")
with col2:
    if st.button("Next step: Feedback", type="primary"):
        switch_page("feedback")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)


#### MAIN CONTENT ####
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def write_data(mydict):
    db = client.test_db #establish connection to the 'test_db' db
    items = db.test_chat # return all result from the 'test_chats' collection
    items.insert_one(mydict)

def get_chatlog():
    log = {}
    message_id_count = 0
    for msg in st.session_state.chatbot2_messages:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog):
    userchat = {"Task-1":{"id": str(st.session_state.user_id), "time": datetime.now(), "Chatbot-2": chatlog}}
    return userchat

def update_chat_db():
    db = client.test_db 
    chatlog = get_chatlog()
    
    print(len(list(db.test_chat.find({"Task-1.id": st.session_state.user_id}))))
    print(st.session_state.user_id)

    if len(list(db.test_chat.find({"Task-1.id": st.session_state.user_id}))) > 0:
        print("opdaterte chatobjekt")
        db.test_chat.update_one({"Task-1.id": st.session_state.user_id}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Chatbot-2": chatlog}})
    else:
        write_data(get_userchat(chatlog))
        print("lagret ny chatobjekt")

    print(st.session_state.user_id)

# savebutton = st.button("Save chat")

# if savebutton:
#     chatlog = get_userchat(get_chatlog())
#     write_data(chatlog)
#     db = client.test_db 
#     print(len(list(db.test_chat.find({"Task-1.id": str(st.session_state.user_id)}))))


if "chatbot2_messages" not in st.session_state:
    st.session_state["chatbot2_messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.chatbot2_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    #client = OpenAI(api_key=openai_api_key)
    st.session_state.chatbot2_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", chatbot2_messages=st.session_state.chatbot2_messages)
    msg = "hello" #response.choices[0].message.content
    st.session_state.chatbot2_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    update_chat_db()