/*
This js file caters functionality to all html files. 
Main takeaways: -> each html attribute needs to be given an unique id 
-> in the form of "#(nameOfPage)(optional::function)(element) eg submit button in index => #indexSubmitBtn or form in index => indexForm"

*/
document.addEventListener('DOMContentLoaded', ()=>{
    // index page submit button clicked = validate form
    const request = new XMLHttpRequest();
    request.open('POST', '/')

    if(!localStorage.getItem('display_name')) {
        document.querySelector('#indexSubmitBtn').onclick = () =>{
            //stores dp in localstorage
            const display_name = document.querySelector('#indexForm').querySelector('#display_name').value
            const data = new FormData();
            data.append('display_name', display_name)
            request.send(data)
            localStorage.setItem('display_name', display_name)

        }
        
    }
    if(localStorage.getItem('display_name')){
        location.href = 'channels/view'
    }
    
    
    
})