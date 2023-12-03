document.addEventListener('DOMContentLoaded', () => {

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.classList.contains('day-hour')) {
            event.preventDefault()
            const computedStyle = window.getComputedStyle(element);
            const bgcolor = computedStyle.backgroundColor;
            alterAvailability(element);
       }
    });
    if (document.querySelector('#form-compose-bio')) {
        document.querySelector('#form-compose-bio').addEventListener('submit', (event) => {
            event.preventDefault();
            changeBio();
        });
    }
    if (document.querySelector("#button-bio-edit")) {
        document.querySelector("#button-bio-edit").addEventListener('click', (event) => {
            event.preventDefault();
            document.querySelector('#bio-show').style.display = 'none';
            document.querySelector('#bio-form').style.display = 'block';
        });
    }

    if (document.querySelector('#form-compose-des')) {
        document.querySelector('#form-compose-des').addEventListener('submit', (event) => {
            event.preventDefault();
            changeDes();
        });
    }
    if (document.querySelector("#button-des-edit")) {
        document.querySelector("#button-des-edit").addEventListener('click', (event) => {
            event.preventDefault();
            document.querySelector('#des-show').style.display = 'none';
            document.querySelector('#des-form').style.display = 'block';
        });
    }

});

function alterAvailability(element) {
    console.log(element);
    const day = element.dataset.day;
    const start = element.dataset.start;
    const end = element.dataset.end;
    fetch('/availability', {
        method: 'POST',
        body: JSON.stringify({
            day: day,
            start: start,
            end: end,
        })
      })
      .then(response => response.json())
      .then(result => {
        if (result.status === 0) {
            element.style.backgroundColor = 'red';
        } else if (result.status === 1) {
            element.style.backgroundColor = 'yellow';
        } else if (result.status === 2) {
            element.style.backgroundColor = 'green';
        }
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

function changeDes() {
    const content = document.querySelector('#content-des-compose');
    const text = content.value;
    const type = content.dataset.type;
    const id = content.dataset.id;
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
        fetch(`/display/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                text: text,
                type: type
            })
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
            document.querySelector('#des-form').style.display = 'none';

            document.querySelector('#content-des').innerHTML = text;
            document.querySelector('#des-show').style.display = 'block';

          })
          .catch(error => {
              console.log('Error:', error);
          });
    }
}

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