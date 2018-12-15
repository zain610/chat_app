import os
import requests
from flask import Flask, render_template, request, redirect, url_for, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel_list = ["anthony"]

@app.route("/", methods=["POST", "GET"])
def index():
    message = "Hello, Please Enter your display name"
    return render_template('index.html', message = message)


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
        if(channel_name is not None and type(channel_name) is str and (channel_name not in channel_list)):
            channel_list.append(channel_name)
            print(channel_list, channel_name )
            return jsonify({"success": True})
        return jsonify({"success": False})
    return render_template('channels.html', action="view", data=channel_list)
    
# @app.route('/messages/<channel>', methods=["POST", "GET"])
# def messages(channel):
