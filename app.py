import streamlit as st
import requests
import uuid


# Rasa REST API URL
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"


# Page setup
st.set_page_config(
    page_title="Gym and Fitness Chatbot",
    page_icon="🤖💪💪"
)


st.title("🤖 Gym and Fitness Chatbot")


# Create unique conversation ID
if "sender_id" not in st.session_state:
    st.session_state.sender_id = str(uuid.uuid4())


# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



# User input box
user_input = st.chat_input("Type your message...")


if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.chat_message("user"):
        st.write(user_input)



    # Send message to Rasa
    response = requests.post(
        RASA_URL,
        json={
            "sender": st.session_state.sender_id,
            "message": user_input
        }
    )


    rasa_response = response.json()



    # Display bot response
    if rasa_response:

        for message in rasa_response:

            if "text" in message:

                bot_text = message["text"]


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_text
                    }
                )


                with st.chat_message("assistant"):
                    st.write(bot_text)

    else:

        st.warning("No response from Rasa")