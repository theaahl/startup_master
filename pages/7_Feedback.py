import streamlit as st

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
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("option", c3_option_2, "text")

