import requests
from pymongo import MongoClient
import datetime
import uuid

# === AI21 API SETUP ===
API_KEY = "0ba6f1ea-e26c-4a52-9efb-ce63cdef50e4"
API_URL = "https://api.ai21.com/studio/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# === MongoDB SETUP ===
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbotDB"]
collection = db["chatHistory"]

# === Generate Unique Session ID ===
session_id = str(uuid.uuid4())  # like: 'e9b3d112-9d12-4e67-9b91-63f...' 

# === Main Chat Function ===
def get_reply(user_input):
    history.append({"role": "user", "content": user_input})

    try:
        collection.insert_one({
            "session_id": session_id,
            "role": "user",
            "message": user_input,
            "timestamp": datetime.datetime.utcnow()
        })
        print(" Saved user message to MongoDB")
    except Exception as e:
        print(" Could not save user message:", e)

    payload = {
        "model": "jamba-large",
        "messages": history
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"].strip()
        history.append({"role": "assistant", "content": reply})

        try:
            collection.insert_one({
                "session_id": session_id,
                "role": "assistant",
                "message": reply,
                "timestamp": datetime.datetime.utcnow()
            })
            print(" Saved assistant message to MongoDB")
        except Exception as e:
            print(" Could not save assistant message:", e)

        return reply
    else:
        print(" API Error:", response.json())
        return "Sorry, something went wrong."


# === Run the Chat Loop ===
if __name__ == "__main__":
    print("🗣️ Chatbot started. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("d Ending session.")
            break
        response = get_reply(user_input)
        print("Assistant:", response)
