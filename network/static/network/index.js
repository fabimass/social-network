document.addEventListener('DOMContentLoaded', () => {
    
    // Event listener for when the user is typing a new post
    document.querySelector('#newpost').addEventListener('input', () => calculate_remaining_chars());
    
});

const calculate_remaining_chars = () => {

    const newpost = document.querySelector('#newpost').value;
    const span = document.querySelector('#charsleft');
    const max_length = parseInt(document.querySelector('#maxlength').value);
    const remaining_chars = max_length - newpost.length;
    span.innerHTML = `${remaining_chars} characters left`;
}