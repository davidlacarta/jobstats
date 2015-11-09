from django.db import models

class Offer(models.Model):
    id_supplier = models.CharField(max_length=256, primary_key=True, null=False)
    poblation = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    applications = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    salary_min = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.description