import os
import logging
import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_first_response

logging.basicConfig(level=logging.ERROR)

chatbot = ChatBot(
    "MentorMateQ&ABot",
    read_only = True,
    storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
    # database_uri = 'sqlite:///database.db',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters = [
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.9
        }
    ],
    response_selection_method = get_first_response
)

trainer = ListTrainer(chatbot)

for file in os.listdir(os.getcwd() + '/MentorMateData'):
    chats = open(os.getcwd() + '/MentorMateData/' + file, 'r').readlines()
    trainer.train(chats)

GREETING_INPUTS = ("hello", "hi", "greetings", "what's up", "hey")
GREETING_RESPONSES = ["Hi, nice to meet you.", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

print("If you want to exit, type Bye!")

while True:
    user_response = input().lower()

    if user_response != 'Bye':
        if user_response == 'thanks' or user_response == 'thank you':
            print(chatbot.name + ": You are welcome.")
        else:
            if greeting(user_response) is not None:
                print(chatbot.name + ": " + greeting(user_response))
            else:
                print(chatbot.name, chatbot.get_response(user_response))
    else:
        print(chatbot.name + ": Bye!")
        break

