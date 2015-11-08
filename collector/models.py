from django.db import models

class Offer(models.Model):
    poblation = models.CharField(max_length=256)
    description = models.CharField(max_length=5000, blank=True, null=True)
    aplications = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    salary_min = models.IntegerField(blank=True, null=True)
    fetching_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.description