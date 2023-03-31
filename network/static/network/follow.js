document.addEventListener('DOMContentLoaded', () => {
    
    const username = document.querySelector('h2').innerHTML

    fetch(`/follow/${username}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(result => updateStatus(result))
    .then(() => document.querySelector('#follow')?.addEventListener('click', () => follow(username)));
    
});


const follow = (username) => {
    
    fetch(`/follow/${username}`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(result => updateStatus(result));
}


const updateStatus = (status) => {

    const followButton = document.querySelector('#follow');
    
    if (followButton){
        if (status.currently_following) {
            followButton.innerHTML = "Unfollow";
        }
        else {
            followButton.innerHTML = "Follow";
        }
    }

    document.querySelector('#followers').innerHTML = status.followers;
    document.querySelector('#following').innerHTML = status.following;
}