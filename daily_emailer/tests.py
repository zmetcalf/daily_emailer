import datetime
import json
import unittest

from django.contrib.auth.models import User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import  CommandError
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.utils import timezone

from daily_emailer import models, fields, utils
from daily_emailer.management.commands import send_daily_email

class AjaxAssociatedEmailTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('Admin', 'admin@sample.com', 'password')
        user.is_staff = True
        user.save()
        eq = models.EmailGroup(group_name='NewRep')
        eq.save()
        eq.email_set.create(subject='Subject1', message='Message1')
        eq.email_set.create(subject='Subject2', message='Message2')
        eq.email_set.create(subject='Subject3', message='Message3')
        eq.save()
        self.client = Client()

    def test_ajax_associated_emails(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/associated_emails/1/')
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], 1)
        self.assertEqual(data[0]['fields']['message'], 'Message1')
        self.assertEqual(data[1]['fields']['message'], 'Message2')
        self.assertEqual(data[2]['fields']['message'], 'Message3')

    def test_ajax_associated_emails_authenticated_empty(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/associated_emails/2/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_ajax_associated_emails_authenticated(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/associated_emails/1/')
        self.assertEqual(response.status_code, 200)

    def test_ajax_associated_emails_unauthenticated(self):
        response = self.client.post('/daily_emailer/associated_emails/1/')
        self.assertEqual(response.status_code, 404)

class AjaxCampaignEmailsTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('Admin', 'admin@sample.com', 'password')
        user.is_staff = True
        user.save()
        recipient = models.Recipient(first_name='John', last_name='Smith',
                                     email='sample@email.com')
        recipient.save()
        eg = models.EmailGroup(group_name='NewRep')
        eg.save()
        eg.email_set.create(subject='Subject1', message='Message1')
        eg.email_set.create(subject='Subject2', message='Message2')
        eg.email_set.create(subject='Subject3', message='Message3')
        eg.save()
        campaign = models.Campaign(reference_name='C1',
            start_date=datetime.date.today())
        campaign.email_group = eg
        campaign.recipient = recipient
        campaign.save()
        self.client = Client()

    def test_ajax_campaign_emails(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/campaign_emails/1/')
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], 1)
        self.assertEqual(data[0]['fields']['message'], 'Message1')
        self.assertEqual(data[1]['fields']['message'], 'Message2')
        self.assertEqual(data[2]['fields']['message'], 'Message3')

    def test_ajax_campaign_emails_authenticated_empty(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/campaign_emails/2/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_ajax_campaign_emails_authenticated(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/daily_emailer/campaign_emails/1/')
        self.assertEqual(response.status_code, 200)

    def test_ajax_campaign_emails_unauthenticated(self):
        response = self.client.post('/daily_emailer/campaign_emails/1/')
        self.assertEqual(response.status_code, 404)

class SendDailyEmailTests(TestCase):

    def setUp(self):
        recipient = models.Recipient(first_name='John', last_name='Smith',
                                     email='sample@email.com')
        recipient.save()
        eq = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eq.save()
        eq.email_set.create(subject='Subject1', message='Message1')
        eq.email_set.create(subject='Subject2', message='Message2')
        sent_email_three = eq.email_set.create(subject='Subject3', message='Message3')
        eq.save()
        campaign = models.Campaign(reference_name='RefName',
                                   start_date=str(datetime.date.today()),
                                   email_group=eq,
                                   recipient=recipient)
        campaign.save()
        campaign.sentemail_set.create(email=sent_email_three,
            sent_date=datetime.date.today())
        campaign.save()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        success = models.Campaign(reference_name='Success',
                                   start_date=str(datetime.date.today()),
                                   email_group=eq,
                                   recipient=recipient)
        success.save()
        success.sentemail_set.create(email=sent_email_three, sent_date=yesterday)
        self.cmd = send_daily_email.Command()

    def test_get_next_email_success(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.get_next_email(emails, [3,1,2],
                         {3: '2014-4-1'}).pk, 1)

    def test_get_next_email_fail(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.get_next_email(emails, [3,1,2],
                         {3: '2014-4-1', 2: '2014-4-2', 1: '2014-4-3'}), False)

    def test_reconcile_emails_addition(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(emails, [3,1]), [3,1,2])

    def test_reconcile_emails_subtraction(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(emails, [5,3,1,4,2]), [3,1,2])

    def test_reconcile_emails_no_change(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(emails, [3,1,2]), [3,1,2])

    def test_reconcile_emails_add_and_sub(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(emails, [3,4,2]), [3,2,1])

    def test_get_ok_to_mail_completed(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        campaign.completed_date = str(datetime.date.today())
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_today(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        campaign.status = ''
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_tomorrow(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        campaign.status = ''
        campaign.start_date += datetime.timedelta(days=1)
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_yesterday(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        campaign.status = ''
        campaign.start_date -= datetime.timedelta(days=1)
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_none_today(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        campaign.status="{3: '%s'}" % str(yesterday)
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_none_today_or_day_before(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        two_yesterday = datetime.date.today() - datetime.timedelta(days=2)
        campaign.status="{3: '%s'}" % str(two_yesterday)
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    # Not possible but just checking the algorithm
    def test_get_ok_to_mail_mailed_in_future(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        tomorrow = datetime.date.today() + datetime.timedelta(days=2)
        campaign.status="{3: '%s'}" % str(tomorrow)
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_mailed_today(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_handle_success(self):
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.assertEqual(campaign.status, {3: str(yesterday),
                                           1: str(datetime.date.today())})
        self.assertEqual(len(mail.outbox), 1)

    def test_handle_already_sent_today(self):
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='RefName')
        self.assertEqual(campaign.status, {3: str(datetime.date.today())})

    def test_handle_no_emails(self):
        campaign = models.Campaign.objects.get(reference_name='Success')
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        emails = models.Email.objects.all().delete()
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.status, {3: str(yesterday)})

    def test_handle_additional_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        campaign = models.Campaign.objects.get(reference_name='Success')
        eg = models.EmailGroup.objects.get(pk=campaign.email_group.pk)
        eg.email_order = '3,1'
        eg.save()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1')
        campaign.status = {3: str(yesterday), 1: str(yesterday)}
        campaign.save()
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1,2')
        self.assertEqual(campaign.status, {3: str(yesterday),
                                           1: str(yesterday),
                                           2: str(datetime.date.today())})

    def test_handle_less_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        campaign = models.Campaign.objects.get(reference_name='Success')
        eg = models.EmailGroup.objects.get(pk=campaign.email_group.pk)
        eg.email_order = '3,1,2,4'
        eg.save()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1,2,4')
        campaign.status = {3: str(yesterday), 1: str(yesterday)}
        campaign.save()
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1,2')
        self.assertEqual(campaign.status, {3: str(yesterday),
                                           1: str(yesterday),
                                           2: str(datetime.date.today())})

    def test_handle_more_and_less_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        campaign = models.Campaign.objects.get(reference_name='Success')
        eg = models.EmailGroup.objects.get(pk=campaign.email_group.pk)
        eg.email_order = '3,1,4'
        eg.save()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1,4')
        campaign.status = {3: str(yesterday), 1: str(yesterday)}
        campaign.save()
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.email_group.email_order, '3,1,2')
        self.assertEqual(campaign.status, {3: str(yesterday),
                                           1: str(yesterday),
                                           2: str(datetime.date.today())})

    def test_handle_completed(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        campaign = models.Campaign.objects.get(reference_name='Success')
        campaign.status = {3: str(yesterday), 1: str(yesterday),
                           2: str(yesterday)}
        campaign.save()
        self.cmd.execute()
        campaign = models.Campaign.objects.get(reference_name='Success')
        self.assertEqual(campaign.completed_date, datetime.date.today())

class UtilTests(TestCase):

    def setUp(self):
        self.recipient = models.Recipient(first_name='John', last_name='Smith',
                                     email='sample@email.com')
        self.email = models.Email(subject='Subject1', message='Message1')

    def test_send_django_mail(self):
        utils.send_email(self.email, self.recipient)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject1')
        self.assertEqual(mail.outbox[0].body, 'Message1')
        self.assertEqual(mail.outbox[0].to, ['John Smith <sample@email.com>',])

    # Creates a folders in media /media/email_attachments/2014/XX/XX/
    def test_attachment_send_django_email(self):
        eg = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eg.save()
        eg.email_set.create(subject='Subject1', message='Message1')
        eg.save()
        email = models.Email.objects.get(subject='Subject1')
        email.save()
        attachment = email.attachment_set.create(file_name='TestFile',
            attachment=SimpleUploadedFile('Test.docx', 'File Contents'))
        email.save()
        utils.send_email(email, self.recipient)
        self.assertEqual(mail.outbox[0].attachments,
                         [('Test.docx', 'File Contents', None)])
        models.Attachment.objects.get(pk=1).attachment.delete()

    @unittest.skip('Creates a file /media/email_attachments/2014/XX/XX/Test.docx')
    @override_settings(DEBUG=False)
    @override_settings(SENDGRID=True)
    @override_settings(SENDGRID_USERNAME='')
    @override_settings(SENDGRID_PASSWORD='')
    def test_sendgrid_attachment_email(self):
        eg = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eg.save()
        eg.email_set.create(subject='Subject1', message='Message1')
        eg.save()
        email = models.Email.objects.get(subject='Subject1')
        email.save()
        email.attachment_set.create(file_name='TestFile',
            attachment=SimpleUploadedFile('Test.docx', 'File Contents'))
        email.save()
        self.recipient.email = 'john@email.com'
        utils.send_email(email, self.recipient)
        models.Attachment.objects.get(pk=1).attachment.delete()

    # TODO Find way to put SendGrid Info without leaving it in the repo
    @unittest.skip('Test will send out emails')
    @override_settings(DEBUG=False)
    @override_settings(SENDGRID=True)
    @override_settings(SENDGRID_USERNAME='')
    @override_settings(SENDGRID_PASSWORD='')
    def test_sendgrid_mail(self):
        self.recipient.email = 'sample@email.com'
        utils.send_email(self.email, self.recipient)
