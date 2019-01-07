import * as moment from 'src/moment.js';
if(localStorage.getItem('username') && localStorage.getItem('channel')){
    document.addEventListener('DOMContentLoaded', () => {
        // get username and channel of user
        console.log(moment())
        let channel_list = []
        const username = localStorage.getItem('username');
        const channel = localStorage.getItem('channel');
        let users = localStorage.getItem('users')
        var socket = io.connect(location.protocol + '//' + document.domain + ':'+ location.port)
        socket.on('connect', () => {
            let data = {
                //init data object
                // helps streamline data being sent from one socket to another
                'username': username,
                'channel': channel,
            };
            console.log('connected', 'user',username,'to', channel)
            socket.emit('join_channel', data)



            document.getElementById('messageInputBtn').onclick = () => {
                const message = document.getElementById('messageInput').value;

                data['message'] = message
                console.log('message submitted', data['message'])
                //Send message event
                socket.emit('submit message', data)
                document.getElementById('messageInput').value = "";
            };
        });
        socket.on('connected_user', data=>{
            console.log(data)
            channel_list = data.user_list
            console.log('users in this room =>', channel_list)
            const li = document.createElement('li');
            li.innerHTML = `${data.username} has joined the room: ${data.room}`
            document.querySelector('#messages').append(li)
            localStorage.setItem('users', channel_list)
            printUsers()

        });

        socket.on('announce message', data=>{
            const li = document.createElement('li');
            li.innerHTML = `Message recorded: ${data.message} by ${data.username}`;
            document.querySelector('#messages').append(li)
        })
        socket.on('new_user', username=>{
            console.log(username + '  added successfully')
        })
        socket.on('user_leave', data=>{
            console.log(data)
            channel
        })

    });
    // noinspection JSAnnotator
    function userLogout(){
        localStorage.clear()
        location.href = '/channels/view'
    }

    // noinspection JSAnnotator
    function printUsers() {
        let users = localStorage.getItem('users')
        const li = document.createElement('li')
        li.innerText = users
        document.querySelector('#userList').innerHTML = li.textContent
    }
}
else{
    location.href='/channels/view'
}


/**
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