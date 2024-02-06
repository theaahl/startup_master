from openai import OpenAI
import streamlit as st
from st_pages import add_indentation, hide_pages,show_pages_from_config
import extra_streamlit_components as stx
import uuid
import time


st.set_page_config(layout="wide") 
# show_pages_from_config()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")
add_indentation()
hide_pages(["All_Tasks", "Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()
with st.spinner('Loading page'):
    time.sleep(2)

# Fetch a specific cookie
userid_cookie = cookie_manager.get(cookie="userid")



####### SIDEBAR #######
with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        if userid_cookie:
            st.page_link("pages/6_Task_Information.py", label="Task information")
            st.page_link("pages/3_Chatbot_1.py", label="Chatbot 1")
            st.page_link("pages/4_Chatbot_2.py", label="Chatbot 2")
            st.page_link("pages/5_Feedback.py", label="Feedback")
        
        else:
            st.page_link("pages/6_Task_Information.py", label="Task information", disabled=True)
            st.page_link("pages/3_Chatbot_1.py", label="Chatbot 1", disabled=True)
            st.page_link("pages/4_Chatbot_2.py", label="Chatbot 2", disabled=True)
            st.page_link("pages/5_Feedback.py", label="Feedback", disabled=True)



#### MAIN PAGE ####
st.title("StartupGPT")

c = st.container()
script = """<div id = 'chat_outer'></div>"""
st.markdown(script, unsafe_allow_html=True)

# Fetch a specific cookie
# user_consent_cookie = cookie_manager.get(cookie="kjeks")

# Create a main container
main_container = st.container()

with main_container:
    script = """<div id = 'chat_inner'></div>"""
    st.markdown(script, unsafe_allow_html=True)
    st.write("***Please read the information below before consenting.***")
    st.write("I consent to the collection and processing of chatlogs and feedback-data as described below for the purposes of this research study.")
    # Create a sub-container for the button
    button_container = st.empty()

    if userid_cookie:
        # User has already given consent
        button_container.button('Thank you for your consent', disabled=True)
    else:
        # User has not given consent yet
        consent_button = button_container.button('Click to consent to continue')

        if consent_button:
            # Set the consent cookie when the button is clicked
            cookie_manager.set("userid", str(uuid.uuid4()))
            



st.header("Information about the project")
st.write("This website serves as a prototype developed as part of a master thesis in Computer Science at the Norwegian University of Science and Technology (NTNU). The core objective of this project is to harness the potential of ChatGPT in empowering startups. While ChatGPT is becoming a widely used tool for businesses, tailoring it to fit the needs of different sectors can make it significantly more valuable for that particular sector. For startups this can be especially valuable due to high failure rates and lack of support. The use of AI tools such as ChatGPT as a virtual assistant can thereby help entrepreneurs save time, reduce costs, and improve productivity.")
st.write("Through this prototype we specifically aim to analyze and compare various versions of ChatGPT, utilizing fine-tuning techniques and advanced prompt engineering, to identify models that best align with critical startup use cases. Obtaining real-world input is crucial in evaluating the efficacy of ChatGPT models in practical scenarios. Gaining the insights from potential users associated with startups is thereby a big help.")
st.write("The anticipated outcome of this research is a more effective use of AI tools like ChatGPT in startups, potentially leveling the playing field in the business world. By customizing these tools to the specific needs of burgeoning companies, this project aspires to contribute to a future where more startups can thrive and succeed.")

st.header("Voluntary Participation")
st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw all the data obtained concerning you for this study is deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study click the button below:")
if st.button("Click to withdraw from study"): ## Ad functionality to delete user data
    print("witdrawn") ## Add modal when feature is released
st.header("Confidentiality and Data Protection")
lst = ['All personal data collected during this study will be treated confidentially and will only be used for research purposes.', 'We will implement appropriate technical and organizational measures to ensure the security of your data.', 'Data will be anonymized/pseudonymized', 'The data will be stored securely in a secure database and will only be accessible to the research team.', 'Your data will be retained for the duration of this master study and will be destroyed securely after this period.']
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


## applying style
style = """<style>
div[data-testid='stVerticalBlock']:has(div#chat_inner):not(:has(div#chat_outer)) {background-color: #E4F2EC; border-radius:10px; padding:16px;};
</style>
"""

st.markdown(style, unsafe_allow_html=True)
