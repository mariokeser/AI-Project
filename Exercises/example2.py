import streamlit as st


st.title("Nested Buttons example")

if "show_second_button" not in st.session_state:
    st.session_state.show_second_button = False
if "show_third_button" not in st.session_state:
    st.session_state.show_third_button = False
if "clicked_third_button" not in st.session_state:
    st.session_state.clicked_third_button = False

if st.button("First Button"):
    st.session_state.show_second_button = True


if st.session_state.show_second_button:
    st.write("Revealed")
    if st.button("Second Button"):
        st.session_state.show_third_button=True
    if st.session_state.show_third_button:
        st.write("second button clicked")
        if st.button("Third Button"):
            st.session_state.clicked_third_button = True
    if st.session_state.clicked_third_button:
        st.write("third button clicked")
