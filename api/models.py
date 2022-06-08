from statistics import mode
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    ric_code = models.CharField(max_length=50)
    esg_score = models.IntegerField(blank=True, null=True)
    environment_score = models.IntegerField(blank=True, null=True)
    social_score = models.IntegerField(blank=True, null=True)
    governance_score = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

