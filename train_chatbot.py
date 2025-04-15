import json
import pickle
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import tensorflow as tf
from tensorflow import keras

nltk.download("punkt")
lemmatizer = WordNetLemmatizer()

with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

words, labels, docs_x, docs_y = [], [], [], []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])
    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = sorted(set([lemmatizer.lemmatize(w.lower()) for w in words if w not in ["?", ".", "!"]]))

training, output = [], []
out_empty = [0] * len(labels)

for x, doc in enumerate(docs_x):
    bag = [1 if w in [lemmatizer.lemmatize(word.lower()) for word in doc] else 0 for w in words]
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    training.append(bag)
    output.append(output_row)

training, output = np.array(training), np.array(output)

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(len(training[0]),)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(training, output, epochs=100, batch_size=8, verbose=1)

model.save("chatbot_model.h5")
pickle.dump((words, labels), open("chatbot_data.pkl", "wb"))

print("✅ Training complete. Model saved to chatbot_model.h5 and data to chatbot_data.pkl")