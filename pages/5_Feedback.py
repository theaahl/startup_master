import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout = "wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")


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

####### SIDEBAR #######
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])

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
        <button class="not_clicked">
            Chatbot 2
        </button></a>
            """
        st.markdown(c2, unsafe_allow_html=True)

        feedback = f"""
        <a href="Feedback" target = "_self">
        <button class="clicked">
            Feedback
        </button></a>
            """
        st.markdown(feedback, unsafe_allow_html=True)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()   

header = st.container()
header.header("Feedback")

col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: Chatbot 2", type="secondary"):
        switch_page("chatbot 2")
with col2:
    if st.button("Next step: None", type="primary", disabled=True):
        switch_page("feedback")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

#### MAIN CONTENT ####
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def init_cookies():
  states = ["c1_option_1", "c1_txt_1", "c1_option_2", "c1_txt_2", "c2_option_1", "c2_txt_1", "c2_option_2", "c2_txt_2", "c3_option_1", "c3_txt_1", "c3_option_2", "c3_txt_2", "final"]

  key_count = 1
  for state in states:
    if cookie_manager.get(state) is None:
      cookie_manager.set(state, "", key=key_count)
    key_count += 1

init_cookies()

def write_data(mydict):
    db = client.test_db #establish connection to the 'sample_guide' db
    items = db.chat # return all result from the 'planets' collection
    items.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": cookie_manager.get(cookie="userid"), "time": datetime.now(), "Feedback": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.test_db 
    user_feedback = get_user_feedback(feedback)
    
    print("feedback:", user_feedback)
    print("userid:", cookie_manager.get(cookie="userid"))

    print(len(list(db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))))

    if len(list(db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        print("opdaterte chatobjekt")
        db.chat.update_one({"Task-1.id": cookie_manager.get(cookie="userid")}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Feedback": feedback}})
    else:
        write_data(user_feedback)
        print("lagret ny chatobjekt")

def gather_feedback():
  return {
    "correct":{
      "chatbot_1":{
        "option":cookie_manager.get("c1_option_1"),
        "comment":cookie_manager.get("c1_txt_1")
      },
      "chatbot_2":{
        "option":cookie_manager.get("c1_option_2"),
        "comment":cookie_manager.get("c1_txt_2")
      }
    },

    "complete":{
      "chatbot_1":{
        "option":cookie_manager.get("c2_option_1"),
        "comment":cookie_manager.get("c2_txt_1")
      },
      "chatbot_2":{
        "option":cookie_manager.get("c2_option_2"),
        "comment":cookie_manager.get("c2_txt_2")
      }
    },

    "consistent":{
      "chatbot_1":{
        "option":cookie_manager.get("c3_option_1"),
        "comment":cookie_manager.get("c3_txt_1")
      },
      "chatbot_2":{
        "option":cookie_manager.get("c3_option_2"),
        "comment":cookie_manager.get("c3_txt_2")
      }
    },

    "final_comment":cookie_manager.get("final")
  }

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True
    
#------------- Form ------------------------   
    
st.caption("Please rate your experience with the chat based on the following criteria:")

selectionbox_options = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]

def get_selected_option(cookie):
  value = cookie_manager.get(cookie)
  return None if value == '' or value == None else selectionbox_options.index(value)

#Correctness
st.subheader("Correctness")
with st.expander(":bulb:  Correctness explenation"): #Kan legge til ,True hvis den skal være åpen som default
  st.write("Correctness indicates ..... .....")

st.markdown("**Chatbot 1**")
c1_option_1 = st.selectbox('To what degre did you feel the answers you received... Correctness Chatbot 1',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c1_option_1"))
cookie_manager.set("c1_option_1", c1_option_1, key="c1_option_1")

c1_txt_1 = st.text_area(
"Comment on *Correctness* for **Chatbot 1**",
value=cookie_manager.get("c1_txt_1"),placeholder="Comment"
)
cookie_manager.set("c1_txt_1", c1_txt_1, key="c1_txt_1")

st.markdown("**Chatbot 2**")
c1_option_2 = st.selectbox('To what degre did you feel the answers you received...Correctness Chatbot 2',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c1_option_2"))
cookie_manager.set("c1_option_2", c1_option_2, key="c1_option_2")
c1_txt_2 = st.text_area(
"Comment on *Correctness* for **Chatbot 2**",
value=cookie_manager.get("c1_txt_2"),placeholder="Comment"
)
cookie_manager.set("c1_txt_2", c1_txt_2, key="c1_txt_2")

#Completeness
st.subheader("Completeness")
with st.expander(":bulb:  Completeness explenation"):
  st.write("Completeness indicates ..... .....")

st.markdown("**Chatbot 1**")
c2_option_1 = st.selectbox('To what degre did you feel the answers you received... Completeness Chatbot 1',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c2_option_1"))
cookie_manager.set("c2_option_1", c2_option_1, key="c2_option_1")
c2_txt_1 = st.text_area(
"Comment on *Completeness* for **Chatbot 1**",
value=cookie_manager.get("c2_txt_1"),placeholder="Comment"
)
cookie_manager.set("c2_txt_1", c2_txt_1, key="c2_txt_1")

st.markdown("**Chatbot 2**")
c2_option_2 = st.selectbox('To what degre did you feel the answers you received...Completeness Chatbot 2',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c2_option_2"))
cookie_manager.set("c2_option_2", c2_option_2, key="c2_option_2")
c2_txt_2 = st.text_area(
"Comment on  *Completeness* for **Chatbot 2**",
value=cookie_manager.get("c2_txt_2"),placeholder="Comment"
)
cookie_manager.set("c2_txt_2", c2_txt_2, key="c2_txt_2")

#Consinstency
st.subheader("Consinstency")
with st.expander(":bulb:  Consinstency explenation"):
  st.write("Consinstency indicates ..... .....")

st.markdown("**Chatbot 1**")
c3_option_1 = st.selectbox('To what degre did you feel the answers you received...Consinstency Chatbot 1',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c3_option_1", c3_option_1, key="c3_option_1")
c3_txt_1 = st.text_area(
"Comment on *Consinstency* for **Chatbot 1**",
value=cookie_manager.get("c3_txt_1"),placeholder="Comment"
)
cookie_manager.set("c3_txt_1", c3_txt_1, key="c3_txt_1")

st.markdown("**Chatbot 2**")
c3_option_2 = st.selectbox('To what degre did you feel the answers you received...Consinstency Chatbot 2',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c3_option_2", c3_option_2, key="c3_option_2")
c3_txt_2 = st.text_area(
"Comment on  *Consinstency* for **Chatbot 2**",
value=cookie_manager.get("c3_txt_2"),placeholder="Comment"
)
cookie_manager.set("c3_txt_2", c3_txt_2, key="c3_txt_2")

#Consinstency
st.subheader("Final comments")
c4_txt = st.text_area(
"Do you have any final comments that you would like us to know",
value=cookie_manager.get("final"),placeholder="Comment"
)
cookie_manager.set("final", c4_txt, key="final")
# Every form must have a submit button. Fix what happends on submit
submitted = st.button(
  "Submit", on_click=disable, disabled=st.session_state.disabled
)


if submitted:
  print("Form has been submitted")
  all_feedback = gather_feedback()
  update_chat_db(all_feedback)
  st.info("Thank you for giving us your feedback!")
   

   
   
