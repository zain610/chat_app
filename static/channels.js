
document.addEventListener('DOMContentLoaded', () =>{
    if (localStorage.getItem('username') == null) {
        const username = prompt('Please Enter a username')
        localStorage.setItem('username', username)
    }
    
    const form = document.getElementById('channelAddForm')
    form.addEventListener('submit', ()=>{
        const channel = form.querySelector('#channelsAddName').value
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
        data.append('channel', channel );
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
// function addUser(name){
//     console.log(name)
// }