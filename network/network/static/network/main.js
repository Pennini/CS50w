document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('#compose-post') != null) {
        document.querySelector('#compose-post').addEventListener('submit', sendPost);
    }

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.className === 'icone-like') {
            event.preventDefault();
            changeImage(element);
        }
    });

});


function sendPost(event) {
    event.preventDefault();
    const text = document.querySelector('#text-post').value;
    let error_message = document.querySelector("#error");
    if (!text.trim()) {
        console.log('Error: No text to post');
        error_message.style.display = 'block';
        error_message.innerHTML = 'No text to post';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 4000);
        return;
    } else if (text.length > 280) {
        console.log('Error: Text too long');
        error_message.style.display = 'block';
        error_message.innerHTML = 'Text too long';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 4000);
        return;
    } else {
        console.log('Success: Post sent');
        error_message.style.display = 'block';
        error_message.style.backgroundColor = 'green';
        error_message.innerHTML = 'Text posted successfully';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 4000);
    }
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
      })
      .catch(error => {
          console.log('Error:', error);
      });
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