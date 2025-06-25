import ulid
from django.db import models


class ULIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26
        kwargs['default'] = self.generate_ulid
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    @staticmethod
    def generate_ulid():
        return str(ulid.new())
