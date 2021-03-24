from flask import Flask, request, abort
from datetime import datetime
from db_server import DB
db = DB()
dateformat = db.dateformat

app = Flask(__name__)

@app.route("/")
def hello():
    return "Working..."

@app.route("/sing_up", methods=['POST'])
def sing_up():
    user = request.json
    if not isinstance(user, dict) or \
            set(user) != {'name'}:
        return abort(400)

    name = user['name']

    if not isinstance(name, str):
        return abort(400)
    confirm_added = db.add_user(name)
    user_id = None
    if confirm_added:
        user_id = db.get_user_id(name)
    print(user_id)
    return {'user_id': user_id}

@app.route("/sing_in", methods=['GET'])
def sing_in():
    try:
        name = request.args['name']
    except:
        return abort(400)

    return {'user_id': db.get_user_id(name)}


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

    return {'ok': True}

@app.route('/messages')
def get_messages():
    try:
        last_time = request.args['last_time']
        user_id = request.args['user_id']
    except:
        return abort(400)

    result = []
    for message in db.get_messages(user_id=user_id, last_time=last_time):
        if is_date_be_before(message['time'], last_time):
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}

@app.route('/create_chat')
def create_chat():
    try:
        user1_id = request.args['user1_id']
        user2_id = request.args['user2_id']
    except:
        return abort(400)

    result = db.add_chat(user1_id=user1_id, user2_id=user2_id)

    if result is not None:
        return abort(400)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    users = request.json
    if not isinstance(users, dict) or set(users) != {'user_id', 'contact_name'}:
        return abort(400)

    user_id = users['user_id']
    contact_name = users['contact_name']

    if not isinstance(user_id, int) or not isinstance(contact_name, str):
        return abort(400)

    result = db.add_contact(user_id=user_id, contact_name=contact_name)
    if result['result'] == 'is_your_name':
        return {'request': 'is_your_name'}
    if result['result'] == 'is_not_exist':
        return {'request': 'contact_is_not_exist'}
    if result['result'] == 'is_in_contacts':
        return {'request': 'contact_is_in_contacts'}
    return {'request': 'ok'}

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