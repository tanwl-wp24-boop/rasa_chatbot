import streamlit as st
import requests
import uuid
import time
import pandas as pd
import os


# ==============================
# Rasa API Configuration
# ==============================

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"


# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="Gym and Fitness Chatbot",
    page_icon="🤖💪",
    layout="centered"
)


# ==============================
# Session Management
# ==============================

if "sender_id" not in st.session_state:
    st.session_state.sender_id = str(uuid.uuid4())


if "messages" not in st.session_state:
    st.session_state.messages = []



# ==============================
# Header
# ==============================

col1, col2 = st.columns([8, 1])


with col1:

    st.title("🤖 Gym and Fitness Chatbot")

    st.caption(
        "Your AI fitness assistant that recommends exercises based on "
        "body part, equipment, and difficulty level."
    )


with col2:

    st.write("")

    if st.button("🗑"):

        st.session_state.messages = []

        st.session_state.sender_id = str(uuid.uuid4())

        st.rerun()



st.divider()



# ==============================
# Display Chat History
# ==============================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])



# ==============================
# User Input
# ==============================

user_input = st.chat_input(
    "Example: Recommend beginner chest exercises using dumbbells"
)



if user_input:


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.chat_message("user"):

        st.write(user_input)



    try:

        start_time = time.time()


        response = requests.post(

            RASA_URL,

            json={
                "sender": st.session_state.sender_id,
                "message": user_input
            },

            timeout=10

        )


        response_time = round(
            time.time() - start_time,
            2
        )


        response.raise_for_status()


        rasa_response = response.json()



        if rasa_response:


            for item in rasa_response:


                if "text" in item:


                    bot_text = item["text"]


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": bot_text
                        }
                    )


                    with st.chat_message("assistant"):

                        st.write(bot_text)



            st.caption(
                f"⚡ Response time: {response_time}s"
            )



        else:


            bot_text = (
                "Sorry, I could not understand your request. "
                "Please try again."
            )


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": bot_text
                }
            )


            with st.chat_message("assistant"):

                st.warning(bot_text)



    except requests.exceptions.ConnectionError:


        st.error(
            """
            ❌ Cannot connect to Rasa server.

            Please run:

            1. rasa run actions

            2. rasa run --enable-api
            """
        )


    except requests.exceptions.Timeout:


        st.error(
            "⏳ Rasa response timeout."
        )


    except Exception as e:


        st.error(
            f"Unexpected error: {e}"
        )



# ==============================
# Feedback
# ==============================

st.divider()


st.subheader("⭐ Rate Your Experience")


rating = st.slider(

    "How useful was the chatbot recommendation?",

    1,

    5,

    5

)



if st.button("Submit Feedback"):


    feedback_file = "feedback.csv"


    new_feedback = pd.DataFrame(
        [
            {
                "sender_id": st.session_state.sender_id,
                "rating": rating
            }
        ]
    )


    if os.path.exists(feedback_file):

        old_feedback = pd.read_csv(feedback_file)

        new_feedback = pd.concat(
            [
                old_feedback,
                new_feedback
            ],
            ignore_index=True
        )


    new_feedback.to_csv(
        feedback_file,
        index=False
    )


    st.success(
        "Thank you for your feedback!"
    )
