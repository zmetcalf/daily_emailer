from django.conf import settings
from django.core.mail import send_mail

def send_email(email, recipient):
    addressee = '%s %s <%s>' % (recipient.first_name, recipient.last_name, \
                               recipient.email)
    if settings.SENDGRID:
        send_sendgrid_mail(email, addressee)
    else:
        send_django_mail(email, addressee)

def send_sendgrid_mail(email, addressee):
    import sendgrid
    sg = sendgrid.SendGridClient(settings.SENDGRID_USERNAME,
                                 settings.SENDGRID_PASSWORD)
    message = sendgrid.Mail()
    message.add_to(addressee)
    message.set_subject(email.subject)
    message.set_html(email.message)
    message.set_from(settings.EMAIL_FROM_BLOCK)
    status, msg = sg.send(message)

def send_django_mail(email, addressee):
    send_mail(email.subject, email.message, settings.EMAIL_FROM_BLOCK, [addressee])
