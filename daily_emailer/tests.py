import datetime
import json
import unittest

from django.contrib.auth.models import User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from daily_emailer import models, utils
from daily_emailer.management.commands import send_daily_email


class AjaxAssociatedEmailTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            'Admin',
            'admin@sample.com',
            'password')

        user.is_staff = True
        user.save()
        eg = models.EmailGroup(group_name='NewRep')
        eg.save()
        eg.email.create(subject='Subject1', message='Message1')
        eg.email.create(subject='Subject2', message='Message2')
        eg.email.create(subject='Subject3', message='Message3')
        eg.save()
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


class SendDailyEmailTests(TestCase):

    def setUp(self):
        recipient = models.Recipient(first_name='John', last_name='Smith',
                                     email='sample@email.com')
        recipient.save()
        eg = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eg.save()
        self.email1 = eg.email.create(subject='Subject1', message='Message1')
        self.email2 = eg.email.create(subject='Subject2', message='Message2')
        self.email3 = eg.email.create(subject='Subject3', message='Message3')
        eg.save()
        self.campaign = models.Campaign(
            reference_name='RefName',
            start_date=str(datetime.date.today()),
            email_group=eg,
            recipient=recipient)
        self.campaign.save()
        self.campaign.sent_email.create(
            email=self.email3,
            sent_date=datetime.date.today())
        self.campaign.save()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.success = models.Campaign(
            reference_name='Success',
            start_date=str(datetime.date.today()),
            email_group=eg,
            recipient=recipient)
        self.success.save()
        self.success.sent_email.create(email=self.email3, sent_date=yesterday)
        self.cmd = send_daily_email.Command()

    def test_get_next_email_success(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.campaign.sent_email.create(
            email=self.email3,
            sent_date=datetime.date.today())
        self.campaign.save()
        self.assertEqual(self.cmd.get_next_email(emails, [3, 1, 2],
                         self.campaign).pk, 1)

    def test_get_next_email_fail(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.campaign.sent_email.create(
            email=self.email1,
            sent_date=datetime.date.today())
        self.campaign.sent_email.create(
            email=self.email2,
            sent_date=datetime.date.today())
        self.campaign.sent_email.create(
            email=self.email3,
            sent_date=datetime.date.today())
        self.campaign.save()
        self.assertEqual(self.cmd.get_next_email(emails, [3, 1, 2],
                         self.campaign), False)

    def test_reconcile_emails_addition(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(emails, [3, 1]), [3, 1, 2])

    def test_reconcile_emails_subtraction(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(
            emails, [5, 3, 1, 4, 2]), [3, 1, 2])

    def test_reconcile_emails_no_change(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(
            emails, [3, 1, 2]), [3, 1, 2])

    def test_reconcile_emails_add_and_sub(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.reconcile_emails(
            emails, [3, 4, 2]), [3, 2, 1])

    def test_get_ok_to_mail_completed(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        campaign.completed_date = str(datetime.date.today())
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_today(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        models.SentEmail.objects.all().delete()
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_tomorrow(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        models.SentEmail.objects.all().delete()
        campaign.start_date += datetime.timedelta(days=1)
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_no_status_yesterday(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        models.SentEmail.objects.all().delete()
        campaign.start_date -= datetime.timedelta(days=1)
        self.assertTrue(self.cmd.get_ok_to_mail(campaign))

    def test_get_ok_to_mail_none_today(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        models.SentEmail.objects.all().delete()
        self.campaign.sent_email.create(
            email=self.email3, sent_date=yesterday)
        self.campaign.save()
        self.assertTrue(self.cmd.get_ok_to_mail(self.campaign))

    def test_get_ok_to_mail_none_today_or_day_before(self):
        models.SentEmail.objects.all().delete()
        two_yesterday = datetime.date.today() - datetime.timedelta(days=2)
        self.campaign.sent_email.create(
            email=self.email3, sent_date=two_yesterday)
        self.campaign.save()
        self.assertTrue(self.cmd.get_ok_to_mail(self.campaign))

    def test_get_ok_to_mail_mailed_today(self):
        campaign = models.Campaign.objects.get(reference_name='RefName')
        self.assertFalse(self.cmd.get_ok_to_mail(campaign))

    def test_handle_success(self):
        self.cmd.execute()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        email_sent = models.SentEmail.objects.all().filter(
            campaign=self.success)
        self.assertEqual(email_sent[0].email.pk, 3)
        self.assertEqual(email_sent[0].sent_date, yesterday)
        self.assertEqual(email_sent[1].email.pk, 1)
        self.assertEqual(email_sent[1].sent_date, datetime.date.today())
        self.assertEqual(len(mail.outbox), 1)

    def test_handle_already_sent_today(self):
        self.cmd.execute()
        email_sent = models.SentEmail.objects.all().filter(
            campaign=self.campaign)
        self.assertEqual(email_sent[0].email.pk, 3)
        self.assertEqual(email_sent[0].sent_date, datetime.date.today())
        with self.assertRaises(IndexError):
            email_sent[1].email.pk

    def test_handle_additional_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        models.SentEmail.objects.all().delete()

        self.success.sent_email.create(
            email=self.email3, sent_date=yesterday)
        self.success.sent_email.create(
            email=self.email1, sent_date=yesterday)
        self.success.save()

        eg = models.EmailGroup.objects.get(pk=self.success.email_group.pk)
        eg.email_order = '3,1'
        eg.save()

        self.cmd.execute()
        self.assertEqual(self.success.email_group.email_order, '3,1,2')
        email_sent = models.SentEmail.objects.all().filter(
            campaign=self.success)
        self.assertEqual(email_sent[2].email.pk, 2)
        self.assertEqual(email_sent[2].sent_date, datetime.date.today())

    def test_handle_less_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        models.SentEmail.objects.all().delete()

        self.success.sent_email.create(
            email=self.email3, sent_date=yesterday)
        self.success.sent_email.create(
            email=self.email1, sent_date=yesterday)
        self.success.save()

        eg = models.EmailGroup.objects.get(pk=self.success.email_group.pk)
        eg.email_order = '3,1,2,4'
        eg.save()

        self.cmd.execute()
        self.assertEqual(self.success.email_group.email_order, '3,1,2')
        email_sent = models.SentEmail.objects.all().filter(
            campaign=self.success)
        self.assertEqual(email_sent[2].email.pk, 2)
        self.assertEqual(email_sent[2].sent_date, datetime.date.today())

    def test_handle_more_and_less_emails(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        models.SentEmail.objects.all().delete()

        self.success.sent_email.create(
            email=self.email3, sent_date=yesterday)
        self.success.sent_email.create(
            email=self.email1, sent_date=yesterday)
        self.success.save()

        eg = models.EmailGroup.objects.get(pk=self.success.email_group.pk)
        eg.email_order = '3,1,4'
        eg.save()

        self.cmd.execute()
        self.assertEqual(self.success.email_group.email_order, '3,1,2')
        email_sent = models.SentEmail.objects.all().filter(
            campaign=self.success)
        self.assertEqual(email_sent[2].email.pk, 2)
        self.assertEqual(email_sent[2].sent_date, datetime.date.today())

    def test_handle_completed(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        models.SentEmail.objects.all().delete()
        self.campaign.delete()
        self.assertEqual(len(models.SentEmail.objects.all().filter(
            campaign=self.success)), 0)

        self.success.sent_email.create(
            email=self.email3, sent_date=yesterday)
        self.success.sent_email.create(
            email=self.email1, sent_date=yesterday)
        self.success.sent_email.create(
            email=self.email2, sent_date=yesterday)
        self.success.save()

        self.assertEqual(len(models.SentEmail.objects.all().filter(
            campaign=self.success)), 3)
        self.cmd.execute()

        campaign = models.Campaign.objects.get(reference_name="Success")
        self.assertEqual(len(models.SentEmail.objects.all().filter(
            campaign=campaign)), 3)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(campaign.completed_date, datetime.date.today())


class UtilTests(TestCase):

    def setUp(self):
        self.recipient = models.Recipient(
            first_name='John',
            last_name='Smith',
            email='sample@email.com')
        self.email = models.Email(subject='Subject1', message='Message1')

    def tearDown(self):
        try:
            models.Attachment.objects.get(pk=1).attachment.delete()
        except:
            pass

    def test_send_django_mail(self):
        utils.send_email(self.email, self.recipient)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject1')
        self.assertEqual(mail.outbox[0].body, 'Message1')
        self.assertEqual(mail.outbox[0].to, ['John Smith <sample@email.com>'])

    # Creates a folders in media /media/email_attachments/2014/XX/XX/
    def test_attachment_send_django_email(self):
        eg = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eg.save()
        eg.email.create(subject='Subject1', message='Message1')
        eg.save()
        email = models.Email.objects.get(subject='Subject1')
        email.save()
        email.attachment_set.create(
            file_name='TestFile',
            attachment=SimpleUploadedFile('Test.docx', 'File Contents'))
        email.save()
        utils.send_email(email, self.recipient)
        self.assertEqual(mail.outbox[0].attachments,
                         [('Test.docx', 'File Contents', None)])

    @unittest.skip('Creates a file '
                   '/media/email_attachments/2014/XX/XX/Test.docx')
    @override_settings(DEBUG=False)
    @override_settings(SENDGRID=True)
    @override_settings(SENDGRID_USERNAME='')
    @override_settings(SENDGRID_PASSWORD='')
    def test_sendgrid_attachment_email(self):
        eg = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eg.save()
        eg.email.create(subject='Subject1', message='Message1')
        eg.save()
        email = models.Email.objects.get(subject='Subject1')
        email.save()
        email.attachment_set.create(
            file_name='TestFile',
            attachment=SimpleUploadedFile('Test.docx', 'File Contents'))
        email.save()
        self.recipient.email = 'john@email.com'
        utils.send_email(email, self.recipient)

    # TODO Find way to put SendGrid Info without leaving it in the repo
    @unittest.skip('Test will send out emails')
    @override_settings(DEBUG=False)
    @override_settings(SENDGRID=True)
    @override_settings(SENDGRID_USERNAME='')
    @override_settings(SENDGRID_PASSWORD='')
    def test_sendgrid_mail(self):
        self.recipient.email = 'sample@email.com'
        utils.send_email(self.email, self.recipient)
