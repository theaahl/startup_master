import streamlit as st
from st_pages import add_indentation, hide_pages
import extra_streamlit_components as stx
import time
st.set_page_config(layout="wide") 


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()
with st.spinner('Loading page'):
    time.sleep(0.2)
user_consent_cookie = cookie_manager.get(cookie="kjeks")


local_css("./styles.css")
####### SIDEBAR #######
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])


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



#### MAIN PAGE ####
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
st.write("This website serves as a prototype developed as part of a master thesis in Computer Science at the Norwegian University of Science and Technology (NTNU). The core objective of this project is to harness the potential of ChatGPT in empowering startups. While ChatGPT is becoming a widely used tool for businesses, tailoring it to fit the needs of different sectors can make it significantly more valuable for that particular sector. For startups this can be especially valuable due to high failure rates and lack of support. The use of AI tools such as ChatGPT as a virtual assistant can thereby help entrepreneurs save time, reduce costs, and improve productivity.")
st.write("Through this prototype we specifically aim to analyze and compare various versions of ChatGPT, utilizing fine-tuning techniques and advanced prompt engineering, to identify models that best align with critical startup use cases. Obtaining real-world input is crucial in evaluating the efficacy of ChatGPT models in practical scenarios. Gaining the insights from potential users associated with startups is thereby a big help.")
st.write("The anticipated outcome of this research is a more effective use of AI tools like ChatGPT in startups, potentially leveling the playing field in the business world. By customizing these tools to the specific needs of burgeoning companies, this project aspires to contribute to a future where more startups can thrive and succeed.")

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