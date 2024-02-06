import datetime
import uuid
import streamlit as st
from st_pages import add_indentation, hide_pages, show_pages_from_config
from streamlit_extras.switch_page_button import switch_page
import extra_streamlit_components as stx
import time
import app_components as components 

st.set_page_config(layout = "wide")
# show_pages_from_config()
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("./styles.css")

# @st.cache_resource(experimental_allow_widgets=True)
# def get_manager():
#     return stx.CookieManager()


# cookie_manager = get_manager()
# cookie_manager.get_all()

# Fetch a specific cookie
# user_consent_cookie = cookie_manager.get(cookie="userid")




# cookie_manager = get_manager()
# start_time = time.time()
# timeout = 0.01  # Preset timeout time
# while True:
#     if 'cookies' not in st.session_state:
#         st.session_state['cookies'] = cookie_manager.get_all()
#         time.sleep(2)
#     #elif time.time() - start_time > timeout:
#      #   st.warning("Operation timeout. Please refresh the page or check your network connection.")
#       #  break  # If timed out, exit the loop directly
#     else:
#         if 'lzs_userid' not in st.session_state.cookies:
#             if 'lzs_userid' not in st.session_state:
#                 st.session_state["lzs_userid"] = str(uuid.uuid4())
#             cookie_manager.set('lzs_userid', st.session_state["lzs_userid"], key="0", expires_at=datetime.datetime(year=2023, month=8, day=2))
#             print("hei", st.session_state["lzs_userid"])
#         break

    
####### SIDEBAR #######
components.sidebar_nav(False)
### HEADER ###
components.sticky_header("None", "Task Information", "Chatbot 1")

st.subheader("Task")
st.write("In this user test, your task is to act as an early-stage tech startup that is in the process of developing an MVP for your business. Ask the chatbots about something you wonder about regarding MVP development. Test out **both** Chatbot 1 and Chatbot 2, then answer the questionnaire. Ask both chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.")

st.subheader("Context")
st.write("Early-stage startups face many challenges, leading to the majority of them failing to create a viable product. One of the main reasons for this is the failure to understand the product-market fit, i.e. if the product is something customers are willing to buy.")

st.write("Creating an MVP is an important step on the way to understanding customers, and obtaining feedback from stakeholders in early stages. Low- and high-fidelity prototypes can for instance contribute to testing hypotheses about customer needs, and facilitate fundraising and early user engagement. In the early stages, low-fidelity prototypes will help the startup explore their idea and understand if the problem is worth solving. Later on, high-fidelity prototypes can help secure investors and early adopters. This exposure can help drive the startup for further growth and establish a solid market presence.")

st.write("Thank you! Your participation in this survey is a valuable contribution to our master thesis") #*insert søt emoji eller noe*

