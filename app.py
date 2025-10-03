from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Streamlit Chat", page_icon=":speech_balloon:")
st.title("Chatbot")

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

if not st.session_state.setup_complete:

    st.subheader("Personal information", divider="rainbow")

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    st.session_state["name"] = st.text_input(label="Name", max_chars=40,value=st.session_state["name"], placeholder="Enter your name")

    st.session_state["experience"] = st.text_area(label="Experience", value= st.session_state["experience"], height=200, max_chars=None, placeholder="Describe your experience")

    st.session_state["skills"] = st.text_area(label="Skills", value= st.session_state["skills"], height=None, max_chars=200, placeholder="List your skills")


    st.subheader("Company and Position", divider="rainbow")

    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key="visibility",
            options=["Junior", "Mid-level", "Senior"]
        )

    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose a position",
            ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))
    st.session_state["company"] = st.selectbox(
        "Choose a Company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
    )
    st.write(f"**Your Information**: {st.session_state["level"]} {st.session_state["position"]} at {st.session_state["company"]} ")

    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")

if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    st.info(
        """
        Start by introducing yourself
        """,
        icon = "👏"
    )

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if not st.session_state.messages:
        st.session_state.messages = [{"role": "system",
                                      "content": f"You are an HR executive that interviews an interviewee called {st.session_state["name"]}"
                                                 f"with experience {st.session_state["experience"]} and skills {st.session_state["skills"]}."
                                                 f"You should interview them for the position {st.session_state["level"]} {st.session_state["position"]}"
                                                 f"at the company {st.session_state["company"]}."}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.user_message_count < 5:
        if prompt := st.chat_input("Your answer.", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            if st.session_state.user_message_count < 5:
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model= st.session_state["openai_model"],
                        messages = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream = True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.user_message_count +=1
    if st.session_state.user_message_count >=5:
        st.session_state.chat_complete = True

if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get feedback", on_click=show_feedback):
        st.write("Fetching feedback...")
if st.session_state.feedback_shown:
    st.subheader("Feedback")
    conversation_history = "\n".join([f"{m["role"]} : {m["content"]}" for m in st.session_state.messages])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    feedback_completion = feedback_client.chat.completions.create(
        model = "gpt-4o",
        messages = [{"role": "system",
                     "content": """You are a helpful tool that provides feedback on an interviewee performance.
                     Before a feedback give a score od 1 ro10.
                     Follow this format:
                     Overall Score: // Your score
                     Feedback:// Here put your feedback
                     Give only feedback do not ask any additional questions
                     """},
                    {"role": "user",
                     "content": f"This is the interview you need to evaluate. Keep in mind that you are only a tool"
                                f"and you shouldn't engage in conversation: {conversation_history}"}]
    )
    st.write(feedback_completion.choices[0].message.content)
    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")