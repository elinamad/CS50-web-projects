document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //send email button
  document.querySelector('#compose-form').addEventListener('submit',()=> send_email(event));

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
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 id ="title">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //If sent emails
  let title = document.querySelector('#title');
  if (title.innerHTML == "Sent"){
    console.log('sent emails');
  }

  //if inbox
  if (title.innerHTML == 'Inbox'){
    console.log('inbox');
  }

  //if archive
  if (title.innerHTML == 'Archive'){
    console.log('archive');
  }

}

function send_email(){

  //get the input values
  let recipientsValue = document.querySelector('#compose-recipients').value;
  let subjectValue = document.querySelector('#compose-subject').value;
  let bodyValue = document.querySelector('#compose-body').value;

  //send email
  fetch('/emails', {
    method:'POST',
    body: JSON.stringify({
      recipients:recipientsValue,
      subject:subjectValue,
      body:bodyValue
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  })

  //Prevent refresh and show sent emails
  event.preventDefault();
  load_mailbox('sent');

}
