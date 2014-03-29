import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from daily_emailer import models, fields

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
        response = self.client.post('/associated_emails/1/')
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], 1)
        self.assertEqual(data[0]['fields']['message'], 'Message1')
        self.assertEqual(data[1]['fields']['message'], 'Message2')
        self.assertEqual(data[2]['fields']['message'], 'Message3')

    def test_ajax_associated_emails_authenticated_empty(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/associated_emails/2/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_ajax_associated_emails_authenticated(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/associated_emails/1/')
        self.assertEqual(response.status_code, 200)

    def test_ajax_associated_emails_unauthenticated(self):
        response = self.client.post('/associated_emails/1/')
        self.assertEqual(response.status_code, 404)

'''May go away with custom field
class OrderFieldTests(TestCase):

    def setUp(self):
        eq = models.EmailGroup(group_name='NewRep', email_order='3,4,1')
        eq.save()

    def test_order_field_to_python(self):
        email_group = models.EmailGroup.objects.all().filter(group_name='NewRep')
        self.assertEqual(email_group[0].email_order, [3,4,1])
'''
