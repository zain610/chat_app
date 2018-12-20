import os
import requests
from flask import Flask, render_template, request, redirect, url_for, redirect, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'secret!'
socketio = SocketIO(app)

channel_list = ["anthony"]
user_list = []
server_data = []

@app.route("/", methods=["POST", "GET"])
def index():
    user_name = request.form.get('display_name')
    print(user_name)
    user_list.append(user_name) 
    print(user_list)

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
            print(channel_list, channel_name )
            return jsonify({"success": True})
        return jsonify({"success": False})
    return render_template('channels.html', action="view", data=channel_list)
    
@app.route('/messages/<channel>', methods=["POST", "GET"])
def messages(channel):
    return render_template('messages.html', channel=channel)

@socketio.on('join')
def on_join(data):
    socketio.username = data['username']
    room = data['channel']
    join_room(room)
    dataset={'username': socketio.username, 'room': room}
    print(socketio.rooms[''][room])
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