from django.db import models

# Create your models here.
class GetInfo(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    company = models.CharField(max_length=100)
    url = models.URLField(verbose_name="Site URL")
    word = models.CharField(max_length=40, default = '')

    def __str__(self):
        return self.title
