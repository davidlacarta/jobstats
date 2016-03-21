from django.db import models

class Provider(models.Model):
    key = models.CharField(max_length=256, null=False, unique=True)
    value = models.CharField(max_length=256, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.value if self.value else self.key
        
        
class Country(models.Model):
    key = models.CharField(max_length=256, null=False, unique=True)
    value = models.CharField(max_length=256, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.value if self.value else self.key
        
        
class Province(models.Model):
    country = models.ForeignKey(Country)
    key = models.CharField(max_length=256, null=False)
    value = models.CharField(max_length=256, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.value if self.value else self.key
        
    class Meta:
        unique_together = (("country", "key"),)
        

class City(models.Model):
    province = models.ForeignKey(Province)
    key = models.CharField(max_length=256, null=False)
    value = models.CharField(max_length=256, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.value if self.value else self.key

    class Meta:
        unique_together = (("province", "key"),)
        
        
class Offer(models.Model):
    provider = models.ForeignKey(Provider)
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    key = models.CharField(max_length=256, null=False)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    requirements = models.CharField(max_length=5000, blank=True, null=True)
    link = models.URLField(max_length=5000, blank=True, null=True)
    fetch_date = models.DateTimeField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    salary_min = models.IntegerField(blank=True, null=True)
    experience_min = models.IntegerField(blank=True, null=True)
    applications = models.IntegerField(blank=True, null=True)
    vacancies = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title if self.title else self.key
        
    class Meta:
        unique_together = (("provider", "key"),)