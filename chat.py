import numpy as np
import pickle
import random
import json
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import load_model
from db import save_chat_to_db

# Load model and data
model = load_model("chatbot_model.h5")
words, labels = pickle.load(open("chatbot_data.pkl", "rb"))

with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

def bag_of_words(s):
    """Convert user input to bag of words"""
    bag = [0] * len(words)
    s_words = word_tokenize(s.lower())
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)

def get_response(text):
    """Get chatbot response for user input"""
    X_input = np.array([bag_of_words(text)])
    predictions = model.predict(X_input)[0]
    index = np.argmax(predictions)
    tag = labels[index]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            save_chat_to_db(text, response, tag)
            return response
    return "I'm not sure how to respond to that."