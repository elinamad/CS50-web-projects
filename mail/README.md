<h2>Project 3: Mail</h2>

<b>Project status</b> :black_large_square: <code>not started</code>

Design a front-end for an email client that makes API calls to send and receive emails.

---
<b><h3>Project Specification</h3></b>

Using JavaScript, HTML, and CSS, complete the implementation of your single-page-app email client inside of <code>inbox.js</code> (and not additional or other files; for grading purposes, we’re only going to be considering <code>inbox.js</code>!). You must fulfill the following requirements:

+ <b>Send Mail:</b> When a user submits the email composition form, add JavaScript code to actually send the email.
You’ll likely want to make a <code>POST</code> request to <code>/emails</code>, passing in values for <code>recipients</code>, <code>subject</code>, and <code>body</code>.
Once the email has been sent, load the user’s sent mailbox.
+ <b>Mailbox:</b> When a user visits their Inbox, Sent mailbox, or Archive, load the appropriate mailbox.
    + You’ll likely want to make a <code>GET</code> request to <code>/emails/<mailbox></code> to request the emails for a particular mailbox.
    + When a mailbox is visited, the application should first query the API for the latest emails in that mailbox.
    + When a mailbox is visited, the name of the mailbox should appear at the top of the page (this part is done for you).
    + Each email should then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
    + If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.
+ <b>View Email:</b> When a user clicks on an email, the user should be taken to a view where they see the content of that email.
    + You’ll likely want to make a <code>GET</code> request to <code>/emails/<email_id></code> to request the email.
    + Your application should show the email’s sender, recipients, subject, timestamp, and body.
    + You’ll likely want to add an additional <code>div</code> to <code>inbox.html</code> (in addition to emails-view and compose-view) for displaying the email. Be sure to update your code to hide and show the right views when navigation options are clicked.
    + See the hint in the Hints section about how to add an event listener to an HTML element that you’ve added to the DOM.
    + Once the email has been clicked on, you should mark the email as read. Recall that you can send a <code>PUT</code> request to <code>/emails/<email_id></code> to update whether an email is read or not.
+ <b>Archive and Unarchive:</b> Allow users to archive and unarchive emails that they have received.
    + When viewing an Inbox email, the user should be presented with a button that lets them archive the email. When viewing an Archive email, the user should be presented with a button that lets them unarchive the email. This requirement does not apply to emails in the Sent mailbox.
    + Recall that you can send a <code>PUT</code> request to <code>/emails/<email_id></code> to mark an email as archived or unarchived.
    + Once an email has been archived or unarchived, load the user’s inbox.
+ <b>Reply:</b> Allow users to reply to an email.
    + When viewing an email, the user should be presented with a “Reply” button that lets them reply to the email.
    + When the user clicks the “Reply” button, they should be taken to the email composition form.
    + Pre-fill the composition form with the <code>recipient</code> field set to whoever sent the original email.
    + Pre-fill the subject line. If the original email had a subject line of <code>foo</code>, the new subject line should be <code>Re: foo</code>. (If the subject line already begins with <code>Re: </code>, no need to add it again.)
    + Pre-fill the <code>body</code> of the email with a line like <code>"On Jan 1 2020, 12:00 AM foo@example.com wrote:"</code> followed by the original text of the email.

