import datetime

from redactor.fields import RedactorField
from django.db import models


try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=254)
    author = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    content = RedactorField()


    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        timestamp = datetime.datetime.today()
        if not self.id:
            self.created = timestamp
        self.updated = timestamp
        return super(Blog, self).save(*args, **kwargs)


def __str__(self):
    return self.title
