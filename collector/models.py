from django.db import models
        
class Offer(models.Model):
    offer = models.CharField(max_length=256, primary_key=True, null=False)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    requirements = models.CharField(max_length=5000, blank=True, null=True)
    link = models.URLField(max_length=5000, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    province = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    fetch_date = models.DateTimeField(null=True)
    publish_date = models.DateTimeField(null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    salary_min = models.IntegerField(blank=True, null=True)
    applications = models.IntegerField(blank=True, null=True)
    vacancies = models.IntegerField(blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title