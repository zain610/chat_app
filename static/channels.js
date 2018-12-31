
document.addEventListener('DOMContentLoaded', () =>{
    const request = new XMLHttpRequest();
    request.open('POST', '/channels/add');
    if (localStorage.getItem('username') == null || !localStorage.getItem('username')) {
        const username = prompt('Please Enter a username')
        localStorage.setItem('username', username)
    }
    
    const form = document.getElementById('channelAddForm')
    form.addEventListener('submit', ()=>{
        const channel = form.querySelector('#channelsAddName').value
        // Add data to send with request
        const channel_data = new FormData();
        channel_data.append('channel', channel );
        // Send request
        request.send(channel_data)
        
        //Callback function for when the request completes
        request.onload = () =>{
            // get json data
            const data = JSON.parse(request.responseText)
            console.log(data)
            if(data.success){
                const contents = "successfully added channel to list";
                alert(contents)
            }
            else{
                const contents = "there was an error, please try again!"
                alert(contents)
            }    
        location.reload()
        return false;
        }
       
    })
})
function enterChannel(name) {
    console.log(name)
    localStorage.setItem('channel', name)
    window.location.href = '../messages/'+ name
}
