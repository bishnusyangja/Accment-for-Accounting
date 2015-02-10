from django.db import models

from users.models import Company


class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    percent = models.FloatField()
    company = models.ForeignKey(Company)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' (' + str(self.percent) + '%)'
