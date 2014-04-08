from ast import literal_eval
from collections import MutableMapping

from django.db import models

class StatusField(models.TextField):

    description = 'Tracks which emails have been sent.'

    def __init__(self, *args, **kwargs):
        super(StatusField, self).__init__(*args, **kwargs)

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value == None or value == '':
            return {}

        if isinstance(value, MutableMapping):
            return value

        return literal_eval(value)
