document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.edit').forEach((element) => element.addEventListener('click', (event) => edit(event.target)));
    
});


const edit = (target) => {
    
    const post = document.querySelector(`#post-${target.id}`);
    
    // Clicked on Edit
    if (target.innerHTML == "Edit"){
        const content = post.querySelector('p').innerHTML;

        // Show a textare for editting the post
        post.innerHTML = `<textarea class="form-control">${content}</textarea>`;
        
        // Button now shows "save"
        target.innerHTML = "Save";   
    }
 
    // Clicked on Save
    else {
        const content = post.querySelector('textarea').value;
        
        fetch(`/post/${target.id}`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(result => {
        
            // Change the textarea for a normal paragraph
            post.innerHTML = `<p class="card-text">${result.content}</p>`; 

            // Button shows "edit" again
            target.innerHTML = "Edit";
        });
        
    }
    
}