import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from st_pages import add_indentation,hide_pages



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")
####### SIDEBAR #######
# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
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





@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

# @st.cache_data(ttl=60)
# def get_data():
#     db = client.test_db #establish connection to the 'sample_guide' db
#     items = db.test.find() # return all result from the 'planets' collection
#     items = list(items)        
#     return items

# data = get_data()
# for item in data:
#     st.write(f"{item['feedback']} ")

def write_data(mydict):
    db = client.test_db #establish connection to the 'sample_guide' db
    items = db.test # return all result from the 'planets' collection
    items.insert_one(mydict)


def update_dict(c1_option_1, c1_txt_1, c1_option_2, c1_txt_2, c2_option_1, c2_txt_1, c2_option_2, c2_txt_2, c3_option_1, c3_txt_1, c3_option_2, c3_txt_2, final):
  return { "feedback":{
    "correct":{
      "chatbot_1":{
        "option":c1_option_1,
        "comment":c1_txt_1
      },
      "chatbot_2":{
        "option":c1_option_2,
        "comment":c1_txt_2
      }
    },

    "complete":{
      "chatbot_1":{
        "option":c2_option_1,
        "comment":c2_txt_1
      },
      "chatbot_2":{
        "option":c2_option_2,
        "comment":c2_txt_2
      }
    },

    "consistent":{
      "chatbot_1":{
        "option":c3_option_1,
        "comment":c3_txt_1
      },
      "chatbot_2":{
        "option":c3_option_2,
        "comment":c3_txt_2
      }
    },

    "final_comment":final
  }}

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True




with st.form("my_form"):
   st.header("Feedback form")
   st.caption("Please rate your experience with the chat based on the following criteria:")

   #Correctness
   st.subheader("Correctness")
   with st.expander(":bulb:  Correctness explenation"): #Kan legge til ,True hvis den skal være åpen som default
    st.write("Correctness indicates ..... .....")

   st.markdown("**Chatbot 1**")
   c1_option_1 = st.selectbox('To what degre did you feel the answers you received... Correctness Chatbot 1',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c1_txt_1 = st.text_area(
    "Comment on *Correctness* for **Chatbot 1**",
    "",placeholder="Comment"
    )
   
   st.markdown("**Chatbot 2**")
   c1_option_2 = st.selectbox('To what degre did you feel the answers you received...Correctness Chatbot 2',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c1_txt_2 = st.text_area(
     "Comment on *Correctness* for **Chatbot 2**",
    "",placeholder="Comment"
    )
   
   #Completeness
   st.subheader("Completeness")
   with st.expander(":bulb:  Completeness explenation"):
    st.write("Completeness indicates ..... .....")

   st.markdown("**Chatbot 1**")
   c2_option_1 = st.selectbox('To what degre did you feel the answers you received... Completeness Chatbot 1',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c2_txt_1 = st.text_area(
     "Comment on *Completeness* for **Chatbot 1**",
    "",placeholder="Comment"
    )
   
   st.markdown("**Chatbot 2**")
   c2_option_2 = st.selectbox('To what degre did you feel the answers you received...Completeness Chatbot 2',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c2_txt_2 = st.text_area(
    "Comment on  *Completeness* for **Chatbot 2**",
    "",placeholder="Comment"
    )
   
   #Consinstency
   st.subheader("Consinstency")
   with st.expander(":bulb:  Consinstency explenation"):
    st.write("Consinstency indicates ..... .....")

   st.markdown("**Chatbot 1**")
   c3_option_1 = st.selectbox('To what degre did you feel the answers you received...Consinstency Chatbot 1',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c3_txt_1 = st.text_area(
    "Comment on *Consinstency* for **Chatbot 1**",
    "",placeholder="Comment"
    )
   
   st.markdown("**Chatbot 2**")
   c3_option_2 = st.selectbox('To what degre did you feel the answers you received...Consinstency Chatbot 2',("Not at all", "Somewhat", "Very well"),placeholder="Choose an option",index=None)
   c3_txt_2 = st.text_area(
   "Comment on  *Consinstency* for **Chatbot 2**",
    "",placeholder="Comment"
    )
   
    #Consinstency
   st.subheader("Final comments")
   c4_txt = st.text_area(
   "Do you have any final comments that you would like us to know",
    "",placeholder="Comment"
    )
   # Every form must have a submit button. Fix what happends on submit
   submitted = st.form_submit_button(
        "Submit", on_click=disable, disabled=st.session_state.disabled
    )
   if submitted:
       print("Form has been submitted")
       new_dict = update_dict(c1_option_1, c1_txt_1, c1_option_2, c1_txt_2, c2_option_1, c2_txt_1, c2_option_2, c2_txt_2, c3_option_1, c3_txt_1, c3_option_2, c3_txt_2, c4_txt)
       write_data(new_dict)
       st.info("Thank you for giving us your feedback!")
