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

    Potential Cases;
    1. If user deletes LocalStorage from browser. -> reloading will prompt user for username again and if he enter same username, error follows but the name is registered inside localstorage
    2. If server restarts, -> 
    3. When new user enters site, 
        -> the app shows user list as None, once he enters username, all usernames from session are acquired(check the if action == 'add' section)
        -> 
    '''

    print(action)
    

    if action == "add":
        channel_name = request.form.get("channel")
        username = request.form.get('username')
        print("channel name", channel_name, 'username', username)
        if username is not None and username not in user_list:
            user_list.append(username)
            session['user_list'] = user_list
            return jsonify({'success': True})
        if channel_name is not None and channel_name not in channel_list:
            channel_list.append(channel_name)
            session['channel_list'] = channel_list
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    print('all users', session.get('user_list'), 'channels',session.get('channel_list'))
    data = {'channels': session.get('channel_list'), 'users': session.get('user_list')}
    print('data', data)

    return render_template('channels.html', action="view", data=data)


@app.route('/messages/<channel>', methods=["POST", "GET"])
def messages(data):
    ''' (For now) the initial entry point for a channel/room. The user is directed
    to this when he wants to enter a channel. 

    Redirected from channels/view channel selected
    
    Arguments:
        data {[json]} -- contains all the data passed on from channels. like username and channel name.
        this is needed to 
        - maybe u dont need this since the localstorage stores this data already 

    
    Returns:
        emits an event 'connect' -- this indicates that the username has entered the channel of channelname
        keeps track of the users who have entered this room
    '''

    socketio.emit('connect', data)
    print('users in this room', users)
    return render_template('messages.html')

@socketio.on('connect')
def connect(data):
    users.append(data.username)
    emit('connected')



@socketio.on('join_channel')
def on_join(data):
    '''connects a user to the room. 
    keeps track of the users in each room 
    records the chat history of the room
    stores the chat history to session so it can be retrieved for later use and keep updating new users on old news
    
    
    Arguments:
        data {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''

    if not user_list:
        print('j-as')
        return redirect(url_for('channels', action='view'))
    
    socketio.username = data['username']
    print(socketio.username)
    if socketio.username is not None and socketio.username not in users:
        users.append(socketio.username)
    print('users in this room', users)
    room = data['channel']
    print('all users', user_list)
    session[room] = user_list
    join_room(room)
    dataset={'username': socketio.username, 'room': room, 'user_list': session[room]}
    emit('join', dataset, broadcast=True)
    
@socketio.on('disconnect')
def test_disconnect():
    
    print('client disconnected')

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     channel = data['channel']
#     leave_room(channel)
#     session[channel]
#     dataset = {'username': username, 'room': room}

@socketio.on('submit message')
def message(data):
    server_data.append(data)
    print(server_data)
    emit('announce message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug= True)
