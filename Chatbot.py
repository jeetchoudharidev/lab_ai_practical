
import re
import random
import nltk

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# NLP preprocessing tool
stemmer = PorterStemmer()


def preprocess(text):
    """Clean, tokenize and stem user input."""
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return " ".join(stemmer.stem(word) for word in words)


# Predefined intents, example questions and responses
intents = {
    "greeting": {
        "patterns": [
            "hello", "hi", "hey", "good morning",
            "good evening", "howdy"
        ],
        "responses": [
            "Hello! How can I help you?",
            "Hey there! What would you like to know?",
            "Hi! Nice to talk to you."
        ]
    },

    "name": {
        "patterns": [
            "what is your name",
            "who are you",
            "tell me your name",
            "what should I call you"
        ],
        "responses": [
            "I am a Python-based AI chatbot.",
            "You can call me ChatBot!",
            "I am your virtual assistant."
        ]
    },

    "wellbeing": {
        "patterns": [
            "how are you",
            "how are you doing",
            "are you fine",
            "how is your day"
        ],
        "responses": [
            "I am doing great! How about you?",
            "I am fine, thanks for asking!",
            "Everything is running smoothly!"
        ]
    },

    "course": {
        "patterns": [
            "tell me about my course",
            "what subjects do I study",
            "give me course information",
            "what is my subject",
            "help me with my studies"
        ],
        "responses": [
            "I can help with basic course-related questions.",
            "Tell me the subject you want to learn about.",
            "Which topic are you studying currently?"
        ]
    },

    "help": {
        "patterns": [
            "help me",
            "what can you do",
            "how can you help me",
            "what are your features"
        ],
        "responses": [
            "I can answer questions about greetings, my name, "
            "course information and general topics.",
            "Try asking me a question in your own words!"
        ]
    },

    "thanks": {
        "patterns": [
            "thank you",
            "thanks",
            "thanks a lot",
            "I appreciate your help"
        ],
        "responses": [
            "You're welcome!",
            "Happy to help!",
            "Anytime! Let me know if you need more help."
        ]
    },

    "goodbye": {
        "patterns": [
            "bye",
            "goodbye",
            "see you later",
            "exit",
            "quit"
        ],
        "responses": [
            "Goodbye! Have a nice day.",
            "See you again!",
            "Take care!"
        ]
    }
}


# Prepare example questions for similarity matching
training_patterns = []
pattern_intents = []

for intent, data in intents.items():
    if intent == "goodbye":
        continue

    for pattern in data["patterns"]:
        training_patterns.append(preprocess(pattern))
        pattern_intents.append(intent)


# Convert text into numerical TF-IDF vectors
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
training_vectors = vectorizer.fit_transform(training_patterns)


def chatbot_response(user_input):
    text = user_input.lower().strip()

    if not text:
        return "Please enter a message."

    # Handle exit commands first
    if re.fullmatch(
        r"(bye|goodbye|exit|quit|see you later)[.! ]*",
        text
    ):
        return random.choice(intents["goodbye"]["responses"])

    # Rule-based pattern matching
    tokens = set(re.findall(r"\b[a-z]+\b", text))

    if tokens.intersection({"hello", "hi", "hey", "howdy"}):
        return random.choice(intents["greeting"]["responses"])

    if "thank" in tokens or "thanks" in tokens:
        return random.choice(intents["thanks"]["responses"])

    # NLP preprocessing
    processed_input = preprocess(text)

    # Convert input into a TF-IDF vector
    input_vector = vectorizer.transform([processed_input])

    # Find the most similar predefined question
    similarities = cosine_similarity(
        input_vector, training_vectors
    )[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    # Minimum similarity threshold
    if best_score >= 0.30:
        matched_intent = pattern_intents[best_index]
        return random.choice(
            intents[matched_intent]["responses"]
        )

    return (
        "Sorry, I couldn't understand that. "
        "Could you ask in a different way?"
    )


# Main conversation loop
print("=" * 45)
print("       WELCOME TO PYTHON CHATBOT")
print("=" * 45)
print("Ask me something! Type 'bye' to exit.\n")

while True:
    user_input = input("You: ")

    response = chatbot_response(user_input)
    print("Chatbot:", response)

    if re.fullmatch(
        r"\s*(bye|goodbye|exit|quit|see you later)[.! ]*\s*",
        user_input.lower()
    ):
        break
