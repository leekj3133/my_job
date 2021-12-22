from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=40, primary_key=True)
    company = models.CharField(max_length=40)
    url = models.CharField(max_length=40)

    def __str__(self):
        return self.title
