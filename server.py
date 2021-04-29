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
            set(user) != {'name', 'password'}:
        return abort(400)

    name = user['name']
    password = user['password']
    if not isinstance(name, str) and isinstance(password, str):
        return abort(400)
    result_check_password = check_password(password=password)
    if not result_check_password['result']:
        return {'password': result_check_password['notice']}

    confirm_added = db.add_user(name=name, password=password)
    if confirm_added:
        return {'user_id': db.get_user_id(name=name, password=password)}
    else:
        return {'user_id': None}


def check_password(password: str) -> dict:
    result = {'result': True, 'notice': 'ok'}
    if len(password) < 8:
        result = {'result': False, 'notice': 'smallpassword'}
    elif password.isdigit():
        result = {'result': False, 'notice': 'needletter'}
    elif password == password.lower():
        result = {'result': False, 'notice': 'needupper'}
    elif password == password.upper():
        result = {'result': False, 'notice': 'needlower'}
    return result

@app.route("/sing_in", methods=['GET'])
def sing_in():
    try:
        name = request.args['name']
        password = request.args['password']
    except:
        return abort(400)

    return {'user_id': db.get_user_id(name=name, password=password)}


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict) or \
            set(data) != {'chat_id', 'user_id', 'text'}:
        return abort(400)

    chat_id = data['chat_id']
    user_id = data['user_id']
    text = data['text']

    if not isinstance(chat_id, int) or not isinstance(user_id, int) or not isinstance(text, str):
        return abort(400)
    db.add_message(chat_id=chat_id, user_id=user_id, text=text)
    return {'ok': True}


@app.route('/messages')
def get_messages():
    try:
        last_time = request.args['last_time']
        user_id = request.args['user_id']
    except:
        return abort(400)

    result = []
    messages = db.get_messages(user_id=user_id)
    if messages is None:
        result = None
    else:
        for message in messages:
            if is_date_be_before(message['time'], last_time):
                result.append(message)
                if len(result) >= 100:
                    break
    return {'messages': result, 'time': db.get_now_time()}


@app.route('/create_chat')
def create_chat():
    try:
        user1_id = request.args['user1_id']
        user2_id = request.args['user2_id']
    except:
        return abort(400)

    result = db.add_chat_if_not_exist(user1_id=user1_id, user2_id=user2_id)

    if result is not None:
        return abort(400)


@app.route('/chat_id')
def get_chat_id():
    try:
        user_id = request.args['user_id']
        contact_id = request.args['contact_id']
    except:
        return abort(400)

    result = db.add_chat_if_not_exist(user1_id=user_id, user2_id=contact_id)
    return {'chat_id': result}


@app.route('/add_contact', methods=['POST'])
def add_contact():
    users = request.json
    if not isinstance(users, dict) or set(users) != {'user_id', 'contact_name', 'contact_id'}:
        return abort(400)

    user_id = users['user_id']
    contact_name = users['contact_name']
    contact_id = users['contact_id']

    if not isinstance(user_id, int) \
            or not isinstance(contact_name, str) and not contact_name is None\
            or not isinstance(contact_id, int) and not contact_id is None:
        return abort(400)

    result = db.add_contact(user_id=user_id, contact_name=contact_name, contact_id=contact_id)
    if set(result) == {'result', 'contact_id', 'contact_name'}:
        return {'result': result['result'], 'contact_id': result['contact_id'], 'contact_name': result['contact_name']}
    else:
        return {'result': result['result'], 'contact_id': None, 'contact_name': None}


@app.route('/contacts')
def contacts():
    try:
        user_id = int(request.args['user_id'])
    except:
        return abort(400)

    if not isinstance(user_id, int):
        return abort(400)

    contacts_id = db.get_contacts(user_id=user_id)
    if contacts_id is None:
        return {'contacts': None}
    contacts = []
    for contact_id in contacts_id:
        name = db.get_user(contact_id)
        contacts.append((contact_id, name))
    return {'contacts': contacts}


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


app.run()  # host='0.0.0.0', port=4567
