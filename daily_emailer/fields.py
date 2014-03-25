from django.db import models

class OrderField(models.TextField):

    description = 'Order of emails to be sent'

    def __init__(self, *args, **kwargs):
        super(OrderField, self).__init__(*args, **kwargs)
