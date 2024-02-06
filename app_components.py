import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages

def sidebar_nav(disabeled):
    hide_pages(["All_Tasks", "Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])
    with st.sidebar:
        st.write("Your tasks")
        with st.expander("Task 1", expanded=True):
            if(disabeled):
                st.page_link("pages/6_Task_Information.py", label="Task information", disabled=True, help="Consent to unlock")
                st.page_link("pages/3_Chatbot_1.py", label="Chatbot 1", disabled=True, help="Consent to unlock")
                st.page_link("pages/4_Chatbot_2.py", label="Chatbot 2", disabled=True, help="Consent to unlock")
                st.page_link("pages/5_Feedback.py", label="Feedback", disabled=True, help="Consent to unlock")
            
            else:
                st.page_link("pages/6_Task_Information.py", label="Task information")
                st.page_link("pages/3_Chatbot_1.py", label="Chatbot 1")
                st.page_link("pages/4_Chatbot_2.py", label="Chatbot 2")
                st.page_link("pages/5_Feedback.py", label="Feedback")


def sticky_header(prev_text, current_text, next_text):
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
    header = st.container()
    if(current_text != "Feedback"):
        header.warning('Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information')
    header.header(current_text)
    col1, col2 = header.columns([1,1])
    with col1:
        if(prev_text != "None"):
            if st.button("Previous step: "+prev_text, type="secondary"):
                switch_page(prev_text.lower())
        else:
            if st.button("Previous step: "+prev_text, type="primary", disabled=True):
                switch_page(current_text.lower())
        
    with col2:
        if(next_text != "None"):
            if st.button("Next step: "+next_text, type="primary"):
                switch_page(next_text.lower())
        else:
            if st.button("Next step: "+next_text, type="primary", disabled=True):
                switch_page(current_text.lower())
            

    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)