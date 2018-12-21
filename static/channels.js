document.addEventListener('DOMContentLoaded', () =>{
    const form = document.getElementById('channelAddForm')
    // if(localStorage.getItem('channel')) {
    //     location.href = '../messages/' + localStorage.getItem('channel')
    // }
    const username = prompt('Please Enter a username')

    // 

    form.addEventListener('submit', ()=>{
        const name = form.querySelector('#channelsAddName').value
        const request = new XMLHttpRequest();
        request.open('POST', '/channels/add');
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
        }
        // Add data to send with request
        const data = new FormData();
        data.append('name', name );
        data.append('username', username)
        // Send request
        request.send(data)
        return false;
    })
})
function enterChannel(name) {
    console.log(name)
    localStorage.setItem('channel', name)
    window.location.href = '../messages/'+ name
}