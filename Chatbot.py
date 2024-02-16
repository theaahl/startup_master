from datetime import datetime
import streamlit as st
import uuid
import app_components as components 
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide", page_title="StartupGPT") 


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

print(st.session_state['user_id'])

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

#### MAIN PAGE ####
st.title("Welcome to StartupGPT")


st.header("Information about the project")
st.write("This website serves as a prototype developed as part of a master thesis in Computer Science at the Norwegian University of Science and Technology (NTNU). The core objective of this project is to harness the potential of ChatGPT in empowering startups. While ChatGPT is becoming a widely used tool for businesses, tailoring it to fit the needs of different sectors can make it significantly more valuable for that particular sector. For startups this can be especially valuable due to high failure rates and lack of support. The use of AI tools such as ChatGPT as a virtual assistant can thereby help entrepreneurs save time, reduce costs, and improve productivity.")
st.write("Through this prototype we specifically aim to analyze and compare various versions of ChatGPT to identify models that best align with critical startup use cases. Obtaining real-world input is crucial in evaluating the efficacy of ChatGPT models in practical scenarios. Gaining the insights from potential users associated with startups is thereby a big help.")
st.write("The anticipated outcome of this research is a more effective use of AI tools like ChatGPT in startups. By customizing these tools to the specific needs startup companies, this project aspires to contribute to a future where more startups can thrive and succeed.")

def gather_feedback():
  return {
    "stage": st.session_state['stage'],
    "year_of_business":st.session_state['year'],
    "size": st.session_state['size'],
    "industry": st.session_state['industry'],
    #"revenue": st.session_state['revenue'],
    "location": st.session_state['location'],
    "role": st.session_state['role'],
    "ChatGPT_experience":st.session_state['gpt_experience'],
  }

def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_1 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_1
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), "Demographic": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.usertests 
    backup_db = client.usertests_backup
    user_feedback = get_user_feedback(feedback)

    print("form:", user_feedback)
    print("userid:", st.session_state['user_id'])

    print(len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})
        backup_db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})

    else:
        write_data(user_feedback)
        print("lagret ny chatobjekt")


def get_selectbox_index(option_list, session_state_key):
    # """Returns the index of the current session state value in the options list, or None if not found."""
    try:
        return option_list.index(st.session_state[session_state_key])
    except (ValueError, KeyError):
        return None  # Return None to use the placeholder


def display_form():
    # """Displays the form for both new and returning users."""
    st.subheader("Fill out form to continue")
    st.write("By submitting the form you are consenting to the collection and processing of chatlogs and form-data as described below for the purposes of this research study.")

    st.caption("Business details")
    stage_options = ["Seed stage", "Early stage", "Growth stage", "Mature stage"]
    year_options = ["<1 year", "2-5 years", "5-10 years", ">10 years"]
    gpt_exp_options = ["No experience", "Some experience", "Very familiar"]

    st.session_state['stage'] = st.selectbox("Stage", options=stage_options, index=get_selectbox_index(stage_options, 'stage'), placeholder="Select an option")
    st.session_state['year'] = st.selectbox("Year of business", year_options, index=get_selectbox_index(year_options, 'year'), placeholder="Select an option")
    st.session_state['size'] = st.number_input("Size of business", value=st.session_state.get('size'), placeholder="Number of employees", )
    st.session_state['industry'] = st.text_input("Industry", value=st.session_state.get('industry', ''), placeholder="Technology, healthcare, finance, etc.")
    # Uncomment the following line if needed
    # st.session_state['revenue'] = st.selectbox("Revenue Range", ["No revenue", "<1M NOK", "1M-10M NOK", ">10M NOK"], placeholder="Select an option") 

    st.session_state['location'] = st.text_input("Location", value=st.session_state.get('location', ''), placeholder="City, Country")

    st.caption("Personal details")
    st.session_state['role'] = st.text_input("Company Role", value=st.session_state.get('role', ''), placeholder="CEO, CTO, backend developer, UI/UX designer, etc.")
    st.session_state['gpt_experience'] = st.selectbox("Level of experience with ChatGPT", gpt_exp_options, index=get_selectbox_index(gpt_exp_options, 'gpt_experience'), placeholder="Select an option")

def handle_submit(is_new_user, submit_text):
    # """Handles the form submission for new and returning users."""
    if is_new_user:
        st.session_state['user_id'] = str(uuid.uuid4())

    st.toast("Thank you for submitting. You can still update the information and submit again")
    
    if submit_text != "Click to update form information":
        button_container.form_submit_button("Click to update form information")
        st.info("You can now access the tasks in the sidebar")
    all_feedback = gather_feedback()
    update_chat_db(all_feedback)

with st.form("test_form"):
    is_new_user = st.session_state.get('user_id') is None
    display_form()

    submit_text = "Submit and consent to data usage as described on this page" if is_new_user else "Click to update form information"
    button_container = st.empty()

    if button_container.form_submit_button(submit_text):
        handle_submit(is_new_user, submit_text)


st.header("Voluntary Participation")
st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw all the data obtained concerning you for this study is deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study click the button below:")
withdraw_button_container = st.empty()
if st.session_state['user_id'] is None:
    withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=True)
else:
    if withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=False):
        
        print("witdrawn") ## Add modal when feature is released
        db = client.usertests
        backup_db = client.usertests_backup

        if len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))) > 0:
            db.cycle_1.delete_one({"Task-1.id": st.session_state['user_id']})
            backup_db.cycle_1.delete_one({"Task-1.id": st.session_state['user_id']})

        for key in st.session_state.keys():
            del st.session_state[key]
        
        st.session_state['user_id'] = None  
        
        withdraw_button = withdraw_button_container.button("You have successfully withdrawn from the study. All data associated to you has been deleted", type="primary", disabled=True)   
        consent_button = button_container.form_submit_button('Submit and consent to data usage as described on this page')

        streamlit_js_eval(js_expressions="parent.window.location.reload()")
####### SIDEBAR #######
components.sidebar_nav(st.session_state['user_id'] is None)

st.header("Confidentiality and Data Protection")
lst = ['All personal data collected during this study will be treated confidentially and will only be used for research purposes.', 'We will implement appropriate technical and organizational measures to ensure the security of your data.', 'Data will be anonymized', 'The data will be stored securely in a secure database and will only be accessible to the research team.', 'Your data will be retained for the duration of this master study and will be destroyed securely after this period.']
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)

st.header("Rights of Participants")
lst_2 = ["You have the right to access your personal data and request a copy of the data collected from you.", "You have the right to request rectification or erasure of your personal data.","You have the right to object to the processing of your data and to restrict processing in certain circumstances."]
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)


st.header("Contact")
st.write("If you have any questions or feedback on the prototype, please don't hesitate to contact us!")
st.markdown('<a href="mailto:thealah@stud.ntnu.no">thealah@stud.ntnu.no</a>', unsafe_allow_html=True)
st.markdown('<a href="mailto:helenfs@stud.ntnu.no">helenfs@stud.ntnu.no</a>', unsafe_allow_html=True)

