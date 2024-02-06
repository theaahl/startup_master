import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
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

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def init_cookies():
  states = ["c1_option_1", "c1_txt_1", "c1_option_2", "c1_txt_2", "c2_option_1", "c2_txt_1", "c2_option_2", "c2_txt_2", "c3_option_1", "c3_txt_1", "c3_option_2", "c3_txt_2", "c4_txt_1", "c4_txt_2","final"]

  key_count = 1
  for state in states:
    if cookie_manager.get(state) is None:
      cookie_manager.set(state, "", key=key_count)
    key_count += 1

init_cookies()

####### SIDEBAR #######
components.sidebar_nav(False)

### HEADER ###
components.sticky_header("Chatbot 2", "Feedback", "None")

#### MAIN CONTENT ####

def write_data(mydict):
    db = client.usertests #establish connection to the 'sample_guide' db
    items = db.cycle_1 # return all result from the 'planets' collection
    items.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": cookie_manager.get(cookie="userid"), "time": datetime.now(), "Feedback": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.usertests 
    user_feedback = get_user_feedback(feedback)
    
    print("feedback:", user_feedback)
    print("userid:", cookie_manager.get(cookie="userid"))

    print(len(list(db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}))))

    if len(list(db.cycle_1.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_1.update_one({"Task-1.id": cookie_manager.get(cookie="userid")}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Feedback": feedback}})
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

    "usefull":{
      "chatbot_1":{
        "option":cookie_manager.get("c4_option_1"),
        "comment":cookie_manager.get("c4_txt_1")
      },
      "chatbot_2":{
        "option":cookie_manager.get("c4_option_2"),
        "comment":cookie_manager.get("c4_txt_2")
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
  # st.write("Correctness indicates ..... .....")
  lst = ['The answer aligns with the literature and other sources as far as known for the user (factually correct).', 'The chatbot is able to understand the context, provide relevant information, and meet the user\'s expectations in a way that adds value to their specific objectives']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)


st.markdown("**Chatbot 1**")
c1_option_1 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Correctness**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c1_option_1"))
cookie_manager.set("c1_option_1", c1_option_1, key="c1_option_1")

c1_txt_1 = st.text_area(
"Comment on **Correctness** for **Chatbot 1**",
value=cookie_manager.get("c1_txt_1"),placeholder="Comment"
)
cookie_manager.set("c1_txt_1", c1_txt_1, key="c1_txt_1")

st.markdown("**Chatbot 2**")
c1_option_2 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Correctness**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c1_option_2"))
cookie_manager.set("c1_option_2", c1_option_2, key="c1_option_2")

c1_txt_2 = st.text_area(
"Comment on **Correctness** for **Chatbot 2**",
value=cookie_manager.get("c1_txt_2"),placeholder="Comment"
)
cookie_manager.set("c1_txt_2", c1_txt_2, key="c1_txt_2")

c1_prefer = st.selectbox(
   "Which chatbot do you think gave the most correct answers?",
   ("Chatbot 1", "Chatbot 2", "No difference"),
   index=None,
   placeholder="Select chatbot",
)



#Completeness
st.subheader("Completeness")
with st.expander(":bulb:  Completeness explenation"):
  # st.write("Completeness indicates ..... .....")
  lst = ['The answers lacks no essential components', 'The chatbot answers all questions in the users prompt']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c2_option_1 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Completeness**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c2_option_1"))
cookie_manager.set("c2_option_1", c2_option_1, key="c2_option_1")
c2_txt_1 = st.text_area(
"Comment on **Completeness** for **Chatbot 1**",
value=cookie_manager.get("c2_txt_1"),placeholder="Comment"
)
cookie_manager.set("c2_txt_1", c2_txt_1, key="c2_txt_1")

st.markdown("**Chatbot 2**")
c2_option_2 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Completeness**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c2_option_2"))
cookie_manager.set("c2_option_2", c2_option_2, key="c2_option_2")
c2_txt_2 = st.text_area(
"Comment on  **Completeness** for **Chatbot 2**",
value=cookie_manager.get("c2_txt_2"),placeholder="Comment"
)
cookie_manager.set("c2_txt_2", c2_txt_2, key="c2_txt_2")

c2_prefer = st.selectbox(
   "Which chatbot do you think gave the most complete answers",
   ("Chatbot 1", "Chatbot 2", "No difference"),
   index=None,
   placeholder="Select chatbot",
)



#Consinstency
st.subheader("Consinstency")
with st.expander(":bulb:  Consinstency explenation"):
  #st.write("Consinstency indicates ..... .....")
  lst = ['Consistency between input and response', 'No contradictions in the same answer (internal consistency)']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c3_option_1 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Consinstency**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c3_option_1", c3_option_1, key="c3_option_1")
c3_txt_1 = st.text_area(
"Comment on **Consinstency** for **Chatbot 1**",
value=cookie_manager.get("c3_txt_1"),placeholder="Comment"
)
cookie_manager.set("c3_txt_1", c3_txt_1, key="c3_txt_1")

st.markdown("**Chatbot 2**")
c3_option_2 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Consinstency**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c3_option_2", c3_option_2, key="c3_option_2")
c3_txt_2 = st.text_area(
"Comment on  **Consinstency** for **Chatbot 2**",
value=cookie_manager.get("c3_txt_2"),placeholder="Comment"
)
cookie_manager.set("c3_txt_2", c3_txt_2, key="c3_txt_2")


c3_prefer = st.selectbox(
   "Which chatbot do you think gave the most consistent answers",
   ("Chatbot 1", "Chatbot 2", "No difference"),
   index=None,
   placeholder="Select chatbot",
)


#Usefulness
st.subheader("Usefulness")
with st.expander(":bulb:  Usefulness explenation"):
  #st.write("Consinstency indicates ..... .....")
  lst = ['The provided answers with valuable information (not too broad, not too unspecific) ', 'The chatbot delivered relevant information without too many user inputs']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c4_option_1 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Usefulness**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c4_option_1", c3_option_1, key="c4_option_1")
c4_txt_1 = st.text_area(
"Comment on **Usefulness** for **Chatbot 1**",
value=cookie_manager.get("c4_txt_1"),placeholder="Comment"
)
cookie_manager.set("c4_txt_1", c4_txt_1, key="c4_txt_1")

st.markdown("**Chatbot 2**")
c4_option_2 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Usefulness**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option("c3_option_2"))
cookie_manager.set("c4_option_2", c4_option_2, key="c4_option_2")
c4_txt_2 = st.text_area(
"Comment on  **Usefulness** for **Chatbot 2**",
value=cookie_manager.get("c4_txt_2"),placeholder="Comment"
)
cookie_manager.set("c4_txt_2", c4_txt_2, key="c4_txt_2")


c4_prefer = st.selectbox(
   "Which chatbot do you think gave the most useful answers",
   ("Chatbot 1", "Chatbot 2", "No difference"),
   index=None,
   placeholder="Select chatbot",
)


#Final comments
st.subheader("Final comments")
final_txt = st.text_area(
"Do you have any final comments that you would like us to know",
value=cookie_manager.get("final"),placeholder="Comment"
)
cookie_manager.set("final", final_txt, key="final")
# Every form must have a submit button. Fix what happends on submit
submitted = st.button(
  "Submit", on_click=disable, disabled=st.session_state.disabled
)


if submitted:
  print("Form has been submitted")
  all_feedback = gather_feedback()
  update_chat_db(all_feedback)
  st.info("Thank you for giving us your feedback!")
   

   
   
