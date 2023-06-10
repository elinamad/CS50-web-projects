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

  //SENT
  let title = document.querySelector('#title');
  if (title.innerHTML == "Sent"){
    fetch('emails/sent')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);

      for(i=0;i<emails.length;i++){

        let emailSender = emails[i].sender;
        let emailSubject = emails[i].subject;

        //Email container
        let container = document.createElement('div');
        container.setAttribute('id',`email-container-${i}`);
        container.setAttribute('class','email-container');
        document.querySelector('#emails-view').append(container);

        //sender container
        let senderContainer = document.createElement('div');
        senderContainer.setAttribute('id',`sender-container-${i}`);
        senderContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${i}`).append(senderContainer);

        //sender container
        let subjectContainer = document.createElement('div');
        subjectContainer.setAttribute('id',`subject-container-${i}`);
        subjectContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${i}`).append(subjectContainer);

        //Sender label
        let senderText = document.createElement('p');
        senderText.setAttribute('class','label');
        senderText.innerHTML = 'From:';
        document.querySelector(`#sender-container-${i}`).append(senderText);
      
        //Sender
        let sender = document.createElement('p');
        sender.setAttribute('class','sender');
        sender.innerHTML = emailSender;
        document.querySelector(`#sender-container-${i}`).append(sender);

        //Subject label
        let subjectText = document.createElement('p');
        subjectText.setAttribute('class','label');
        subjectText.innerHTML = 'Subject:'
        document.querySelector(`#subject-container-${i}`).append(subjectText);

        //Subject
        let subject = document.createElement('p');
        subject.setAttribute('class',`subject-${i}`);
        subject.innerHTML = emailSubject;
        document.querySelector(`#subject-container-${i}`).append(subject);

      }
    })
  }

  //INBOX
  if (title.innerHTML == 'Inbox'){
    console.log('inbox');
  }

  //ARCHIVE
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
