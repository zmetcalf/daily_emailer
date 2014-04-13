daily emailer
=============

Web application using Django's admin to automate sending an email a day to an email address.

## Usage

Start by creating an Email Group. This is the series of emails that you will send to a recipient.
Next add emails and attachments to the email group.
Then add a recipient that will receive the emails.
Finally, create a campaign to tie the recipient and email group together.

A cron job will be necessary to tell the program to send out emails. Daily emailer can only send out one email per campaign per day. So you can set your cron job to be more restrictive than that (once per week, once per month, etc.)

A sample cron job looks like this:
```
0 11 * * 4,5 /path/to/python/in/virtualenv/python /path/to/installation/manage.py send_daily_email
```
This would send the emails on Thursday and Friday at 11:00 am.

## Installation

Daily emailer was developed with django 1.6.2, and it has only been tested with this version.

SendGrid is not a requirement.

A seperate file, email_settings.py, is suggested for putting SMTP (https://docs.djangoproject.com/en/dev/topics/email/#smtp-backend) or SendGrid settings.

For SendGrid, add these settings and change SENDGRID to True

```python
SENDGRID_USERNAME = 'yoursendgridusername'
SENDGRID_PASSWORD = 'yoursendgridpassword'
```

Add daily emailer urls to your urls.py file:

```python
url(r'^daily_emailer/', include('daily_emailer.urls')),
```
Change Debug to False in your settings.py file to send live emails.

For email attachments, make sure you have a media file with correct permissions.

Other than these additional considerations, installation is just like Django.
