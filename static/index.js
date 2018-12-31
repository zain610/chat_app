/*
This js file caters functionality to all html files. 
Main takeaways: -> each html attribute needs to be given an unique id 
-> in the form of "#(nameOfPage)(optional::function)(element) eg submit button in index => #indexSubmitBtn or form in index => indexForm"

*/
document.addEventListener('DOMContentLoaded', ()=>{

    if(!localStorage.getItem('username')) {
        document.querySelector('#indexSubmitBtn').onclick = () =>{
            //stores dp in localstorage
            const username = document.querySelector('#indexForm').querySelector('#display_name').value
            localStorage.setItem('username', username)
        } 
    }
    location.href = '/channels/view'
    
})