if(localStorage.getItem('username') && localStorage.getItem('channel')){
    document.addEventListener('DOMContentLoaded', () => {
        // get username and channel of user
        let channel_list = []
        const username = localStorage.getItem('username');
        const channel = localStorage.getItem('channel');
        let users = localStorage.getItem('users')
        var socket = io.connect(location.protocol + '//' + document.domain + ':'+ location.port)
        socket.on('connect', () => {
            let id = socket.io.engine.id;
            let data = {
                //init data object
                // helps streamline data being sent from one socket to another
                'username': username,
                'channel': channel
            };
            console.log('connected', 'user',username,'to', channel)
            socket.emit('join_channel', data)



            document.getElementById('messageInputBtn').onclick = () => {
                const message = document.getElementById('messageInput').value;
                console.log(message)
                data['message'] = message
                console.log(data)
                socket.emit('submit message', data)
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
    function userLogout(){
        localStorage.clear()
        location.href = '/channels/view'
    }

    function printUsers() {
        users = localStorage.getItem('users')
        const li = document.createElement('li')
        li.innerText = users
        document.querySelector('#userList').innerHTML = li.textContent
    }
}
else{
    location.href='/channels/view'
}