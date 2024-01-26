import streamlit as st 
from st_pages import add_indentation,hide_pages
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
        <button class="clicked">
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

header = st.container()

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

s = f"<p style='color:red;'>Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information.</p>"
header.markdown(s, unsafe_allow_html=True) 
header.header("Chatbot 1")
#st.markdown(title_style,unsafe_allow_html=True)
col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: Task Information", type="secondary"):
        switch_page("task information")
with col2:
    if st.button("Next step: Chatbot 2", type="primary"):
        switch_page("chatbot 2")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

            
