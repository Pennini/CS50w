document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('#compose-post') != null) {
        document.querySelector('#compose-post').addEventListener('submit', sendPost);
    }

    if (document.querySelector('#follow-but') != null) {
        const follow_but = document.querySelector('#follow-but');
        follow_but.addEventListener('click', (event) => {
            event.preventDefault();
            follow(follow_but);
        });
    }

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.className === 'icone-like') {
            event.preventDefault();
            changeImage(element);
        }
        if (element.className === "edit-post") {
            event.preventDefault();
            document.querySelector(`#post-content-${element.dataset.id}`).style.display = "none";
            document.querySelector(`#post-edit-${element.dataset.id}`).style.display = "block";
        }
        if (element.dataset.intention === 'edit') {
            document.querySelector(`#form-${element.dataset.id}`).addEventListener('submit', (event) => {
                event.preventDefault();
                editPost(element.dataset.id);
            });
        }
    });
});

function editPost(element) {
    const text = document.querySelector(`#content-${element}`).value;
    let error_message = document.querySelector(`#error-${element}`);
    if (!text.trim()) {
        console.log('Error: No text to post');
        error_message.style.display = 'block';
        error_message.innerHTML = 'No text to post';
        error_message.style.backgroundColor = "red";
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 3000);
        return;
    } else if (text.length > 300) {
        console.log('Error: Text too long');
        error_message.style.display = 'block';
        error_message.innerHTML = 'Text too long';
        error_message.style.backgroundColor = "red";
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 3000);
        return;
    } else {
        fetch(`/edit/${element}`, {
            method: "POST",
            body: JSON.stringify({
                text: text
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector(`#post-edit-${element}`).style.display = "none";
            document.querySelector(`#post-content-${element}`).style.display = "flex";
            document.querySelector(`#textarea-${element}`).innerHTML = text;

        })
        .catch(error => {
            console.log('Error:', error);
        });
    }
    
}



function follow(element) {
    fetch(`/follow/${element.dataset.following}`,{
        method: "POST",
        body: JSON.stringify({
            follow: element.dataset.follow
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.status === 1) {
            let followers = parseInt(document.querySelector('#followers').innerHTML);
            if (element.dataset.follow === "True") {
                element.className = "btn btn-outline-primary";
                element.innerHTML = "Follow";
                element.dataset.follow = "False";
                followers--;
            } else {
                element.className = "btn btn-primary";
                element.innerHTML = "Unfollow";
                element.dataset.follow = "True";
                followers++;
            }
            document.querySelector('#followers').innerHTML = followers;
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}



function sendPost(event) {
    event.preventDefault()
    const text = document.querySelector('#text-post').value;
    let error_message = document.querySelector("#error");
    if (!text.trim()) {
        console.log('Error: No text to post');
        error_message.style.display = 'block';
        error_message.innerHTML = 'No text to post';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 3000);
        return;
    } else if (text.length > 300) {
        console.log('Error: Text too long');
        error_message.style.display = 'block';
        error_message.innerHTML = 'Text too long';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 3000);
        return;
    } else {
        fetch('/posts', {
            method: 'POST',
            body: JSON.stringify({
                text: text
            })
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
            document.querySelector('#text-post').value = "";
            console.log('Success: Post sent');
            error_message.style.display = 'block';
            error_message.style.backgroundColor = 'lightgreen';
            error_message.innerHTML = 'Posted successfully';
            setTimeout(() => {
                error_message.style.display = 'none';
            }, 3000);
          })
          .catch(error => {
              console.log('Error:', error);
          });
    }
}

function changeImage(element) {
    const post_id = element.dataset.id;
    if (element.src === 'http://127.0.0.1:8000/static/network/images/like.png') {
        element.src = '/static/network/images/unlike.png';
    } else {
        element.src = '/static/network/images/like.png';
    }
    fetch(`/posts/${post_id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector(`#like-${post_id}`).innerHTML = result.likes;
    })
    .catch(error => {
        console.log('Error:', error);
    });

}