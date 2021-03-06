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

Finally, you must be able to trust staff with this module because they can
upload any file and send it out to any email address.

## Installation

Daily emailer was originally developed with django 1.6 and has been updated to django 1.7. It has only been tested with these versions.

Also, it has only been tested with MySQL and sqlite3.

Please install from source:

```
$ pip install git+https://github.com/zmetcalf/daily_emailer.git
```
Add 'daily_emailer' to INSTALLED_APPS.

Add your from address:

```python
EMAIL_FROM_BLOCK = 'John Smith <jsmith@debug.com>'
```

If you are using the demo, a seperate file, email_settings.py, is suggested for putting SMTP (https://docs.djangoproject.com/en/dev/topics/email/#smtp-backend) or SendGrid settings.
You can also just include these settings in your settings.py file.

SendGrid is not a requirement but to enable it, add these settings:

```python
SENDGRID = True
SENDGRID_USERNAME = 'yoursendgridusername'
SENDGRID_PASSWORD = 'yoursendgridpassword'
```

Add daily emailer urls to your urls.py file:

```python
url(r'^daily_emailer/', include('daily_emailer.urls')),
```
For email attachments, make sure you have a media file with correct permissions.

If you are using the demo, change Debug to False in the settings.py file to send live emails.

Other than these additional considerations, installation is just like Django.
