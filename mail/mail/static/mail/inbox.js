document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', sendEmail);
  window.addEventListener('click', (event) => {
    const element = event.target;
    if (element.className === 'col-sm-10' || element.tagName === 'SPAN' || element.tagName === 'STRONG') {
      const emails = document.querySelector("#emails-view");
      const id_mail = element.dataset.id;
      fetch(`/emails/${id_mail}`)
      .then(response => response.json())
      .then(email => {
        emails.innerHTML = '';
        // ... do something else with email ...
        const div = document.createElement('div');
        div.innerHTML = `<strong>From:</strong> ${email['sender']}<br><strong>To:</strong> ${email['recipients']}<br><strong>Subject:</strong> ${email['subject']}<br><strong>Timestamp:</strong> ${email['timestamp']}<br><br><button data-id="${email['id']}" class="btn btn-sm btn-outline-primary" id="reply">Reply</button> <hr> <br> ${email['body']}`;
        emails.appendChild(div);
        fetch(`/emails/${id_mail}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      });
    }
    if (element.dataset.name === 'archive') {
      const id_mail = element.dataset.id;
      var parentNode = document.getElementById(`${id_mail}`);
      var is_archive = NaN;
      console.log(parentNode); 
      if (parentNode.dataset.archive === 'true') {
        is_archive = false;
      } else {
        is_archive = true;
      }
      fetch(`/emails/${id_mail}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: is_archive
        })
      })
      .then(() => {
        parentNode.style.animationPlayState = 'running';
        parentNode.addEventListener('animationend', () => {
          parentNode.remove();
        });
      })
      .then(() => {
        load_mailbox('inbox');
      });
    }
    
    if (element.id === 'reply') {
      const id_mail = element.dataset.id;
      fetch(`/emails/${id_mail}`)
      .then(response => response.json())
      .then(email => {
        // ... do something else with email ...
        compose_email();
        document.querySelector('#compose-recipients').value = email['sender'];
        if (email['subject'].startsWith('Re: ')){
          document.querySelector('#compose-subject').value = `${email['subject']}`;
        } else {
          document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
        }
        document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote:\n${email['body']}\n\n`;
      });
    }
  })

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  const views = document.querySelector('#emails-view');
  // Show the mailbox and hide other views
  views.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  views.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // ... do something else with emails ...
      for (var i = 0; i < emails.length; i++) {
        const div_maior = document.createElement('div');
        div_maior.className = 'row';
        const div = document.createElement('div');
        div.dataset.id = `${emails[i].id}`
        div.dataset.archive = `${emails[i].archived}`
        div.className = 'col-sm-10';
        div.id = `${emails[i].id}`;

        if (emails[i].read) {
          div.style.backgroundColor = 'gainsboro';
        } else {
          div.style.backgroundColor = 'white';
        }

        div.innerHTML = `<span data-id="${emails[i].id}" class="sender"><strong data-id="${emails[i].id}">${emails[i].sender}</strong></span> <span data-id="${emails[i].id}" class="vl"></span> <span data-id="${emails[i].id}" class="subject">Subject: ${emails[i].subject}</span> <span data-id="${emails[i].id}" class="timestamp">${emails[i].timestamp}</span>`;

        const but = document.createElement('div');
        but.className = 'col-sm-2';
        if (mailbox === 'inbox') {
          but.innerHTML += `<span class="archive"><button data-name="archive" data-id="${emails[i].id}" class="btn btn-outline-primary">Archive</button></span>`
        } else if (mailbox === 'archive') {
          but.innerHTML += `<span class="archive"><button data-name="archive" data-id="${emails[i].id}" class="btn btn-outline-primary">Unarchive</button></span>`
        } else {
          but.innerHTML += `<span class="archive" style="visibility: hidden;"><button data-name="archive" data-id="${emails[i].id}" class="btn btn-outline-primary">Unarchive</button></span>`
        }
        views.appendChild(div_maior);
        div_maior.appendChild(div);
        div_maior.appendChild(but);
      }
  });

}

function sendEmail(event) {
  event.preventDefault();
  
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const content = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: content
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      load_mailbox('sent');
  })
  .catch(error => {
      console.log('Error:', error);
  });
}