from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMessage

from daily_emailer.models import Attachment

def send_email(_email, recipient):
    addressee = '%s %s <%s>' % (recipient.first_name, recipient.last_name, \
                               recipient.email)
    attachments = Attachment.objects.all().filter(email=_email)

    if settings.SENDGRID:
        send_sendgrid_mail(_email,  addressee, attachments)
    else:
        send_django_mail(_email, addressee, attachments)

def send_sendgrid_mail(email,  addressee, attachments):
    import sendgrid
    sg = sendgrid.SendGridClient(settings.SENDGRID_USERNAME,
                                 settings.SENDGRID_PASSWORD)
    message = sendgrid.Mail()
    message.add_to(addressee)
    message.set_subject(email.subject)
    message.set_html(email.message)
    message.set_from(settings.EMAIL_FROM_BLOCK)
    if attachments:
        for doc in attachments:
            try:
                file_name = doc.attachment.name.split('/')
                message.add_attachment_stream(file_name.pop(),
                    BytesIO(doc.attachment.read()))
                doc.attachment.close()
            except IOError:
                pass # TODO Add to body that attachements have been removed
            except AssertionError:
                pass
    status, msg = sg.send(message)

def send_django_mail(email, addressee, attachments):
    email = EmailMessage(email.subject, email.message, settings.EMAIL_FROM_BLOCK,
                         [addressee])
    if attachments:
        for doc in attachments:
            try:
                file_name = doc.attachment.name.split('/')
                email.attach(file_name.pop(), doc.attachment.read())
                doc.attachment.close()
            except IOError:
                pass # TODO Add to body that attachements have been removed
            except AssertionError:
                pass
    email.send(fail_silently=True)
