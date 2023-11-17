document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#compose-post').addEventListener('submit', sendPost);


});


function sendPost(event) {
    event.preventDefault();
    const text = document.querySelector('#text-post').value;
    if (!text.trim()) {
        console.log('Error: No text to post');
        let error_message = document.querySelector("#error");
        error_message.style.display = 'block';
        setTimeout(() => {
            error_message.style.display = 'none';
        }, 4000);
        return;
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