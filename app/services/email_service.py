from flask_mail import Mail, Message

mail = Mail()

def send_email(subject, recipients, body):
    message = Message(subject, recipients=recipients)
    message.body = body
    mail.send(message)
