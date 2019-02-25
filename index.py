import os
import json
import time
import logging
import random
from chatterbot import ChatBot
from chatterbot.response_selection import get_first_response
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.ERROR)

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

chatbot = ChatBot(
    "MentorMateQ&ABot",
    read_only = True,
    logic_adapters = [
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. For more information contact: support@mentormate.com',
            'maximum_similarity_threshold': 0.9
        }
    ],
    response_selection_method = get_first_response
)

GREETING_INPUTS = ("hello", "hi", "greetings", "what's up", "hey")
GREETING_RESPONSES = ["Hi, nice to meet you.", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/': {'status': 200}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def do_POST(self):
        paths = {
            '/chat': {'status': 200}
        }
        self.respond(paths[self.path])


    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if path == '/chat':
            # length = int(self.headers['content-length'])
            # postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)

            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)

            user_response = str(post_body).split('=')[1][:-1].lower()

            if user_response != 'Bye':
                if user_response == 'thanks' or user_response == 'thank you':
                    answer = "You are welcome."
                else:
                    if greeting(user_response) is not None:
                        answer = greeting(user_response)
                    else:
                        answer = chatbot.get_response(user_response).text
            else:
                answer = "Bye!"

            return bytes(json.dumps({"message": answer}), 'UTF-8')
        else:
            f = open(os.getcwd() + '/index.html', 'r').read()
            return bytes(f, 'UTF-8')


    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))