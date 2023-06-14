let isEvent = false;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //by default, hide view email
  document.querySelector('#email-view').style.display = 'none';

  //send email button
  document.querySelector('#compose-form').addEventListener('submit',()=> send_email(event));

});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display='none';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML='';
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

        let emailRecipients = emails[i].recipients;
        let emailSubject = emails[i].subject;
        let emailTimestamp = emails[i].timestamp;
        let emailRead = emails[i].read;
        let emailID = emails[i].id;
        let emailSender = emails[i].sender;
        let emailBody = emails[i].body;
        let emailArchived = emails[i].archived;

        //Email container
        let container = document.createElement('div');
        container.setAttribute('id',`email-container-${emailID}`);
        container.setAttribute('class','email-container');
        document.querySelector('#emails-view').append(container);

        //recipient container
        let recipientsContainer = document.createElement('div');
        recipientsContainer.setAttribute('id',`recipients-container-${emailID}`);
        recipientsContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(recipientsContainer);

        //subject container
        let subjectContainer = document.createElement('div');
        subjectContainer.setAttribute('id',`subject-container-${emailID}`);
        subjectContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(subjectContainer);

        //timestamp container
        let timestampContainer = document.createElement('div');
        timestampContainer.setAttribute('id',`timestamp-container-${emailID}`);
        timestampContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(timestampContainer);

        //recipients label
        let recipientsText = document.createElement('p');
        recipientsText.setAttribute('class','label');
        recipientsText.innerHTML = 'To:';
        document.querySelector(`#recipients-container-${emailID}`).append(recipientsText);
      
        //Recipients
        let recipients = document.createElement('p');
        recipients.innerHTML = emailRecipients;
        document.querySelector(`#recipients-container-${emailID}`).append(recipients);

        //Subject label
        let subjectText = document.createElement('p');
        subjectText.setAttribute('class','label');
        subjectText.innerHTML = 'Subject:'
        document.querySelector(`#subject-container-${emailID}`).append(subjectText);

        //Subject
        let subject = document.createElement('p');
        subject.innerHTML = emailSubject;
        document.querySelector(`#subject-container-${emailID}`).append(subject);

        //timestamp label
        let timestampText = document.createElement('p');
        timestampText.setAttribute('class','label');
        timestampText.innerHTML = 'Date:'
        document.querySelector(`#timestamp-container-${emailID}`).append(timestampText);

        //timestamp
        let timestamp = document.createElement('p');
        timestamp.innerHTML = emailTimestamp;
        document.querySelector(`#timestamp-container-${emailID}`).append(timestamp);

        //Apply read or unread styling
        if (emailRead == false){
          document.querySelector(`#email-container-${emailID}`).classList.add('unread');
        }else{
          document.querySelector(`#email-container-${emailID}`).classList.remove('unread');
        }

        //open email
        document.querySelector(`#email-container-${emailID}`).addEventListener('click',function(){
          document.querySelector(`#emails-view`).style.display = 'none';
          document.querySelector('#email-view').style.display = 'block';
          document.querySelector('#btn-archive').style.display ='none';
          document.querySelector('#btn-reply').style.display='none';

          if (emailRead == false){
            fetch(`emails/${emailID}`,{
              method:'PUT',
              body:JSON.stringify({
                read:true
              })
            })
          }

          document.querySelector('#email-view-sender').innerHTML = emailSender;
          document.querySelector('#email-view-recipients').innerHTML = emailRecipients;
          document.querySelector('#email-view-subject').innerHTML = emailSubject;
          document.querySelector('#email-view-timestamp').innerHTML = emailTimestamp;
          document.querySelector('#email-view-body').innerHTML = emailBody;

          
        })


      }
    })
  }

  //INBOX
  if (title.innerHTML == 'Inbox'){
    fetch('emails/inbox')
    .then(response => response.json())
    .then(emails => {
      console.log(emails)

      for (i=0;i<emails.length;i++){
        let emailSender = emails[i].sender;
        let emailRecipients = emails[i].recipients;
        let emailSubject = emails[i].subject;
        let emailTimestamp = emails[i].timestamp;
        let emailRead = emails[i].read;
        let emailID = emails[i].id;
        let emailBody = emails[i].body;
        let emailArchived = emails[i].archived;

        //email container
        let container = document.createElement('div');
        container.setAttribute('id',`email-container-${emailID}`);
        container.setAttribute('class','email-container');
        document.querySelector('#emails-view').append(container);

        //sender container
        let senderContainer = document.createElement('div');
        senderContainer.setAttribute('id',`sender-container-${emailID}`);
        senderContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(senderContainer);

        //subject container
        let subjectContainer = document.createElement('div');
        subjectContainer.setAttribute('id',`subject-container-${emailID}`);
        subjectContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(subjectContainer);

        //timestamp container
        let timestampContainer = document.createElement('div');
        timestampContainer.setAttribute('id',`timestamp-container-${emailID}`);
        timestampContainer.setAttribute('class','item-container');
        document.querySelector(`#email-container-${emailID}`).append(timestampContainer);

        //sender label
        let senderText = document.createElement('p');
        senderText.setAttribute('class','label');
        senderText.innerHTML= "From:";
        document.querySelector(`#sender-container-${emailID}`).append(senderText);

        //sender
        let sender = document.createElement('p');
        sender.innerHTML = emailSender;
        document.querySelector(`#sender-container-${emailID}`).append(sender);

        //subject label
        let subjectText = document.createElement('p');
        subjectText.setAttribute('class','label');
        subjectText.innerHTML = "Subject:";
        document.querySelector(`#subject-container-${emailID}`).append(subjectText);

        //subject
        let subject = document.createElement('p');
        subject.innerHTML = emailSubject;
        document.querySelector(`#subject-container-${emailID}`).append(subject);

        //timestamp label
        let timestampText = document.createElement('p');
        timestampText.setAttribute('class','label');
        timestampText.innerHTML = 'Date:';
        document.querySelector(`#timestamp-container-${emailID}`).append(timestampText);

        //timestamp
        let timestamp = document.createElement('p');
        timestamp.innerHTML = emailTimestamp;
        document.querySelector(`#timestamp-container-${emailID}`).append(timestamp);

        //apply read or unread styling
        if (emailRead == false){
          document.querySelector(`#email-container-${emailID}`).classList.toggle('unread');
        }

        //Open email
          document.querySelector(`#email-container-${emailID}`).addEventListener('click',function(){
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#email-view').style.display = 'block';
            document.querySelector('#btn-archive').style.display ='flex';
            document.querySelector('#btn-reply').style.display = 'flex';

            if (emailRead == false){
              fetch(`/emails/${emailID}`,{
                method:'PUT',
                body:JSON.stringify({
                  read:true
                })
              })
            }

            document.querySelector('#email-view-sender').innerHTML = emailSender;
            document.querySelector('#email-view-recipients').innerHTML = emailRecipients;
            document.querySelector('#email-view-subject').innerHTML = emailSubject;
            document.querySelector('#email-view-timestamp').innerHTML = emailTimestamp;
            document.querySelector('#email-view-body').innerHTML = emailBody;

            //Archive button

            if (emailArchived === false){
              document.querySelector('#btn-archive').innerHTML = "Archive";
            }else{
              document.querySelector('#btn-archive').innerHTML = "Unarchive";
            }

            document.querySelector('#btn-archive').onclick = function(){
              if(emailArchived === false){
                fetch(`/emails/${emailID}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived:true
                  })
                })
                document.querySelector('#btn-archive').innerHTML = "Unarchive";
              }else{
                fetch(`/emails/${emailID}`, {
                  method:'PUT',
                  body: JSON.stringify({
                    archived:false
                  })
                })
                document.querySelector('#btn-archive').innerHTML = "Archive";

              }
              document.querySelector('#emails-view').innerHTML = '';

              let delay = 250
              setTimeout(function(){
                load_mailbox('inbox');
              },delay);
            }

            //reply button
            document.querySelector('#btn-reply').onclick = function(){
              document.querySelector('#email-view').style.display = 'none';
              document.querySelector('#emails-view').style.display = 'none';
              document.querySelector('#compose-view').style.display = 'block';

              document.querySelector('#compose-recipients').value = emailSender;
              document.querySelector('#compose-subject').value = `Re:${emailSubject}`;
              document.querySelector('#compose-body').value = `on ${emailTimestamp} ${emailSender} wrote: ${emailBody}`;
            }
            
  
          })  
      }
    })
  }

  //ARCHIVE
  if (title.innerHTML == 'Archive'){
    fetch('emails/archive')
    .then(response => response.json())
    .then(emails => {
      console.log(emails);

      if(emails){
        for(i=0;i<emails.length;i++){
          let emailSender = emails[i].sender;
          let emailId = emails[i].id;
          let emailRecipients = emails[i].recipients;
          let emailSubject = emails[i].subject;
          let emailTimestamp = emails[i].timestamp;
          let emailBody = emails[i].body;
          let emailArchived = emails[i].archived;

          //email container
          let container = document.createElement('div');
          container.setAttribute('id',`email-container-${emailId}`);
          container.setAttribute('class','email-container');
          document.querySelector('#emails-view').append(container);

          //sender container
          let senderContainer = document.createElement('div');
          senderContainer.setAttribute('id',`sender-container-${emailId}`);
          senderContainer.setAttribute('class','item-container');
          document.querySelector(`#email-container-${emailId}`).append(senderContainer);

          //subject container
          let subjectContainer = document.createElement('div');
          subjectContainer.setAttribute('id',`subject-container-${emailId}`);
          subjectContainer.setAttribute('class','item-container');
          document.querySelector(`#email-container-${emailId}`).append(subjectContainer);

          //timestamp container
          let timestampContainer = document.createElement('div');
          timestampContainer.setAttribute('id',`timestamp-container-${emailId}`);
          timestampContainer.setAttribute('class','item-container');
          document.querySelector(`#email-container-${emailId}`).append(timestampContainer);

          //sender label
          let senderText = document.createElement('p');
          senderText.setAttribute('class','label');
          senderText.innerHTML = 'From:'
          document.querySelector(`#sender-container-${emailId}`).append(senderText);

          //sender
          let sender = document.createElement('p');
          sender.innerHTML = emailSender;
          document.querySelector(`#sender-container-${emailId}`).append(sender);

          //subject label
          let subjectText  = document.createElement('p');
          subjectText.setAttribute('class','label');
          subjectText.innerHTML = "Subject:";
          document.querySelector(`#subject-container-${emailId}`).append(subjectText);

          //subject
          let subject = document.createElement('p');
          subject.innerHTML = emailSubject;
          document.querySelector(`#subject-container-${emailId}`).append(subject);

          //timestamp label
          let timestampText = document.createElement('p');
          timestampText.setAttribute('class','label');
          timestampText.innerHTML = "Date:";
          document.querySelector(`#timestamp-container-${emailId}`).append(timestampText);

          //timestamp
          let timestamp = document.createElement('p');
          timestamp.innerHTML = emailTimestamp;
          document.querySelector(`#timestamp-container-${emailId}`).append(timestamp);

        //Open email

        document.querySelector(`#email-container-${emailId}`).addEventListener('click',function(){
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-view').style.display = 'block';
          document.querySelector('#btn-archive').style.display ='flex';
          document.querySelector('#btn-reply').style.display ='none';

          document.querySelector('#email-view-sender').innerHTML = emailSender;
          document.querySelector('#email-view-recipients').innerHTML = emailRecipients;
          document.querySelector('#email-view-subject').innerHTML = emailSubject;
          document.querySelector('#email-view-timestamp').innerHTML = emailTimestamp;
          document.querySelector('#email-view-body').innerHTML = emailBody;

          //Archive button
          if(emailArchived === false){
            document.querySelector('#btn-archive').innerHTML = "Archive";
          }else{
            document.querySelector('#btn-archive').innerHTML = "Unarchive";
          }

            document.querySelector('#btn-archive').onclick = function(){
              isEvent = true;
              if(emailArchived ==false){
                fetch(`/emails/${emailId}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived:true
                  })
                })
              }else{
                fetch(`/emails/${emailId}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived:false
                  })
                })
              }
              let delay = 250
              setTimeout(function(){
                load_mailbox('archive');
              },delay);
            }
        
          
        })
      }
      }else{
        let error = document.createElement('p');
        error.innerHTML = 'no archived emails';
        document.querySelector('#emails-view').append(error);
      }

      
    })
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
      body:bodyValue,
      read:false,
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
