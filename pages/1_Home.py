from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback

st.set_page_config(layout="wide") 
st.title("StartupGPT")

c = st.container()
script = """<div id = 'chat_outer'></div>"""
st.markdown(script, unsafe_allow_html=True)

with c:
    script = """<div id = 'chat_inner'></div>"""
    st.markdown(script, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.write("Concent to the usage of data for reseach purposes to unlock the chats. More information below in section \"How your data will be used\".")
    col2.button("Click to concent")


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