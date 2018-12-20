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
user_list = []
server_data = []

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
        print("channel name", channel_name)
        if(channel_name is not None and (channel_name not in channel_list)):
            channel_list.append(channel_name)
            session['channels'] = channel_list
            return jsonify({"success": True})
        return jsonify({"success": False})
    return render_template('channels.html', action="view", data=session.get('channels'))
    
@app.route('/messages/<channel>', methods=["POST", "GET"])
def messages(channel):
    return render_template('messages.html', channel=channel)

@socketio.on('join')
def on_join(data):
    username = data['username']
    print(user_list)
    room = data['channel']
    session[room].append(username)
    join_room(room)
    dataset={'username': username, 'room': room}
    emit('test', dataset, broadcast=True)
    

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    channel = data['channel']
    leave_room(channel)
    send(username + ' has left the room.', room=channel)

@socketio.on('submit message')
def message(data):
    server_data.append(data)
    print(server_data)
    emit('announce message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)