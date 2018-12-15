document.addEventListener('DOMContentLoaded', () =>{
    const form = document.getElementById('channelAddForm')
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
                document.getElementById('result').innerHTML = contents
            }
            else{
                const contents = "there was an error, please try again!"
                document.getElementById('result').innerHTML = contents;
            }
            location.reload()
        }
        // Add data to send with request
        const data = new FormData();
        data.append('name', name );
        // Send request
        request.send(data)
        return false;
    })
})
