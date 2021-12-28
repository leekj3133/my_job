from django.db import models

# Create your models here.
class Jobapp(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    company = models.CharField(max_length=100)
    url = models.URLField(verbose_name="Site URL")

    def __str__(self):
        return self.text
