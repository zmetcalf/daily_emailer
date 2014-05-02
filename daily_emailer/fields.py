import warnings

from ast import literal_eval
from collections import MutableMapping

from django.db import models

from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^daily_emailer\.fields\.StatusField"])

class StatusField(models.TextField):

    description = 'Tracks which emails have been sent.'

    def __init__(self, *args, **kwargs):
        warnings.warn('deprecated - used for migration 0001', DeprecationWarning)
        super(StatusField, self).__init__(*args, **kwargs)

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value == None or value == '':
            return {}

        if isinstance(value, MutableMapping):
            return value

        return literal_eval(value)
