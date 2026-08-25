import streamlit as st
import pandas as pd
import uuid
import os


# Page setup
st.set_page_config(
    page_title="Gym and Fitness Chatbot",
    page_icon="🤖💪"
)


st.title("🤖 Gym and Fitness Chatbot")


# Create unique conversation ID
if "sender_id" not in st.session_state:
    st.session_state.sender_id = str(uuid.uuid4())


# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Load dataset
@st.cache_data
def load_data():

    file_path = "dataset/MegaGymDataset.csv"

    df = pd.read_csv(file_path)

    return df


try:
    df = load_data()

except Exception as e:
    st.error("Dataset cannot be loaded.")
    st.write(e)
    st.stop()



# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



# Recommendation function
def recommend_exercise(user_message):

    message = user_message.lower()

    result = df.copy()


    # Filter body part
    body_parts = [
        "chest",
        "back",
        "legs",
        "shoulders",
        "biceps",
        "triceps",
        "abs"
    ]


    selected_body = None

    for body in body_parts:

        if body in message:
            selected_body = body
            break



    if selected_body:

        if "bodyPart" in result.columns:

            result = result[
                result["bodyPart"]
                .astype(str)
                .str.lower()
                .str.contains(selected_body)
            ]



    # Return recommendation

    if len(result) > 0:

        sample = result.sample(
            min(3, len(result))
        )


        response = "Here are some recommended exercises:\n\n"


        for _, row in sample.iterrows():

            if "Title" in row:

                response += f"💪 {row['Title']}\n"

            elif "title" in row:

                response += f"💪 {row['title']}\n"

            else:

                response += f"💪 {row.iloc[0]}\n"



        return response


    else:

        return (
            "I could not find a suitable exercise. "
            "Try asking with a body part, for example: "
            "'Recommend chest exercises'."
        )



# User input

user_input = st.chat_input(
    "Type your message..."
)



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



    # Generate answer

    bot_response = recommend_exercise(
        user_input
    )



    # Display bot response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response
        }
    )


    with st.chat_message("assistant"):
        st.write(bot_response)
