from django.db import models

class Recipient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

class Email(models.Model):
    subject = models.CharField(max_length=77)
    message = models.TextField()

    def __unicode__(self):
        return (self.subject[:50] + '...') if len(self.subject) > 50 \
                                           else self.subject

class EmailGroup(models.Model):
    group_name = models.CharField(max_length=50)
    emails = models.ManyToManyField('Email')
    email_order = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.group_name

class Campaign(models.Model):
    email_group = models.ForeignKey('EmailGroup')
    recipient = models.ForeignKey('Recipient')
    status = models.TextField()
    reference_name = models.CharField(max_length=128) # Will be generated by admin
    start_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.reference_name

class Attachment(models.Model):
    file_name = models.CharField(max_length=50)
    attachment = models.FileField(upload_to='email_attachments/%Y/%m/%d')
    email = models.ForeignKey('Email')

    def __unicode__(self):
        return self.file_name
