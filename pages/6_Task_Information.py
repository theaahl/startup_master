import datetime
import uuid
import streamlit as st
from st_pages import add_indentation, hide_pages, show_pages_from_config
from streamlit_extras.switch_page_button import switch_page
import extra_streamlit_components as stx
import time


st.set_page_config(layout = "wide")
# show_pages_from_config()
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("./styles.css")


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


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

# Fetch a specific cookie
user_consent_cookie = cookie_manager.get(cookie="kjeks")




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
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])


with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        if user_consent_cookie:
            task_info = f"""
            <a href="Task_Information" target = "_self">
            <button class="clicked">
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
            <button class="not_clicked">
                Feedback
            </button></a>
                """
            st.markdown(feedback, unsafe_allow_html=True)

        else:
            task_info = f"""
            <a href="Task_Information" target = "_self">
            <button type="button" class="not_clicked">
                Task information
            </button></a>
                """
            st.markdown(task_info, unsafe_allow_html=True)

            c1 = f"""
            <a href="Chatbot_1" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 1
            </button></a>
                """
            st.markdown(c1, unsafe_allow_html=True)

            c2 = f"""
            <a href="Chatbot_2" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 2
            </button></a>
                """
            st.markdown(c2, unsafe_allow_html=True)

            feedback = f"""
            <a href="Feedback" target = "_self">
            <button type="button" class="disabeled" disabled>
                Feedback
            </button></a>
                """
            st.markdown(feedback, unsafe_allow_html=True)

header = st.container()
header.info('Please read the task carefully to make sure you know how to communicate with ChatGPT in the next step')
header.header("Task Information")
col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: None", type="secondary", disabled=True):
        switch_page("Task Information")
with col2:
    if st.button("Next step: Chatbot 1", type="primary"):
        switch_page("chatbot 1")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)


