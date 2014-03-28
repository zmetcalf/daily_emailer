from django.db import models

class OrderField(models.TextField):

    description = 'Order of emails to be sent.'

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(OrderField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == None:
            return []

        formated_list = list(map(int, value.strip('[]').split(',')))
        return formated_list

class StatusField(models.TextField):

    description = 'Tracks which emails have been sent.'

    def __init__(self, *args, **kwargs):
        super(StatusField, self).__init__(*args, **kwargs)
