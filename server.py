from flask import Flask, request, abort
from time import time
from datetime import datetime
dateformat = '%Y.%m.%d'
app = Flask(__name__)
db = [{'name': "Valent",
       'text': "Hello, it is test message",
       'time': time()},
      {'name': "Amadeus",
       'text': "Hello, hello, it is fine",
       'time': time()}
      ]

@app.route("/")
def hello():
    return "Working..."

@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict) or\
            set(data) != {'name', 'text'}:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or\
            not isinstance(text, str):
        return abort(400)

    message = {
        'name': name,
        'text': text,
        'time': time()
    }
    db.append(message)
    return {'ok': True}

@app.route('/messages')
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}

app.run() #host='0.0.0.0', port=4567