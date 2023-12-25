let members = [];
var counter = 0;
var timer;

document.addEventListener('DOMContentLoaded', () => {

    if (document.querySelector('#meeting-select')) {
        document.querySelector('#meeting-select').addEventListener('change', (event) => {
            event.preventDefault();
            const elementSelect = document.querySelector('#meeting-select');
            const elementOption = document.querySelector('#meeting-select option:checked');
            if (elementSelect.value !== '0') {
                document.querySelector('#start-meeting').disabled = false;
                prepareMembers(elementOption, elementSelect);
            } else {
                document.querySelector('#start-meeting').disabled = true;
            }
        });
    }

    if (document.querySelector('#start-meeting')) {
        document.querySelector('#start-meeting').addEventListener('click', (event) => {
            event.preventDefault();
            const selected = document.querySelector('#meeting-select');
            const elementOption = document.querySelector('#meeting-select option:checked');
            if (selected.value === '0' || selected.innerHTML === 'Select a option') {
                alert('Select a Group or a Area to start a meeting');
                return false;
            }
            prepareButtons(elementOption);

            prepareTitle(elementOption);

            document.querySelector('.meeting-archive').style.display = 'block';
            count();
        });
    } console.log

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.classList.contains('day-hour')) {
            event.preventDefault();
            alterAvailability(element);
        }

        if (element.classList.contains('day-desactive')) {
            event.preventDefault();
            showDayInfo(element);
        }
        if (element.parentElement) {
            if (element.parentElement.classList.contains('day-desactive')) {
                event.preventDefault();
                showDayInfo(element.parentElement);
            }
            if (element.parentElement.parentElement) {
                if (element.parentElement.parentElement.classList.contains('day-desactive')) {
                    event.preventDefault();
                    showDayInfo(element.parentElement.parentElement);
                }
            }
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

function prepareMembers(elementOption, elementSelect) {
    fetch("/meeting/members", {
        method: "POST",
        body: JSON.stringify({
            id: elementSelect.value,
            type: elementOption.dataset.type
        })
    }).then(response => response.json())
    .then(result => {

        var memberDict = JSON.parse(result.members);

        for (var index in memberDict) {
            const member = memberDict[index];

            const divMember = document.createElement('div');
            divMember.className = 'members-check';

            document.querySelector('.meeting-members').appendChild(divMember);

            const inputMember = document.createElement('input');
            inputMember.type = 'checkbox';
            inputMember.name = 'member';
            inputMember.value = member;
            inputMember.id = 'member_' + member;

            const labelMember = document.createElement('label');
            labelMember.innerHTML = index;
            labelMember.htmlFor = 'member_' + member;

            divMember.appendChild(inputMember);
            divMember.appendChild(labelMember);

            inputMember.addEventListener('change', (event) => {
                if (event.target.checked) {
                    members.push(event.target.value);
                } else {
                    members = members.filter(member => member !== event.target.value);
                }
            });
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function goBack() {
    document.querySelector('#meeting-title').remove();
    document.querySelector('#meeting-select').style.display = 'block';
    document.querySelector('#meeting-select').value = '0';
    document.querySelector('#cancel-meeting').remove();
    document.querySelector('#finish-meeting').remove();
    document.querySelector('#restart-meeting').remove();
    document.querySelector('.meeting-archive').style.display = 'none';
    document.querySelector('.meeting-start-button').style.display = 'block';
    document.querySelector('.meeting-buttons').style.display = 'none';
    document.querySelector('#meeting-member').style.display = 'none';
    counter = 0;
    document.querySelector('#counter').innerHTML = '00:00:00';
    document.querySelector('#start-meeting').disabled = true;
    document.querySelector('.meeting-members').innerHTML = '';
    document.querySelector('#inputGroupFile02').value = '';
    document.querySelector('#label-file').innerHTML = 'Choose a Meeting Report';
}

function prepareTitle(selected) {
    document.querySelector('#meeting-select').style.display = 'none';
    const title = document.createElement('h2');
    title.innerHTML = selected.innerHTML;
    title.id = 'meeting-title';
    document.querySelector('.meeting-header').appendChild(title);
}

function prepareButtons(element) { 
    document.querySelector('.meeting-start-button').style.display = 'none';
    const butCancel = document.createElement('button');
    const butFinish = document.createElement('button');
    const butRestart = document.createElement('button');

    butCancel.innerHTML = 'Cancel';
    butFinish.innerHTML = 'Finish';
    butRestart.innerHTML = 'Restart';

    butCancel.className = 'btn btn-danger';
    butFinish.className = 'btn btn-success';
    butRestart.className = 'btn btn-warning';

    butCancel.id = 'cancel-meeting';
    butFinish.id = 'finish-meeting';
    butRestart.id = 'restart-meeting';

    document.querySelector('.meeting-buttons').appendChild(butCancel);
    document.querySelector('.meeting-buttons').appendChild(butRestart);
    document.querySelector('.meeting-buttons').appendChild(butFinish);
    document.querySelector('.meeting-buttons').style.display = 'block';
    document.querySelector('#meeting-member').style.display = 'block';

    document.querySelector('#message-success').style.display = 'none';

    butCancel.addEventListener('click', (event) => {
        event.preventDefault();
        if (confirm('Are you sure you want to cancel the meeting?')) {
            goBack();
            document.querySelector('#message-success').innerHTML = 'Meeting canceled';
            document.querySelector('#message-success').style.display = 'block';
            counter = 0;
            clearInterval(timer);
        } else {
            console.log('Continue');
        }
    });

    butRestart.addEventListener('click', (event) => {
        event.preventDefault();
        if (confirm('Are you sure you want to restart the meeting?')) {
            counter = 0;
            document.querySelector('#counter').innerHTML = '00:00:00';
            clearInterval(timer);
            count();
        } else {
            console.log('Continue');
        }
    });

    butFinish.addEventListener('click', (event) => {
        event.preventDefault();
        const formulario = document.getElementById('forms-file');

        const formData = new FormData(formulario);

        if (confirm('Are you sure you want to finish the meeting?\nDon\'t forget to select a meeting report archive')) {
            
            formData.append('type', element.dataset.type);
            formData.append('id', element.value);
            formData.append('duration', parseInt(localStorage.getItem('counter')));
            formData.append('members', members);

            fetch('/meeting/finish', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                counter = 0;
                clearInterval(timer);
                goBack();
                document.querySelector('#message-success').innerHTML = 'Meeting finished successfully';
                document.querySelector('#message-success').style.display = 'block';
            })
            .catch(error => {
                console.log('Error:', error);
            });
        } else {
            console.log('Continue');
        }
    });
}

function count() {
    timer = setInterval(() => {
        counter++;
        localStorage.setItem('counter', counter);
        let hours = Math.floor((counter / 60) / 60);
        let minutes = Math.floor(counter / 60 - (hours * 60));
        let seconds = Math.floor(counter % 60);

        if (seconds < 10) {
            seconds = `0${seconds}`;
        }
        if (minutes < 10) {
            minutes = `0${minutes}`;
        }
        if (hours < 10) {
            hours = `0${hours}`;
        }
        document.querySelector('#counter').innerHTML = `${hours}:${minutes}:${seconds}`;
    }, 1000);
}


function showDayInfo(element) {
    if (document.querySelector('.day-active')) {
        const activeDay = document.querySelector('.day-active')
        const dayActive = activeDay.dataset.day;
        const weekdayActive = activeDay.dataset.weekday;
        
        activeDay.className = 'day-desactive';
        document.getElementById(`${dayActive}-${weekdayActive}`).style.display = 'none';

    }
    element.className = 'day-active';
    const day = element.dataset.day;
    const weekday = element.dataset.weekday;
    document.getElementById(`${day}-${weekday}`).style.display = 'block';
}

function alterAvailability(element) {
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
        fetch(`/display/${type}/${id}`, {
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