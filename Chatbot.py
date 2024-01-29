from openai import OpenAI
import streamlit as st
from st_pages import add_indentation, hide_pages
import extra_streamlit_components as stx

st.set_page_config(layout="wide") 


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



@st.cache_resource
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

# Fetch a specific cookie
user_consent_cookie = cookie_manager.get(cookie="kjeks")

with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        if user_consent_cookie:
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



####### SIDEBAR #######
# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
# add_indentation()
# hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])
# #show_pages_from_config()

# with st.sidebar:
#     st.write("Your tasks")
#     with st.expander("Task 1", expanded=True):
#         if st.button("Task information"):
#             switch_page("Task_information")

#         if st.button("Chatbot 1"):
#             switch_page("Chatbot_1")
        
#         if st.button("Chatbot 2"):
#             switch_page("Chatbot_2")

#         if st.button("Feedback"):
#             switch_page("Feedback")

st.title("StartupGPT")

c = st.container()
script = """<div id = 'chat_outer'></div>"""
st.markdown(script, unsafe_allow_html=True)


# Create a main container
main_container = st.container()

with main_container:
    script = """<div id = 'chat_inner'></div>"""
    st.markdown(script, unsafe_allow_html=True)
    st.write("Consent to the usage of data for reseach purposes to unlock the chats. More information below in section \"How your data will be used\".")
    # Create a sub-container for the button
    button_container = st.empty()

    if user_consent_cookie:
        # User has already given consent
        button_container.button('Thank you for your consent', disabled=True)
    else:
        # User has not given consent yet
        consent_button = button_container.button('Click to consent to continue')

        if consent_button:
            # Set the consent cookie when the button is clicked
            cookie_manager.set("kjeks", "consent")


st.header("Information about the project")
st.write("Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.")


st.header("How you data will be used")
st.write("Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.")


st.header("How to participate in the research")
st.write("Here is some text that explains the header. It can be long or short an gives the reader an understanding of the what the header is trying to convey.")

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