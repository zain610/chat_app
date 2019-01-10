if(localStorage.getItem('username') && localStorage.getItem('channel') && localStorage.getItem('channel')!=null){
    document.addEventListener('DOMContentLoaded', () => {
        // get username and channel of user
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
            document.getElementById('channelName').innerText = channel
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
            socket.on('connected_user', data=>{
                channel_list = data.user_list;
                const savedMessages = data.saved_messages;
                console.log('users in this room =>', channel_list, 'saved messages=>', savedMessages);
                const li = document.createElement('li');
                li.innerHTML = `${data.username} has joined the room: ${data.room}`;
                if (savedMessages) {
                    savedMessages.forEach((message)=>{
                        printMessages(message)
                    })
                }
                document.querySelector('#messages').append(li);
                localStorage.setItem('users', channel_list);
                printUsers(channel_list)
            });

            socket.on('announce message', data=>{
                printMessages(data)
            })


            socket.on('new_user', username=>{
                console.log(username + '  added successfully')
            })
            socket.on('user_leave', data=>{
                console.log(data)
                channel
            })

        });

        document.getElementById('userLogout').onclick = () => {
            localStorage.clear()
            location.href = '/channels/view'
        };

        document.getElementById('leaveChannel').onclick = ()=>{
            socket.emit('leave')
            localStorage.removeItem('channel')
            location.href = '/channels/view'
        };

        // noinspection JSAnnotator
        // This type of arrow function is called anonymous function
        let printUsers = (users) => {
            const li = document.createElement('li')
            li.innerText = users
            document.querySelector('#userList').innerHTML = li.textContent
        };
        let printMessages = (data) => {
            const li = document.createElement('li');
            li.innerHTML = `Message recorded: ${data.message} by ${data.username}`;
            document.querySelector('#messages').append(li)
        }
    });
}
else{
    location.href='/channels/view'
}


