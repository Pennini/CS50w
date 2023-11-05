document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', sendEmail);

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
  
  const emails = document.querySelector('#emails-view');
  // Show the mailbox and hide other views
  emails.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails.innerHTML += `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  const list = document.createElement("ul");
  list.className = "list-group";
  emails.append(list);

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...
      for (var i = 0; i < emails.length; i++) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `<span> id="email${i}" ${emails[i].sender}</span> <span class="subject">${emails[i].subject}</span> <span class="timestamp">${emails[i].timestamp}</span>`;
        list.append(li);
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