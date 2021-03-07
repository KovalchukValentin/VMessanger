from flask import Flask, request, abort
from datetime import datetime
dateformat = '%d-%m-%Y %H:%M:%S:%f'
app = Flask(__name__)
db = [{'name': "Valent",
       'text': "Hello, it is test message",
       'time': datetime.now().strftime(dateformat)}
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
        'time': datetime.now().strftime(dateformat)
    }
    db.append(message)
    return {'ok': True}

@app.route('/messages')
def get_messages():
    try:
        after = request.args['after']
    except:
        return abort(400)

    result = []
    for message in db:
        if is_date_be_before(message['time'], after):
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}

def is_date_be_before(date, check_date):
    date, check_date = date.split(), check_date.split()
    date = date[0].split("-")[::-1] + date[1].split(":")
    check_date = check_date[0].split("-")[::-1] + check_date[1].split(":")
    for i in range(len(date)):
        if int(date[i]) > int(check_date[i]):
            return True
        if int(date[i]) == int(check_date[i]):
            continue
        return False
    return False




app.run() #host='0.0.0.0', port=4567