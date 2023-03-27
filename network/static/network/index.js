document.addEventListener('DOMContentLoaded', () => {
    
    // Event listener for when the user is typing a new post
    document.querySelector('#newpost').addEventListener('input', () => calculate_remaining_chars());

    // Event listener for likes
    document.querySelectorAll('.likes').forEach((element) => element.addEventListener('click', (event) => like(event.target)));
    
});

const calculate_remaining_chars = () => {

    const newpost = document.querySelector('#newpost').value;
    const span = document.querySelector('#charsleft');
    const max_length = parseInt(document.querySelector('#maxlength').value);
    const remaining_chars = max_length - newpost.length;
    span.innerHTML = `${remaining_chars} characters left`;
}

const like = (target) => {

    fetch(`likes/${target.id}`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(result => {
        
        // Update likes count in the page
        target.innerHTML = `${(result.status) ? '&#10084;' : '&#9825;'} ${result.count}` 
    });
}