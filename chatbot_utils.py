import streamlit as st
from datetime import datetime
from openai import OpenAI
from streamlit_extras.switch_page_button import switch_page

def write_data(mydict, client):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_1 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_1
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_chatlog(session_storage_name):
    log = {}
    message_id_count = 0
    for msg in st.session_state[session_storage_name]:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog, chatbot):
    userchat = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), chatbot: chatlog}}
    return userchat

def update_chat_db(client, session_storage_name, chatbot):
    db = client.usertests 
    chatlog = get_chatlog(session_storage_name)
    backup_db = client.usertests_backup
    
    print(len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1."+chatbot: chatlog}})
        backup_db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1."+chatbot: chatlog}})

    else:
        write_data(get_userchat(chatlog, chatbot), client)
        print("lagret ny chatobjekt")


def init_chatbot(client, task, session_storage_name, chatbot, gpt_model, system_description):
    if('user_id' not in st.session_state):
        st.write("You need to consent in the \"Home\" page to get access")
        switch_page("Chatbot")
    else:
        with st.expander("View Task *(PS: Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.)*"):
            st.write(task)

        if session_storage_name not in st.session_state:
            st.session_state[session_storage_name] = [{"role": "assistant", "content": "How can I help you?"}]
    
        for msg in st.session_state[session_storage_name]:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            if not st.secrets.api.key: #openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            APIclient = OpenAI(api_key=st.secrets.api.key)
            st.session_state[session_storage_name].append({"role": "user", "content": prompt})

            st.chat_message("user").write(prompt)
          
            with st.chat_message("assistant"):
                stream = APIclient.chat.completions.create(
                    model=gpt_model,
                    messages=
                        [{"role": "system", "content": system_description}] +
                        [{"role": m["role"], "content": m["content"]}
                        for m in st.session_state[session_storage_name]
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state[session_storage_name].append({"role": "assistant", "content": response})
    
            update_chat_db(client, session_storage_name, chatbot)
