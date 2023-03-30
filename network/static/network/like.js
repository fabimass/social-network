document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.likes').forEach((element) => element.addEventListener('click', (event) => like(event.target)));
    
});


const like = (target) => {
    
    fetch(`${window.location.origin}/likes/${target.id}`, {
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