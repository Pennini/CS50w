document.addEventListener('DOMContentLoaded', () => {

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.classList.contains('day-hour')) {
            event.preventDefault()
            const computedStyle = window.getComputedStyle(element);
            const bgcolor = computedStyle.backgroundColor;
            console.log(bgcolor);
            if (bgcolor === 'rgb(255, 255, 255)' || bgcolor === 'white' || bgcolor === 'rgb(0, 128, 0)' || bgcolor === 'green') {
                element.style.backgroundColor = 'red';
            } else if (bgcolor === 'rgb(255, 0, 0)' || bgcolor === 'red') {
                element.style.backgroundColor = 'yellow';
            } else if (bgcolor === 'rgb(255, 255, 0)' || bgcolor === 'yellow') {
                element.style.backgroundColor = 'green';
            }
       }
    });

    document.querySelector('#form-compose-bio').addEventListener('submit', (event) => {
        event.preventDefault();
        changeBio();
    });

    document.querySelector("#button-bio-edit").addEventListener('click', (event) => {
        event.preventDefault();
        document.querySelector('#bio-show').style.display = 'none';
        document.querySelector('#bio-form').style.display = 'block';
    });

});

function changeBio() {
    const text = document.querySelector('#content-bio-compose').value;
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
        fetch('/bio', {
            method: 'POST',
            body: JSON.stringify({
                text: text
            })
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
            document.querySelector('#bio-form').style.display = 'none';

            document.querySelector('#content-bio').innerHTML = text;
            document.querySelector('#bio-show').style.display = 'block';

          })
          .catch(error => {
              console.log('Error:', error);
          });
    }
}