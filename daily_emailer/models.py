from django.db import models


class Recipient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)


class Email(models.Model):
    subject = models.CharField(max_length=77)
    message = models.TextField()
    email_group = models.ForeignKey('EmailGroup', related_name='email')

    def __unicode__(self):
        return (self.subject[:50] + '...') if len(self.subject) > 50 \
            else self.subject


class SentEmail(models.Model):
    email = models.ForeignKey('Email')
    sent_date = models.DateField()
    campaign = models.ForeignKey('Campaign', related_name='sent_email')


class EmailGroup(models.Model):
    group_name = models.CharField(max_length=50)
    email_order = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.group_name


class Campaign(models.Model):
    email_group = models.ForeignKey('EmailGroup')
    recipient = models.ForeignKey('Recipient')
    reference_name = models.CharField(max_length=128)
    start_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.reference_name


class Attachment(models.Model):
    file_name = models.CharField(max_length=50)
    attachment = models.FileField(upload_to='email_attachments/%Y/%m/%d')
    email = models.ForeignKey('Email')

    def __unicode__(self):
        return self.file_name
