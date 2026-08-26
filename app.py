import streamlit as st
import pandas as pd
import uuid


# Page setup
st.set_page_config(
    page_title="Gym and Fitness Chatbot",
    page_icon="🤖💪"
)


st.title("🤖 Gym and Fitness Chatbot")


# Session
if "sender_id" not in st.session_state:
    st.session_state.sender_id = str(uuid.uuid4())


if "messages" not in st.session_state:
    st.session_state.messages = []



# Load dataset
@st.cache_data
def load_data():

    return pd.read_csv(
        "dataset/megaGymDataset.csv"
    )


try:

    df = load_data()

except Exception as e:

    st.error("Dataset cannot be loaded")
    st.write(e)
    st.stop()



# Show history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])



# -----------------------------
# Intent detection
# -----------------------------

def detect_intent(message):

    message = message.lower()


    greetings = [
        "hi",
        "hello",
        "hey"
    ]


    if any(word in message for word in greetings):

        return "greeting"



    fitness_words = [
        "exercise",
        "workout",
        "gym",
        "fitness",
        "train",
        "training",
        "muscle",
        "strength",
        "lift",
        "routine"
    ]


    if any(word in message for word in fitness_words):

        return "fitness"



    return "unknown"




# -----------------------------
# Extract information
# -----------------------------

def extract_body_part(message):

    body_parts = {

        "chest": [
            "chest",
            "pec",
            "pecs"
        ],

        "back": [
            "back",
            "lat",
            "lats"
        ],

        "legs": [
            "leg",
            "quad",
            "hamstring"
        ],

        "shoulders": [
            "shoulder",
            "delts"
        ],

        "biceps": [
            "bicep"
        ],

        "triceps": [
            "tricep"
        ],

        "abs": [
            "abs",
            "core"
        ]
    }


    for body, keywords in body_parts.items():

        for word in keywords:

            if word in message:

                return body


    return None



def extract_equipment(message):

    equipment = {

        "dumbbell": [
            "dumbbell",
            "db"
        ],

        "barbell": [
            "barbell"
        ],

        "machine": [
            "machine"
        ],

        "bodyweight": [
            "bodyweight",
            "no equipment"
        ]

    }


    for item, keywords in equipment.items():

        for word in keywords:

            if word in message:

                return item


    return None



def extract_level(message):

    levels = [
        "beginner",
        "intermediate",
        "advanced"
    ]


    for level in levels:

        if level in message:

            return level


    return None




# -----------------------------
# Recommendation
# -----------------------------

def recommend_exercise(user_message):

    message = user_message.lower()

    result = df.copy()


    body = extract_body_part(message)

    equipment = extract_equipment(message)

    level = extract_level(message)



    response = "Here are your recommended exercises:\n\n"



    # body filtering

    if body and "bodyPart" in result.columns:

        result = result[
            result["bodyPart"]
            .astype(str)
            .str.lower()
            .str.contains(body)
        ]



    # equipment filtering

    if equipment and "Equipment" in result.columns:

        result = result[
            result["Equipment"]
            .astype(str)
            .str.lower()
            .str.contains(equipment)
        ]



    if len(result) == 0:

        return (
            "I could not find an exact match 😅\n"
            "Try asking something like:\n"
            "'Beginner chest workout with dumbbells'"
        )



    sample = result.sample(
        min(3, len(result))
    )



    for _, row in sample.iterrows():

        if "Title" in row:

            response += f"💪 {row['Title']}\n"

        elif "title" in row:

            response += f"💪 {row['title']}\n"

        else:

            response += f"💪 {row.iloc[0]}\n"



    return response




# -----------------------------
# Chat
# -----------------------------

user_input = st.chat_input(
    "Type your message..."
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



    intent = detect_intent(
        user_input
    )


    if intent == "greeting":

        bot_response = (
            "Hello! 👋\n\n"
            "I am your Gym and Fitness Assistant 💪\n"
            "Ask me for workout recommendations!"
        )


    elif intent == "fitness":

        bot_response = recommend_exercise(
            user_input
        )


    else:

        bot_response = (
            "I am a Gym and Fitness Assistant 💪\n\n"
            "I can help you with:\n"
            "• Exercise recommendations\n"
            "• Workout ideas\n"
            "• Muscle training\n\n"
            "Try asking:\n"
            "'Recommend chest exercises'"
        )



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response
        }
    )


    with st.chat_message("assistant"):

        st.write(bot_response)
