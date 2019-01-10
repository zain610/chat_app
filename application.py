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
# data like message, channel name, user etcs. in dict format
# server_data = {
#     '121': [{
#         'username': 'Zain',
#         'msg': 'doiasndso'
#     },{
#         'username': 'Aryaan',
#         'msg': 'adkashdbks'
#     }],
#     '29012':[{
#         'username': 'Zain',
#         'msg': 'sasd'
#     },
#     {
#         'username': 'Aryaan',
#         'msg': 'askdakbsj'
#     }]
# }
#
# users = {
#     '121': ['aryaan', 'ain', 'ajsdiasd', 'asdiaygkdha' ],
#     '21uhad': ['kbsfjasf', 'asdaskbjad', 'asdjbakfsa']
# }
# server data like messages in each channel and by which user
server_data = {
    'anthony': []
}
# users in each room
users = {}
# init list to track users JOIN this channel
curr_users = []


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html', message=message )


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
        print("channel name", channel_name)
        if channel_name is not None and channel_name not in channel_list:
            channel_list.append(channel_name)
            server_data[channel_name] = []
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    print('channels', channel_list)
    return render_template('channels.html', action="view", channel_list=channel_list)


@app.route('/messages/<channel>', methods=["POST", "GET"])
def messages(channel):
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
    print(channel)
    return render_template('messages.html', channel=channel)


@socketio.on('join_channel')
def on_join(data):
    '''
    connects a user to the room.
    keeps track of the users in each room 
    records the chat history of the room
    stores the chat history to session so it can be retrieved for later use and keep updating new users on old news

    
    Arguments:
        data {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    '''
    socketio.username = data['username']
    channel = data['channel']
    if socketio.username not in curr_users:
        # make function
        curr_users.append(socketio.username)
        print('added user', socketio.username, 'to ', channel)
    # update users
    users[channel] = curr_users
    print('users in this room', curr_users, 'users in all rooms', users)
    session[channel] = curr_users
    join_room(channel)
    print(server_data[channel])
    dataset = {
        'username': socketio.username,
        'room': channel,
        'user_list': curr_users,
        'saved_messages': server_data[channel]
    }
    # send(dataset['username'] + ' has entered the room.', room=dataset['room'])
    emit('connected_user', dataset, broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('client disconnected')
    emit('leave')


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    channel = data['channel']
    leave_room(channel)

@socketio.on('submit message')
def message(data):

    print('data=>', data)
    (username, channel, message) = data.values()
    print(username, channel, message)
    server_data[data['channel']].append({ 'username': username, 'message': message })
    print(server_data[channel])
    emit('announce message', data, broadcast=True)


@app.route('/API/channels', methods=['POST'])
def query_channels():
    return jsonify(channel_list), 200


@app.route('/API/<channel_name>/users', methods=['POST'])
def query_users(channel_name):
    data = users[channel_name]
    return jsonify(data), 200

@app.route('/API/<channel_name>/messages', methods=['POST'])
def query_msg(channel_name):
    data = server_data[channel_name]
    return jsonify(data), 200
if __name__ == '__main__':
    socketio.run(app, debug=True)


'''
To-Do:
 1. Storing chat history.
  -  store all messages under channel name in the server. when a new user joins the channel, he is able to read all messages
  - store only messages and channel
 2. Timestamps:
 - import moment.js and use it to create time stamps for each message
  - add time stamp next to each message
 3. USer disconnects.
  - When user closes tab, disconnect
  - this means that the user is removed from active users list and

 */
'''
