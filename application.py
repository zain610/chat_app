import os
import requests
from flask import Flask, render_template, request, redirect, url_for, redirect, jsonify, session
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

channel_list = ["anthony"]
# data like message, channel name, user etcs
server_data = []
# total user list
user_list = []
# users in each room
users = [] 

@app.route("/", methods=["POST", "GET"])
def index():
    message = "Hello, Please Enter your display name"
    return render_template('index.html', message = message, users =user_list)
    
        
@app.route('/channels/<action>', methods=["POST", "GET"])
def channels(action):
    '''
    Channels route => default is channels/view, form submitted to channels/add
    
    Arguments:
        action {str} -- view/add
    
    Returns:
        html file
    '''

    print(action)
    

    if action == "add":
        channel_name = request.form.get("name")
        username = request.form.get('username')
        print("channel name", channel_name, 'username', username)
        if((channel_name and username) is not None and (channel_name not in channel_list) and (username not in user_list)):
            # maybe create setters and getters for channels and users??
            channel_list.append(channel_name)
            session['channel_list'] = channel_list
            user_list.append(username)
            session['user_list'] = user_list
            return jsonify({"success": True})
        return jsonify({"success": False})
    return render_template('channels.html', action="view", data=session.get('channels'))


@app.route('/messages/<channel>', methods=["POST", "GET"])
def messages(channel):
    print('users in this room', users)
    return render_template('messages.html')

@socketio.on('join')
def on_join(data):
    
    socketio.username = data['username']

    print(socketio.username)
    if socketio.username is not None:
        users.append(socketio.username)
    print('users in this room', users)
    room = data['channel']
    print(user_list)
    session[room] = user_list
    join_room(room)
    dataset={'username': socketio.username, 'room': room, 'user_list': session[room]}
    emit('join', dataset, broadcast=True)
    

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     channel = data['channel']
#     leave_room(channel)
#     session[room].pop()
#     dataset = {'username': username, 'room': room}

@socketio.on('submit message')
def message(data):
    server_data.append(data)
    print(server_data)
    emit('announce message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)